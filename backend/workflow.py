# ============================================================
# BRANDFORGE AI - STRUCTURED WORKFLOW
# ============================================================

from ai_service import (
    ask_ai,
    parse_json_response
)

from prompts import (
    discover_prompt,
    discover_retry_prompt,
    position_prompt,
    position_retry_prompt,
    shape_prompt,
    shape_retry_prompt,
    challenge_prompt,
    visualize_prompt,
    deliver_prompt
)


# ============================================================
# STRUCTURED AI STAGE
# ============================================================

def run_structured_stage(
    prompt,
    max_tokens=1200
):
    """
    Run an AI stage and convert the response into
    a Python dictionary.
    """

    raw_response = ask_ai(
        prompt,
        max_tokens=max_tokens
    )

    try:

        result = parse_json_response(
            raw_response
        )

        if not isinstance(result, dict):

            raise ValueError(
                "AI response must be a JSON object."
            )

        return result

    except Exception as e:

        raise RuntimeError(
            "The AI returned an invalid structured response.\n\n"
            f"{str(e)}"
        )


# ============================================================
# 1. DISCOVER
# ============================================================

def run_discover(
    idea,
    additional_context
):

    prompt = discover_prompt(
        idea,
        additional_context
    )

    try:

        return run_structured_stage(
            prompt,
            max_tokens=900
        )

    except RuntimeError as first_error:

        if "invalid structured response" not in str(first_error).lower():
            raise

        retry_prompt = discover_retry_prompt(
            idea,
            additional_context
        )

        try:

            return run_structured_stage(
                retry_prompt,
                max_tokens=900
            )

        except Exception as retry_error:

            raise RuntimeError(
                "Discover returned invalid structured JSON after one retry."
            ) from retry_error


# ============================================================
# 2. POSITION
# ============================================================

def run_position(
    discover_result
):

    prompt = position_prompt(
        discover_result
    )

    try:

        return run_structured_stage(
            prompt,
            max_tokens=900
        )

    except RuntimeError as first_error:

        if "invalid structured response" not in str(first_error).lower():
            raise

        retry_prompt = position_retry_prompt(
            discover_result
        )

        try:

            return run_structured_stage(
                retry_prompt,
                max_tokens=900
            )

        except Exception as retry_error:

            raise RuntimeError(
                "Position returned invalid structured JSON after one retry."
            ) from retry_error


# ============================================================
# 3. SHAPE
# ============================================================

def run_shape(
    discover_result,
    position_result
):

    prompt = shape_prompt(
        discover_result,
        position_result
    )

    try:

        return run_structured_stage(
            prompt,
            max_tokens=1000
        )

    except RuntimeError as first_error:

        if "invalid structured response" not in str(first_error).lower():
            raise

        retry_prompt = shape_retry_prompt(
            discover_result,
            position_result
        )

        try:

            return run_structured_stage(
                retry_prompt,
                max_tokens=1000
            )

        except Exception as retry_error:

            raise RuntimeError(
                "Shape returned invalid structured JSON after one retry."
            ) from retry_error


# ============================================================
# 4. CHALLENGE
# ============================================================

def run_challenge(
    position_result,
    shape_result
):

    prompt = challenge_prompt(
        position_result,
        shape_result
    )

    return run_structured_stage(
        prompt,
        max_tokens=1800
    )


# ============================================================
# 5. VISUALIZE
# ============================================================

def run_visualize(
    challenge_result
):

    prompt = visualize_prompt(
        challenge_result
    )

    return run_structured_stage(
        prompt,
        max_tokens=850
    )


# ============================================================
# 6. DELIVER
# ============================================================

def run_deliver(
    challenge_result,
    visualize_result
):

    prompt = deliver_prompt(
        challenge_result,
        visualize_result
    )

    return run_structured_stage(
        prompt,
        max_tokens=1400
    )