import json
import os
import re
import time

from dotenv import load_dotenv
from groq import Groq
from groq import RateLimitError
from openai import OpenAI


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-oss-20b"
)

if not groq_api_key and not openrouter_api_key:
    raise ValueError(
        "No AI provider is configured.\n\n"
        "Add GROQ_API_KEY or OPENROUTER_API_KEY to .env."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = (
    Groq(
        api_key=groq_api_key,
        max_retries=0
    )
    if groq_api_key
    else None
)


# ============================================================
# OPENROUTER CLIENT
# ============================================================

openrouter_client = (
    OpenAI(
        api_key=openrouter_api_key,
        base_url="https://openrouter.ai/api/v1"
    )
    if openrouter_api_key
    else None
)


# ============================================================
# PROVIDER STATE
# ============================================================

last_provider = None

MODEL = "openai/gpt-oss-20b"


# ============================================================
# ERROR DETECTION
# ============================================================

def _is_retryable_error(error):
    """Return whether an API failure is likely temporary."""

    status_code = getattr(error, "status_code", None)

    if status_code in {408, 409, 429, 500, 502, 503, 504}:
        return True

    error_text = str(error).lower()

    return any(
        phrase in error_text
        for phrase in (
            "timed out",
            "timeout",
            "temporarily unavailable",
            "connection reset",
            "connection error",
            "rate limit",
            "tokens per minute",
            "tokens per day",
            "daily quota",
            "quota",
            "overloaded",
            "service unavailable"
        )
    )


def _should_fallback_to_openrouter(error):
    """Return whether a Groq failure should trigger OpenRouter fallback."""

    status_code = getattr(error, "status_code", None)

    if status_code in {408, 409, 429, 500, 502, 503, 504}:
        return True

    error_text = str(error).lower()

    return any(
        phrase in error_text
        for phrase in (
            "rate limit",
            "tokens per minute",
            "tokens per day",
            "daily quota",
            "quota",
            "temporarily unavailable",
            "service unavailable",
            "overloaded",
            "timed out",
            "timeout",
            "connection reset",
            "connection error"
        )
    )


# ============================================================
# OPENROUTER REQUEST
# ============================================================

def _ask_openrouter(prompt, max_tokens):
    """
    Generate a response using OpenRouter.

    OpenRouter is used as the fallback provider.
    A larger token budget is used because reasoning models
    can consume output tokens before producing final content.
    """

    global last_provider

    if openrouter_client is None:
        raise RuntimeError(
            "OpenRouter is not configured. "
            "Add OPENROUTER_API_KEY to .env."
        )

    # Give OpenRouter more room than the original request.
    # This is especially important for the Deliver stage.
    requested_tokens = max(
        int(max_tokens or 1200),
        3000
    )

    last_error = None

    for attempt in range(2):

        try:

            response = openrouter_client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=requested_tokens
            )

            # ----------------------------------------------------
            # Validate choices
            # ----------------------------------------------------

            if not response.choices:
                raise RuntimeError(
                    "OpenRouter returned no choices."
                )

            choice = response.choices[0]

            message = choice.message

            if message is None:
                raise RuntimeError(
                    "OpenRouter returned an empty message."
                )

            # ----------------------------------------------------
            # Read normal content
            # ----------------------------------------------------

            content = getattr(message, "content", None)

            if content and str(content).strip():

                last_provider = "OpenRouter"

                return str(content).strip()

            # ----------------------------------------------------
            # Some reasoning models may expose reasoning separately.
            #
            # Do NOT blindly return reasoning as final JSON because
            # it may not be valid JSON.
            # Instead, retry with a stronger instruction.
            # ----------------------------------------------------

            reasoning = getattr(message, "reasoning", None)

            if reasoning:
                last_error = RuntimeError(
                    "OpenRouter returned reasoning but no final content."
                )
            else:
                last_error = RuntimeError(
                    "OpenRouter returned an empty response."
                )

        except Exception as error:

            last_error = error

        # --------------------------------------------------------
        # Retry once with stricter JSON/output instruction
        # --------------------------------------------------------

        if attempt == 0:

            retry_prompt = f"""
Return the final answer only.

Do not provide analysis.
Do not provide reasoning.
Do not explain your answer.
Do not use markdown.
Do not use code fences.

If the requested format is JSON, return ONLY the JSON object.

Original task:

{prompt}
"""

            prompt = retry_prompt

            # Increase budget for retry
            requested_tokens = max(
                requested_tokens,
                4000
            )

            time.sleep(1)

    raise RuntimeError(
        f"OpenRouter request failed: {last_error}"
    )


# ============================================================
# PROVIDER STATUS
# ============================================================

def get_last_provider():
    """Return the provider used for the most recent successful request."""

    return last_provider


# ============================================================
# AI REQUEST
# ============================================================

def ask_ai(
    prompt,
    retries=3,
    max_tokens=1200
):
    """
    Send a prompt to the AI provider.

    Provider order:

    1. Groq
    2. OpenRouter fallback

    If Groq is unavailable because of quota/rate-limit/
    temporary errors, OpenRouter is used immediately.

    The public ask_ai() interface remains unchanged.
    """

    global last_provider

    # --------------------------------------------------------
    # No provider available
    # --------------------------------------------------------

    if client is None and openrouter_client is None:
        raise RuntimeError(
            "No AI provider is configured. "
            "Add GROQ_API_KEY or OPENROUTER_API_KEY to .env."
        )

    # --------------------------------------------------------
    # If Groq is not configured, use OpenRouter
    # --------------------------------------------------------

    if client is None:

        try:
            return _ask_openrouter(
                prompt,
                max_tokens
            )

        except Exception as error:

            raise RuntimeError(
                f"OpenRouter request failed: {error}"
            ) from error

    last_error = None

    # --------------------------------------------------------
    # GROQ PRIMARY
    # --------------------------------------------------------

    for attempt in range(max(1, retries)):

        try:

            response = client.chat.completions.create(
                model=MODEL,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.4,

                max_tokens=max_tokens
            )

            # ------------------------------------------------
            # Validate response
            # ------------------------------------------------

            if not response.choices:
                raise RuntimeError(
                    "Groq returned no choices."
                )

            message = response.choices[0].message

            if message is None:
                raise RuntimeError(
                    "Groq returned an empty message."
                )

            content = message.content

            if content and content.strip():

                last_provider = "Groq"

                return content.strip()

            last_error = RuntimeError(
                "Groq returned an empty response."
            )

            if attempt < retries - 1:
                time.sleep(2)
                continue

        except RateLimitError as error:

            # ------------------------------------------------
            # IMMEDIATE OPENROUTER FALLBACK
            # ------------------------------------------------

            if openrouter_client is None:
                raise RuntimeError(
                    "Groq rate limit reached and "
                    "OPENROUTER_API_KEY is not configured."
                ) from error

            try:

                return _ask_openrouter(
                    prompt,
                    max_tokens
                )

            except Exception as openrouter_error:

                raise RuntimeError(
                    "Both Groq and OpenRouter are temporarily "
                    "unavailable.\n\n"
                    f"Groq: {error}\n\n"
                    f"OpenRouter: {openrouter_error}"
                ) from openrouter_error

        except Exception as error:

            last_error = error

            # ------------------------------------------------
            # TEMPORARY GROQ FAILURE
            # ------------------------------------------------

            if _should_fallback_to_openrouter(error):

                if openrouter_client is None:
                    raise RuntimeError(
                        "Groq is temporarily unavailable and "
                        "OPENROUTER_API_KEY is not configured."
                    ) from error

                try:

                    return _ask_openrouter(
                        prompt,
                        max_tokens
                    )

                except Exception as openrouter_error:

                    raise RuntimeError(
                        "Both Groq and OpenRouter are temporarily "
                        "unavailable.\n\n"
                        f"Groq: {error}\n\n"
                        f"OpenRouter: {openrouter_error}"
                    ) from openrouter_error

            # ------------------------------------------------
            # NON-TEMPORARY ERROR
            # ------------------------------------------------

            if not _is_retryable_error(error):

                raise RuntimeError(
                    f"AI request failed: {error}"
                ) from error

            # ------------------------------------------------
            # RETRY TEMPORARY GROQ ERRORS
            # ------------------------------------------------

            if attempt < retries - 1:
                time.sleep(2)
                continue

    # --------------------------------------------------------
    # ALL GROQ RETRIES FAILED
    # --------------------------------------------------------

    if openrouter_client is not None:

        try:

            return _ask_openrouter(
                prompt,
                max_tokens
            )

        except Exception as openrouter_error:

            raise RuntimeError(
                "Both Groq and OpenRouter failed.\n\n"
                f"Groq: {last_error}\n\n"
                f"OpenRouter: {openrouter_error}"
            ) from openrouter_error

    raise RuntimeError(
        f"AI request failed: {last_error}"
    ) from last_error


# ============================================================
# JSON PARSER
# ============================================================

def parse_json_response(response_text):
    """
    Convert an AI response into a Python dictionary.

    Handles:
    - normal JSON
    - JSON inside ```json ... ```
    - accidental surrounding text
    """

    if not response_text:
        raise ValueError(
            "AI returned an empty response."
        )

    text = response_text.strip()

    # --------------------------------------------------------
    # Remove markdown code fences
    # --------------------------------------------------------

    text = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        text,
        flags=re.IGNORECASE
    ).strip()

    # --------------------------------------------------------
    # Direct JSON
    # --------------------------------------------------------

    try:

        return json.loads(text)

    except json.JSONDecodeError:
        pass

    # --------------------------------------------------------
    # Extract JSON object from surrounding text
    # --------------------------------------------------------

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:

        json_text = text[
            start:end + 1
        ]

        try:

            return json.loads(json_text)

        except json.JSONDecodeError:
            pass

    # --------------------------------------------------------
    # Error diagnostics
    # --------------------------------------------------------

    open_braces = text.count("{")
    closed_braces = text.count("}")

    if start != -1 and (
        end == -1 or open_braces > closed_braces
    ):

        reason = (
            "The AI response appears to be "
            "incomplete JSON."
        )

    else:

        reason = (
            "The AI response was not valid JSON."
        )

    raise ValueError(
        f"{reason}\n\n"
        f"Response received:\n{text[:3000]}"
    )