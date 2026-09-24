# ============================================================
# BRANDFORGE AI
# Structured AI Brand Strategy Dashboard
# ============================================================

import io
import html
import traceback

import streamlit as st

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT

from workflow import (
    run_discover,
    run_position,
    run_shape,
    run_challenge,
    run_visualize,
    run_deliver
)

from demo_data import (
    DEMO_CONTEXT,
    DEMO_IDEA,
    get_demo_workflow
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BrandForge AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    :root {
        color-scheme: light;
    }

    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stMain"], [data-testid="stHeader"] {
        background: #FFFFFF !important;
        color: #111827 !important;
    }

    [data-testid="stSidebar"], [data-testid="stToolbar"] {
        background: #FFFFFF !important;
    }

    [data-testid="stMarkdownContainer"], label,
    [data-testid="stTextInput"] *, [data-testid="stTextArea"] *,
    [data-testid="stSelectbox"] * {
        color: #111827;
    }

    input, textarea, select,
    [data-baseweb="select"] > div {
        background: #FFFFFF !important;
        color: #111827 !important;
        border-color: #E5E7EB !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E5E7EB;
        background: #FFFFFF;
    }

    [data-testid="stDataFrame"] iframe {
        background: #FFFFFF !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        background-color: #111827 !important;
        color: #FFFFFF !important;
        border: 1px solid #111827 !important;
        font-weight: 700 !important;
    }

    .stButton > button p,
    .stButton > button span,
    .stDownloadButton > button p,
    .stDownloadButton > button span {
        color: #FFFFFF !important;
    }

    .stButton > button:hover,
    .stButton > button:focus,
    .stButton > button:focus-visible,
    .stButton > button:active,
    .stDownloadButton > button:hover,
    .stDownloadButton > button:focus,
    .stDownloadButton > button:focus-visible,
    .stDownloadButton > button:active {
        background-color: #1F2937 !important;
        color: #FFFFFF !important;
        border-color: #1F2937 !important;
    }

    .stButton > button:hover p,
    .stButton > button:hover span,
    .stButton > button:focus p,
    .stButton > button:focus span,
    .stButton > button:focus-visible p,
    .stButton > button:focus-visible span,
    .stButton > button:active p,
    .stButton > button:active span,
    .stDownloadButton > button:hover p,
    .stDownloadButton > button:hover span,
    .stDownloadButton > button:focus p,
    .stDownloadButton > button:focus span,
    .stDownloadButton > button:focus-visible p,
    .stDownloadButton > button:focus-visible span,
    .stDownloadButton > button:active p,
    .stDownloadButton > button:active span {
        color: #FFFFFF !important;
    }

    [data-testid="stAlert"] {
        color: #111827 !important;
        border: 1px solid #E5E7EB;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .stage-card {
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        padding: 18px;
        background: #FFFFFF;
        margin-bottom: 15px;
    }

    .stage-number {
        font-size: 13px;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stage-title {
        font-size: 24px;
        font-weight: 750;
        margin-top: 3px;
    }

    .metric-card {
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px;
        background: #FFFFFF;
        min-height: 115px;
    }

    .metric-title {
        font-size: 13px;
        color: #6B7280;
        font-weight: 600;
    }

    .metric-value {
        font-size: 18px;
        font-weight: 700;
        margin-top: 7px;
        line-height: 1.35;
    }

    .badge {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border-radius: 20px;
        background: #F3F4F6;
        font-size: 13px;
        font-weight: 600;
    }

    .high {
        background: #FEE2E2;
        color: #991B1B;
    }

    .medium {
        background: #FEF3C7;
        color: #92400E;
    }

    .low {
        background: #DCFCE7;
        color: #166534;
    }

    .aligned {
        background: #DCFCE7;
        color: #166534;
    }

    .review {
        background: #FEF3C7;
        color: #92400E;
    }

    .conflict {
        background: #FEE2E2;
        color: #991B1B;
    }

    .insight-box {
        border-left: 5px solid #004E92;
        padding: 16px;
        background: #F8FAFC;
        border-radius: 8px;
        margin: 12px 0;
    }

    .swatch {
        height: 90px;
        border-radius: 12px;
        margin-bottom: 8px;
        border: 1px solid #E5E7EB;
    }

    .swatch-label {
        font-weight: 700;
        font-size: 14px;
    }

    .swatch-code {
        font-size: 13px;
        color: #666;
    }

    .final-board {
        border: 2px solid #E5E7EB;
        border-radius: 18px;
        padding: 25px;
        background: #FFFFFF;
        margin-top: 15px;
    }

    .workflow {
        text-align: center;
        font-size: 16px;
        font-weight: 700;
        padding: 15px;
        background: #F8FAFC;
        border-radius: 12px;
        margin: 15px 0 25px 0;
    }

    .small-muted {
        color: #6B7280;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe(value, default="—"):
    """
    Safely convert a value into displayable text.
    """
    if value is None:
        return default

    if isinstance(value, list):
        return ", ".join(
            str(item)
            for item in value
        )

    if isinstance(value, dict):
        return str(value)

    text = str(value).strip()

    return text if text else default


def severity_badge(severity):
    """
    Create a severity badge.
    """

    severity_text = safe(
        severity,
        "Medium"
    )

    css_class = severity_text.lower()

    if css_class not in [
        "high",
        "medium",
        "low"
    ]:
        css_class = "medium"

    return (
        f'<span class="badge {css_class}">'
        f'{html.escape(severity_text.upper())}'
        f'</span>'
    )


def status_badge(status):
    """
    Create a consistency status badge.
    """

    status_text = safe(
        status,
        "Needs Review"
    )

    normalized = status_text.lower()

    if normalized == "aligned":
        css_class = "aligned"

    elif normalized == "conflict":
        css_class = "conflict"

    else:
        css_class = "review"

    return (
        f'<span class="badge {css_class}">'
        f'{html.escape(status_text)}'
        f'</span>'
    )


def metric_card(title, value):
    """
    Render a metric-style card.
    """

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">
                {html.escape(str(title))}
            </div>
            <div class="metric-value">
                {html.escape(safe(value))}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def stage_header(number, title, description):
    """
    Render a stage heading.
    """

    st.markdown(
        f"""
        <div class="stage-card">
            <div class="stage-number">
                Stage {number}
            </div>

            <div class="stage-title">
                {title}
            </div>

            <div class="small-muted">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_badges(items):
    """
    Render a list as badges.
    """

    if not items:
        st.info("No items generated.")

        return

    badges = ""

    for item in items:

        badges += (
            '<span class="badge">'
            + html.escape(safe(item))
            + '</span>'
        )

    st.markdown(
        badges,
        unsafe_allow_html=True
    )

def save_stage_result(stage_name, result, results):
    """Persist a successful stage under both public and internal keys."""

    results[stage_name] = result
    st.session_state[f"{stage_name}_result"] = result

def clear_workflow_state():
    """Clear generated results when the source idea changes."""

    st.session_state["brandforge_results"] = {}

    for stage_name in (
        "discover",
        "position",
        "shape",
        "challenge",
        "visualize",
        "deliver"
    ):
        st.session_state.pop(
            f"{stage_name}_result",
            None
        )

    st.session_state.pop("failed_stage", None)
    st.session_state.pop("workflow_error", None)

def describe_workflow_error(error):
    """Convert known failures into concise, non-sensitive user guidance."""

    error_text = str(error).lower()

    if (
        "429" in error_text
        or "rate limit" in error_text
        or "tokens per minute" in error_text
    ):
        return (
            "Groq rate limit reached during this request. "
            "Please wait a few seconds and retry this stage."
        )

    if "daily token limit" in error_text:
        return (
            "Groq's daily token limit has been reached. "
            "Please try again after the quota resets."
        )

    if "both ai providers" in error_text:
        return "AI providers are temporarily unavailable. Please try again later."

    if (
        "invalid structured response" in error_text
        or "not valid json" in error_text
        or "incomplete json" in error_text
    ):
        return "The AI returned incomplete or invalid JSON for this stage."

    if "groq_api_key" in error_text or "authentication" in error_text:
        return "Groq authentication failed. Check GROQ_API_KEY."

    if "timed out" in error_text or "connection" in error_text:
        return "The AI request could not reach Groq. Please retry this stage."

    return "The stage returned an unexpected error. Please retry this stage."


# ============================================================
# DISCOVER UI
# ============================================================

def render_discover(data):

    stage_header(
        "01",
        "🔎 Discover",
        "Understand the problem before branding."
    )

    col1, col2 = st.columns(2)

    with col1:
        metric_card(
            "Core Problem",
            data.get("core_problem")
        )

    with col2:
        metric_card(
            "Target User",
            data.get("target_user")
        )

    st.markdown("### Problem Landscape")

    pain_points = data.get(
        "pain_points",
        []
    )

    if pain_points:

        rows = []

        for item in pain_points:

            rows.append(
                {
                    "#": len(rows) + 1,
                    "Pain Point": item.get(
                        "title",
                        "—"
                    ),
                    "Impact": item.get(
                        "impact",
                        "Medium"
                    ),
                    "Why it matters": item.get(
                        "description",
                        "—"
                    )
                }
            )

        st.dataframe(
            rows,
            width="stretch",
            hide_index=True
        )

    st.markdown("### Context")

    st.info(
        safe(
            data.get("context")
        )
    )

    st.markdown("### Potential Value")

    render_badges(
        data.get(
            "potential_value",
            []
        )
    )

    st.markdown("### Key Constraints")

    render_badges(
        data.get(
            "constraints",
            []
        )
    )

    st.markdown("### ❓ Unanswered Questions")

    questions = data.get(
        "unanswered_questions",
        []
    )

    if questions:

        question_rows = []

        for question in questions:

            question_rows.append(
                {
                    "#": len(question_rows) + 1,
                    "Question": question,
                    "Status": "Unanswered"
                }
            )

        st.dataframe(
            question_rows,
            width="stretch",
            hide_index=True
        )

    st.markdown("### 💡 Discovery Insight")

    st.markdown(
        f"""
        <div class="insight-box">
            {html.escape(
                safe(data.get("discovery_insight"))
            )}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# POSITION UI
# ============================================================

def render_position(data):

    stage_header(
        "02",
        "🎯 Position",
        "Define where the product fits and why it matters."
    )

    col1, col2 = st.columns(2)

    with col1:
        metric_card(
            "Product Category",
            data.get("product_category")
        )

    with col2:
        metric_card(
            "Primary Audience",
            data.get("primary_audience")
        )

    st.markdown("### Value Proposition")

    st.success(
        safe(
            data.get("value_proposition")
        )
    )

    st.markdown("### Differentiators")

    render_badges(
        data.get(
            "differentiator",
            []
        )
    )

    st.markdown("### Competitive Angle")

    st.info(
        safe(
            data.get("competitive_angle")
        )
    )

    st.markdown("### Positioning Statement")

    st.markdown(
        f"""
        <div class="insight-box">
            {html.escape(
                safe(data.get("positioning_statement"))
            )}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ⚠️ Positioning Risks")

    risks = data.get(
        "positioning_risks",
        []
    )

    if risks:

        rows = []

        for risk in risks:

            rows.append(
                {
                    "Risk": risk.get(
                        "risk",
                        "—"
                    ),
                    "Severity": risk.get(
                        "severity",
                        "Medium"
                    ),
                    "Description": risk.get(
                        "description",
                        "—"
                    )
                }
            )

        st.dataframe(
            rows,
            width="stretch",
            hide_index=True
        )

    st.markdown("### Assumptions")

    render_badges(
        data.get(
            "assumptions",
            []
        )
    )


# ============================================================
# SHAPE UI
# ============================================================

def render_shape(data):

    stage_header(
        "03",
        "✨ Shape",
        "Create the personality, naming direction and voice."
    )

    st.markdown("### Brand Personality")

    render_badges(
        data.get(
            "brand_personality",
            []
        )
    )

    st.markdown("### Traits to Avoid")

    avoid_traits = data.get(
        "traits_to_avoid",
        []
    )

    if avoid_traits:

        badges = ""

        for item in avoid_traits:

            badges += (
                '<span class="badge" '
                'style="background:#FEE2E2;color:#991B1B;">'
                '✕ '
                + html.escape(safe(item))
                + '</span>'
            )

        st.markdown(
            badges,
            unsafe_allow_html=True
        )

    st.markdown("### 🏷️ Naming Territories")

    territories = data.get(
        "naming_territories",
        []
    )

    if territories:

        columns = st.columns(
            min(
                len(territories),
                3
            )
        )

        for index, territory in enumerate(
            territories
        ):

            with columns[
                index % len(columns)
            ]:

                st.markdown(
                    f"#### {safe(territory.get('territory'))}"
                )

                st.caption(
                    safe(
                        territory.get(
                            "description"
                        )
                    )
                )

                names = territory.get(
                    "name_concepts",
                    []
                )

                for name in names:

                    st.markdown(
                        f"**PROPOSED:** {name}"
                    )

    st.markdown("### Tagline Directions")

    render_badges(
        data.get(
            "tagline_directions",
            []
        )
    )

    st.markdown("### Brand Voice")

    voice = data.get(
        "brand_voice",
        []
    )

    if voice:

        voice_rows = []

        for item in voice:

            voice_rows.append(
                {
                    "Voice Trait": item.get(
                        "trait",
                        "—"
                    ),
                    "Meaning": item.get(
                        "description",
                        "—"
                    )
                }
            )

        st.dataframe(
            voice_rows,
            width="stretch",
            hide_index=True
        )

    st.markdown("### Message Hierarchy")

    hierarchy = data.get(
        "message_hierarchy",
        {}
    )

    hierarchy_rows = [
        {
            "Level": "Primary",
            "Message": hierarchy.get(
                "primary",
                "—"
            )
        },
        {
            "Level": "Support 1",
            "Message": hierarchy.get(
                "support_1",
                "—"
            )
        },
        {
            "Level": "Support 2",
            "Message": hierarchy.get(
                "support_2",
                "—"
            )
        }
    ]

    st.dataframe(
        hierarchy_rows,
        width="stretch",
        hide_index=True
    )


# ============================================================
# CHALLENGE UI
# ============================================================

def render_challenge(data):

    stage_header(
        "04",
        "⚔️ Challenge",
        "Stress-test the strategy and remove weak assumptions."
    )

    problems = data.get(
        "problems",
        []
    )

    st.markdown("### AI Risk Matrix")

    if problems:

        rows = []

        for item in problems:

            rows.append(
                {
                    "#": len(rows) + 1,
                    "Problem": item.get(
                        "problem",
                        "—"
                    ),
                    "Severity": item.get(
                        "severity",
                        "Medium"
                    ),
                    "Why it matters": item.get(
                        "why_it_matters",
                        "—"
                    ),
                    "Correction": item.get(
                        "correction",
                        "—"
                    )
                }
            )

        st.dataframe(
            rows,
            width="stretch",
            hide_index=True
        )

    st.markdown("### 🚨 Generic Language Detector")

    generic = data.get(
        "generic_language",
        []
    )

    if generic:

        for phrase in generic:

            st.error(
                f"REMOVE → {phrase}"
            )

    else:
        st.success(
            "No generic language detected."
        )

    st.markdown("### ⚠️ Unsupported Claims")

    claims = data.get(
        "unsupported_claims",
        []
    )

    if claims:

        for claim in claims:

            st.warning(
                f"REVIEW → {claim}"
            )

    else:
        st.success(
            "No unsupported claims detected."
        )

    st.markdown("### Audience & Positioning Risks")

    render_badges(
        data.get(
            "audience_positioning_risks",
            []
        )
    )

    st.markdown("### 🔧 Final Corrections")

    corrections = data.get(
        "final_corrections",
        {}
    )

    correction_rows = [
        {
            "Element": "Positioning",
            "Correction": corrections.get(
                "positioning",
                "—"
            )
        },
        {
            "Element": "Personality",
            "Correction": corrections.get(
                "personality",
                "—"
            )
        },
        {
            "Element": "Naming",
            "Correction": corrections.get(
                "naming",
                "—"
            )
        },
        {
            "Element": "Tagline",
            "Correction": corrections.get(
                "tagline",
                "—"
            )
        },
        {
            "Element": "Messaging",
            "Correction": corrections.get(
                "messaging",
                "—"
            )
        }
    ]

    st.dataframe(
        correction_rows,
            width="stretch",
        hide_index=True
    )

    st.markdown("### Final Decisions")

    decisions = data.get(
        "final_decisions",
        {}
    )

    decision_rows = [
        {
            "Decision": "Audience",
            "Result": decisions.get(
                "audience",
                "—"
            )
        },
        {
            "Decision": "Problem",
            "Result": decisions.get(
                "problem",
                "—"
            )
        },
        {
            "Decision": "Promise",
            "Result": decisions.get(
                "promise",
                "—"
            )
        },
        {
            "Decision": "Differentiator",
            "Result": decisions.get(
                "differentiator",
                "—"
            )
        },
        {
            "Decision": "Naming Direction",
            "Result": decisions.get(
                "naming_direction",
                "—"
            )
        },
        {
            "Decision": "Tagline Direction",
            "Result": decisions.get(
                "tagline_direction",
                "—"
            )
        }
    ]

    st.dataframe(
        decision_rows,
            width="stretch",
        hide_index=True
    )


# ============================================================
# VISUALIZE UI
# ============================================================

def render_visualize(data):

    stage_header(
        "05",
        "🎨 Visualize",
        "Turn the strategy into a coherent visual identity."
    )

    st.markdown("### Visual Concept")

    st.info(
        safe(
            data.get("visual_concept")
        )
    )

    st.markdown("### Logo Direction")

    st.markdown(
        f"""
        <div class="insight-box">
            {html.escape(
                safe(data.get("logo_direction"))
            )}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🎨 Color System")

    color_data = data.get(
        "colors",
        {}
    )

    color_items = [
        (
            "Primary",
            color_data.get(
                "primary",
                "#004E92"
            )
        ),
        (
            "Secondary",
            color_data.get(
                "secondary",
                "#009688"
            )
        ),
        (
            "Accent",
            color_data.get(
                "accent",
                "#FF9800"
            )
        ),
        (
            "Background",
            color_data.get(
                "background",
                "#FFFFFF"
            )
        ),
        (
            "Text",
            color_data.get(
                "text",
                "#333333"
            )
        )
    ]

    columns = st.columns(
        len(color_items)
    )

    for column, (
        label,
        color_code
    ) in zip(
        columns,
        color_items
    ):

        with column:

            st.markdown(
                f"""
                <div
                    class="swatch"
                    style="background:{html.escape(str(color_code))};"
                ></div>

                <div class="swatch-label">
                    {html.escape(label)}
                </div>

                <div class="swatch-code">
                    {html.escape(str(color_code))}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### Typography")

    typography = data.get(
        "typography",
        {}
    )

    typography_rows = [
        {
            "Usage": "Heading",
            "Font": typography.get(
                "heading",
                "—"
            )
        },
        {
            "Usage": "Body",
            "Font": typography.get(
                "body",
                "—"
            )
        }
    ]

    st.dataframe(
        typography_rows,
            width="stretch",
        hide_index=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Graphic Language")

        st.info(
            safe(
                data.get(
                    "graphic_language"
                )
            )
        )

    with col2:

        st.markdown("### Imagery")

        st.info(
            safe(
                data.get(
                    "imagery"
                )
            )
        )

    st.markdown("### UI Direction")

    render_badges(
        data.get(
            "ui_direction",
            []
        )
    )

    st.markdown("### Avoid")

    avoid = data.get(
        "avoid",
        []
    )

    if avoid:

        for item in avoid:

            st.warning(
                f"AVOID → {item}"
            )

    st.markdown("### Visual Rationale")

    st.markdown(
        f"""
        <div class="insight-box">
            {html.escape(
                safe(
                    data.get(
                        "visual_rationale"
                    )
                )
            )}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DELIVER UI
# ============================================================

def render_deliver(data):

    stage_header(
        "06",
        "🚀 Deliver",
        "Your final launch-ready brand system."
    )

    foundation = data.get(
        "brand_foundation",
        {}
    )

    st.markdown("## Final Brand Foundation")

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card(
            "Brand Name",
            foundation.get(
                "brand_name"
            )
        )

    with col2:
        metric_card(
            "Category",
            foundation.get(
                "category"
            )
        )

    with col3:
        metric_card(
            "Target Audience",
            foundation.get(
                "target_audience"
            )
        )

    st.markdown("### Brand Strategy")

    strategy_rows = [
        {
            "Element": "Core Problem",
            "Decision": foundation.get(
                "core_problem",
                "—"
            )
        },
        {
            "Element": "Value Proposition",
            "Decision": foundation.get(
                "value_proposition",
                "—"
            )
        },
        {
            "Element": "Differentiator",
            "Decision": foundation.get(
                "differentiator",
                "—"
            )
        },
        {
            "Element": "Positioning",
            "Decision": foundation.get(
                "positioning_statement",
                "—"
            )
        }
    ]

    st.dataframe(
        strategy_rows,
            width="stretch",
        hide_index=True
    )

    personality = data.get(
        "brand_personality",
        {}
    )

    st.markdown("### Personality")

    render_badges(
        personality.get(
            "traits",
            []
        )
    )

    st.markdown("### Traits to Avoid")

    render_badges(
        personality.get(
            "traits_to_avoid",
            []
        )
    )

    voice = data.get(
        "brand_voice",
        {}
    )

    st.markdown("### Brand Voice")

    col1, col2 = st.columns(2)

    with col1:

        metric_card(
            "Tone",
            voice.get(
                "tone"
            )
        )

    with col2:

        metric_card(
            "Communication Style",
            voice.get(
                "communication_style"
            )
        )

    st.markdown("### Words to Use")

    render_badges(
        voice.get(
            "words_to_use",
            []
        )
    )

    st.markdown("### Words to Avoid")

    render_badges(
        voice.get(
            "words_to_avoid",
            []
        )
    )

    messaging = data.get(
        "final_messaging",
        {}
    )

    st.markdown("### 📣 Final Messaging")

    messaging_rows = [
        {
            "Type": "Primary",
            "Message": messaging.get(
                "primary",
                "—"
            )
        },
        {
            "Type": "Support 1",
            "Message": messaging.get(
                "support_1",
                "—"
            )
        },
        {
            "Type": "Support 2",
            "Message": messaging.get(
                "support_2",
                "—"
            )
        },
        {
            "Type": "Support 3",
            "Message": messaging.get(
                "support_3",
                "—"
            )
        },
        {
            "Type": "Tagline",
            "Message": messaging.get(
                "tagline",
                "—"
            )
        },
        {
            "Type": "CTA",
            "Message": messaging.get(
                "cta",
                "—"
            )
        }
    ]

    st.dataframe(
        messaging_rows,
            width="stretch",
        hide_index=True
    )

    visual = data.get(
        "visual_brand_kit",
        {}
    )

    st.markdown("### 🎨 Visual Brand Kit")

    color_items = [
        (
            "Primary",
            visual.get(
                "primary_color",
                "#004E92"
            )
        ),
        (
            "Secondary",
            visual.get(
                "secondary_color",
                "#009688"
            )
        ),
        (
            "Accent",
            visual.get(
                "accent_color",
                "#FF9800"
            )
        ),
        (
            "Background",
            visual.get(
                "background_color",
                "#FFFFFF"
            )
        ),
        (
            "Text",
            visual.get(
                "text_color",
                "#333333"
            )
        )
    ]

    columns = st.columns(
        len(color_items)
    )

    for column, (
        label,
        color_code
    ) in zip(
        columns,
        color_items
    ):

        with column:

            st.markdown(
                f"""
                <div
                    class="swatch"
                    style="background:{html.escape(str(color_code))};"
                ></div>

                <div class="swatch-label">
                    {html.escape(label)}
                </div>

                <div class="swatch-code">
                    {html.escape(str(color_code))}
                </div>
                """,
                unsafe_allow_html=True
            )

    visual_rows = [
        {
            "Element": "Logo",
            "Direction": visual.get(
                "logo",
                "—"
            )
        },
        {
            "Element": "Heading Typography",
            "Direction": visual.get(
                "typography_heading",
                "—"
            )
        },
        {
            "Element": "Body Typography",
            "Direction": visual.get(
                "typography_body",
                "—"
            )
        },
        {
            "Element": "Graphics",
            "Direction": visual.get(
                "graphics",
                "—"
            )
        },
        {
            "Element": "Imagery",
            "Direction": visual.get(
                "imagery",
                "—"
            )
        }
    ]

    st.dataframe(
        visual_rows,
            width="stretch",
        hide_index=True
    )

    assets = data.get(
        "launch_assets",
        {}
    )

    st.markdown("### 🚀 Launch Assets")

    asset_rows = [
        {
            "Asset": "Landing Headline",
            "Content": assets.get(
                "landing_headline",
                "—"
            )
        },
        {
            "Asset": "Landing Subheadline",
            "Content": assets.get(
                "landing_subheadline",
                "—"
            )
        },
        {
            "Asset": "Landing CTA",
            "Content": assets.get(
                "landing_cta",
                "—"
            )
        },
        {
            "Asset": "Product Description",
            "Content": assets.get(
                "product_description",
                "—"
            )
        }
    ]

    st.dataframe(
        asset_rows,
            width="stretch",
        hide_index=True
    )

    st.markdown("### LinkedIn Post")

    st.info(
        safe(
            assets.get(
                "linkedin_post"
            )
        )
    )

    st.markdown("### Instagram Caption")

    st.info(
        safe(
            assets.get(
                "instagram_caption"
            )
        )
    )

    # --------------------------------------------------------
    # CONSISTENCY GUARDIAN
    # --------------------------------------------------------

    st.markdown("## 🛡️ Consistency Guardian")

    consistency = data.get(
        "consistency_guardian",
        {}
    )

    consistency_rows = []

    consistency_items = [
        (
            "Positioning vs Personality",
            consistency.get(
                "positioning_vs_personality",
                {}
            )
        ),
        (
            "Positioning vs Voice",
            consistency.get(
                "positioning_vs_voice",
                {}
            )
        ),
        (
            "Positioning vs Visuals",
            consistency.get(
                "positioning_vs_visuals",
                {}
            )
        ),
        (
            "Positioning vs Tagline",
            consistency.get(
                "positioning_vs_tagline",
                {}
            )
        ),
        (
            "Positioning vs Launch Message",
            consistency.get(
                "positioning_vs_launch_message",
                {}
            )
        )
    ]

    for label, item in consistency_items:

        consistency_rows.append(
            {
                "Check": label,
                "Status": item.get(
                    "status",
                    "Needs Review"
                ),
                "Reason": item.get(
                    "reason",
                    "—"
                )
            }
        )

    st.dataframe(
        consistency_rows,
            width="stretch",
        hide_index=True
    )

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    summary = data.get(
        "final_summary",
        {}
    )

    st.markdown("## Final Brand Board")

    st.markdown(
        """
        <div class="final-board">
        """,
        unsafe_allow_html=True
    )

    summary_rows = [
        {
            "Decision": "WHO",
            "Answer": summary.get(
                "who",
                "—"
            )
        },
        {
            "Decision": "PROBLEM",
            "Answer": summary.get(
                "problem",
                "—"
            )
        },
        {
            "Decision": "PROMISE",
            "Answer": summary.get(
                "promise",
                "—"
            )
        },
        {
            "Decision": "DIFFERENTIATOR",
            "Answer": summary.get(
                "differentiator",
                "—"
            )
        },
        {
            "Decision": "PERSONALITY",
            "Answer": summary.get(
                "personality",
                "—"
            )
        },
        {
            "Decision": "VOICE",
            "Answer": summary.get(
                "voice",
                "—"
            )
        },
        {
            "Decision": "VISUAL",
            "Answer": summary.get(
                "visual",
                "—"
            )
        }
    ]

    st.dataframe(
        summary_rows,
        width="stretch",
        hide_index=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# PDF GENERATION
# ============================================================

def create_brand_pdf(
    discover,
    position,
    shape,
    challenge,
    visualize,
    deliver
):

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=24,
        leading=30,
        spaceAfter=15
    )

    stage_style = ParagraphStyle(
        "Stage",
        parent=styles["Heading1"],
        fontSize=17,
        leading=22,
        spaceBefore=15,
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=12,
        spaceAfter=4
    )

    story = []

    story.append(
        Paragraph(
            "BrandForge AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Launch-Ready Brand System",
            body_style
        )
    )

    story.append(
        Paragraph(
            "Discover → Position → Shape → Challenge → "
            "Visualize → Deliver",
            body_style
        )
    )

    def add_section(
        title,
        value
    ):

        story.append(
            Paragraph(
                html.escape(title),
                heading_style
            )
        )

        if isinstance(
            value,
            list
        ):

            for item in value:

                if isinstance(
                    item,
                    dict
                ):

                    text = " | ".join(
                        f"{key}: {val}"
                        for key, val in item.items()
                    )

                else:

                    text = str(item)

                story.append(
                    Paragraph(
                        html.escape(text),
                        body_style
                    )
                )

        elif isinstance(
            value,
            dict
        ):

            for key, val in value.items():

                if isinstance(
                    val,
                    list
                ):

                    val = ", ".join(
                        str(x)
                        for x in val
                    )

                elif isinstance(
                    val,
                    dict
                ):

                    val = str(val)

                story.append(
                    Paragraph(
                        f"<b>{html.escape(str(key))}:</b> "
                        f"{html.escape(str(val))}",
                        body_style
                    )
                )

        else:

            story.append(
                Paragraph(
                    html.escape(
                        safe(value)
                    ),
                    body_style
                )
            )

    # --------------------------------------------------------
    # DISCOVER
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "1. DISCOVER",
            stage_style
        )
    )

    add_section(
        "Core Problem",
        discover.get("core_problem")
    )

    add_section(
        "Target User",
        discover.get("target_user")
    )

    add_section(
        "Pain Points",
        discover.get("pain_points")
    )

    add_section(
        "Context",
        discover.get("context")
    )

    add_section(
        "Potential Value",
        discover.get("potential_value")
    )

    add_section(
        "Constraints",
        discover.get("constraints")
    )

    add_section(
        "Unanswered Questions",
        discover.get("unanswered_questions")
    )

    add_section(
        "Discovery Insight",
        discover.get("discovery_insight")
    )

    # --------------------------------------------------------
    # POSITION
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "2. POSITION",
            stage_style
        )
    )

    for key in [
        "product_category",
        "primary_audience",
        "value_proposition",
        "differentiator",
        "competitive_angle",
        "positioning_statement",
        "positioning_risks",
        "assumptions"
    ]:

        add_section(
            key.replace(
                "_",
                " "
            ).title(),
            position.get(key)
        )

    # --------------------------------------------------------
    # SHAPE
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "3. SHAPE",
            stage_style
        )
    )

    for key, value in shape.items():

        add_section(
            key.replace(
                "_",
                " "
            ).title(),
            value
        )

    # --------------------------------------------------------
    # CHALLENGE
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "4. CHALLENGE",
            stage_style
        )
    )

    for key, value in challenge.items():

        add_section(
            key.replace(
                "_",
                " "
            ).title(),
            value
        )

    # --------------------------------------------------------
    # VISUALIZE
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "5. VISUALIZE",
            stage_style
        )
    )

    for key, value in visualize.items():

        add_section(
            key.replace(
                "_",
                " "
            ).title(),
            value
        )

    # --------------------------------------------------------
    # DELIVER
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "6. DELIVER",
            stage_style
        )
    )

    for key, value in deliver.items():

        add_section(
            key.replace(
                "_",
                " "
            ).title(),
            value
        )

    document.build(story)

    buffer.seek(0)

    return buffer


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">✦ BrandForge AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Turn a rough startup idea into a coherent,
        launch-ready brand system using an AI reasoning workflow.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="workflow">
        🔎 Discover
        &nbsp;→&nbsp;
        🎯 Position
        &nbsp;→&nbsp;
        ✨ Shape
        &nbsp;→&nbsp;
        ⚔️ Challenge
        &nbsp;→&nbsp;
        🎨 Visualize
        &nbsp;→&nbsp;
        🚀 Deliver
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INPUT
# ============================================================

st.markdown("## Start with your idea")

execution_mode = st.radio(
    "Execution Mode",
    ["AI Mode", "Demo Mode"],
    index=0,
    horizontal=True,
    key="brandforge_execution_mode"
)

if execution_mode == "Demo Mode":
    st.info("DEMO MODE — SAMPLE AI WORKFLOW OUTPUT")

if st.session_state.get("brandforge_mode") != execution_mode:
    st.session_state["brandforge_mode"] = execution_mode
    clear_workflow_state()

idea = st.text_area(
    "What is your rough idea?",
    placeholder=(
        "Example: I want to create an app "
        "that helps students find teammates."
    ),
    height=150
)

additional_context = st.text_area(
    "Anything else you already know? (Optional)",
    placeholder=(
        "Example: It may be useful for college "
        "students and hackathons."
    ),
    height=100
)


# ============================================================
# GENERATE
# ============================================================

retry_stage = st.session_state.get("failed_stage")
button_label = (
    f"↻ Retry {retry_stage}"
    if retry_stage
    else "✦ Generate Brand System"
)

if st.button(
    button_label,
    type="primary",
    width="stretch",
    key="brandforge_run_workflow"
):

    if execution_mode == "AI Mode" and not idea.strip():

        st.warning(
            "Please enter your rough idea first."
        )

        st.stop()

    workflow_idea = (
        idea
        if execution_mode == "AI Mode"
        else DEMO_IDEA
    )
    workflow_context = (
        additional_context
        if execution_mode == "AI Mode"
        else DEMO_CONTEXT
    )

    input_signature = (
        execution_mode,
        workflow_idea.strip(),
        workflow_context.strip()
    )

    if st.session_state.get("brandforge_input") != input_signature:
        st.session_state["brandforge_input"] = input_signature
        clear_workflow_state()

    results = st.session_state.setdefault(
        "brandforge_results",
        {}
    )

    if execution_mode == "Demo Mode":
        demo_results = get_demo_workflow()

        for stage_name, result in demo_results.items():
            save_stage_result(
                stage_name,
                result,
                results
            )

        st.session_state.pop("failed_stage", None)

    st.session_state.pop(
        "workflow_error",
        None
    )

    current_stage = "Discover"

    try:

        # ----------------------------------------------------
        # DISCOVER
        # ----------------------------------------------------

        current_stage = "Discover"

        if "discover" in results:
            discover = results["discover"]
        else:
            with st.spinner(
                "1/6 Discovering the core problem..."
            ):
                discover = run_discover(
                    workflow_idea,
                    workflow_context
                )

            save_stage_result(
                "discover",
                discover,
                results
            )

        st.divider()
        render_discover(discover)

        # ----------------------------------------------------
        # POSITION
        # ----------------------------------------------------

        current_stage = "Position"

        if "position" in results:
            position = results["position"]
        else:
            with st.spinner(
                "2/6 Building product positioning..."
            ):
                position = run_position(discover)

            save_stage_result(
                "position",
                position,
                results
            )

        st.divider()
        render_position(position)

        # ----------------------------------------------------
        # SHAPE
        # ----------------------------------------------------

        current_stage = "Shape"

        if "shape" in results:
            shape = results["shape"]
        else:
            with st.spinner(
                "3/6 Shaping the brand..."
            ):
                shape = run_shape(
                    discover,
                    position
                )

            save_stage_result(
                "shape",
                shape,
                results
            )

        st.divider()
        render_shape(shape)

        # ----------------------------------------------------
        # CHALLENGE
        # ----------------------------------------------------

        current_stage = "Challenge"

        if "challenge" in results:
            challenge = results["challenge"]
        else:
            with st.spinner(
                "4/6 Challenging assumptions and claims..."
            ):
                challenge = run_challenge(
                    position,
                    shape
                )

            save_stage_result(
                "challenge",
                challenge,
                results
            )

        st.divider()
        render_challenge(challenge)

        # ----------------------------------------------------
        # VISUALIZE
        # ----------------------------------------------------

        current_stage = "Visualize"

        if "visualize" in results:
            visualize = results["visualize"]
        else:
            with st.spinner(
                "5/6 Creating the visual identity..."
            ):
                visualize = run_visualize(challenge)

            save_stage_result(
                "visualize",
                visualize,
                results
            )

        st.divider()
        render_visualize(visualize)

        # ----------------------------------------------------
        # DELIVER
        # ----------------------------------------------------

        current_stage = "Deliver"

        if "deliver" in results:
            deliver = results["deliver"]
        else:
            with st.spinner(
                "6/6 Building the final brand system..."
            ):
                deliver = run_deliver(
                    challenge,
                    visualize
                )

            save_stage_result(
                "deliver",
                deliver,
                results
            )

        st.divider()
        render_deliver(deliver)

        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        pdf_buffer = create_brand_pdf(
            discover=discover,
            position=position,
            shape=shape,
            challenge=challenge,
            visualize=visualize,
            deliver=deliver
        )

        st.divider()

        st.success(
            "Your structured launch-ready brand system is ready."
        )

        st.download_button(
            label="📄 Download Complete Brand Kit PDF",
            data=pdf_buffer,
            file_name="BrandForge_Complete_Brand_Kit.pdf",
            mime="application/pdf",
            type="primary",
            width="stretch"
        )

        st.session_state.pop(
            "failed_stage",
            None
        )
        st.session_state.pop(
            "workflow_error",
            None
        )

    except Exception as e:

        error_summary = describe_workflow_error(e)
        print(
            f"BrandForge {current_stage} failure: "
            f"{type(e).__name__}: {e}"
        )
        traceback.print_exc()

        if error_summary == "The stage returned an unexpected error. Please retry this stage.":
            error_summary = (
                f"{type(e).__name__}: {str(e)[:300]}"
            )

        st.session_state["failed_stage"] = current_stage
        st.session_state["workflow_error"] = error_summary

        st.error("Workflow stopped")
        st.markdown(
            f"**Stage:** {current_stage.upper()}"
        )
        st.markdown(
            f"**Reason:** {error_summary}"
        )
        st.info(
            "Your completed stages are preserved. "
            f"Use the Retry {current_stage} button to continue."
        )