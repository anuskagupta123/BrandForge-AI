# ============================================================
# BRANDFORGE AI - STRUCTURED PROMPTS
# ============================================================
#
# Every prompt asks the AI to return JSON.
# This allows app.py to render the result as:
# - Tables
# - Cards
# - Badges
# - Risk indicators
# - Color swatches
# - Brand boards
# - Structured launch assets
#
# ============================================================


# ============================================================
# DISCOVER
# ============================================================

def discover_prompt(
    idea,
    additional_context
):

    return f"""
You are the DISCOVER stage of BrandForge AI.

Your job is to understand the founder's rough idea before branding.

ROUGH IDEA:
{idea}

ADDITIONAL CONTEXT:
{additional_context}

Return ONLY valid JSON. No Markdown. No explanation. Use exactly these keys:

{{
  "core_problem": "Short description of the main problem.",

  "target_user": "Short description of the primary user.",

  "pain_points": [
    {{
      "title": "Short pain point",
      "impact": "High",
      "description": "Short explanation."
    }},
    {{
      "title": "Short pain point",
      "impact": "Medium",
      "description": "Short explanation."
    }},
    {{
      "title": "Short pain point",
      "impact": "Medium",
      "description": "Short explanation."
    }}
  ],

  "context": "Short description of where and when this problem occurs.",

  "potential_value": [
    "Short potential value 1",
    "Short potential value 2",
    "Short potential value 3",
    "Short potential value 4"
  ],

  "constraints": [
    "Constraint 1",
    "Constraint 2",
    "Constraint 3",
    "Constraint 4",
    "Constraint 5"
  ],

  "unanswered_questions": [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4",
    "Question 5"
  ],

  "discovery_insight": "One concise strategic insight."
}}

RULES:

- Return only one complete JSON object.
- Do not use Markdown or code fences.
- Every value must be a string, an array of strings, or a pain-point object as shown.
- Do not create brand names.
- Do not create logos.
- Do not create taglines.
- Do not invent statistics.
- Do not invent customer research.
- Do not invent pilot results.
- Do not claim features that the founder did not provide.
- Clearly treat uncertain information as assumptions.
- Keep every value concise.
- Pain point impact must be High, Medium, or Low.
"""


def discover_retry_prompt(
    idea,
    additional_context
):

    return f"""
You are retrying the DISCOVER stage because the previous response was not
valid complete JSON.

ROUGH IDEA:
{idea}

ADDITIONAL CONTEXT:
{additional_context}

Return ONLY one complete JSON object. No Markdown, code fences,
explanation, or text before or after the object. Use exactly these keys:

{{
  "core_problem": "",
  "target_user": "",
  "pain_points": [
    {{"title": "", "impact": "High", "description": ""}}
  ],
  "context": "",
  "potential_value": [],
  "constraints": [],
  "unanswered_questions": [],
  "discovery_insight": ""
}}

Keep values concise. Arrays contain strings. Pain-point impact must be
High, Medium, or Low. Complete every brace before stopping. Do not invent
statistics, research, pilot results, features, brands, logos, or taglines.
"""


# ============================================================
# POSITION
# ============================================================

def position_prompt(
    discover_result
):

    return f"""
You are the POSITION stage of BrandForge AI.

Build the product positioning using the Discover result.

DISCOVER RESULT:
{discover_result}

Return ONLY valid JSON. No Markdown. No explanation.
Use exactly these keys and keep every value concise:

{{
  "product_category": "Short category.",

  "primary_audience": "Short description of the primary audience.",

  "value_proposition": "One concise value proposition.",

  "differentiator": [
    "Differentiator 1",
    "Differentiator 2"
  ],

  "competitive_angle": "Short comparison with the existing way users solve the problem.",

  "positioning_statement": "For [audience], [product] helps [solve problem] by [value/differentiator].",

  "positioning_risks": [
    {{
      "risk": "Risk 1",
      "severity": "High",
      "description": "Short explanation."
    }},
    {{
      "risk": "Risk 2",
      "severity": "Medium",
      "description": "Short explanation."
    }},
    {{
      "risk": "Risk 3",
      "severity": "Medium",
      "description": "Short explanation."
    }}
  ],

  "assumptions": [
    "Assumption 1",
    "Assumption 2",
    "Assumption 3"
  ]
}}

RULES:

- Return ONLY JSON.
- Do not use markdown.
- Do not use ```json.
- Build on Discover.
- Do not restart the analysis.
- Do not invent competitors.
- Do not invent market research.
- Do not invent statistics.
- Do not invent customer research.
- Do not make trademark claims.
- Do not claim unimplemented features.
- Mark uncertain points as assumptions.
- Keep responses concise.
- Severity must be High, Medium, or Low.
"""


def position_retry_prompt(
    discover_result
):

    return f"""
You are retrying the POSITION stage because the previous response was not
valid complete JSON.

DISCOVER RESULT:
{discover_result}

Return ONLY one complete JSON object. No Markdown, code fences,
explanation, or text before or after the object. Use exactly these keys:

{{
  "product_category": "",
  "primary_audience": "",
  "value_proposition": "",
  "differentiator": [],
  "competitive_angle": "",
  "positioning_statement": "",
  "positioning_risks": [
    {{"risk": "", "severity": "Medium", "description": ""}}
  ],
  "assumptions": []
}}

All arrays contain strings except positioning_risks, which contains the
shown objects. Severity must be High, Medium, or Low. Keep every value
short. Do not invent competitors, research, statistics, legal claims,
trademark claims, or unimplemented features. Complete every brace.
"""


# ============================================================
# SHAPE
# ============================================================

def shape_prompt(
    discover_result,
    position_result
):

    return f"""
You are the SHAPE stage of BrandForge AI.

Create a concise proposed brand personality, naming directions,
voice and messaging.

DISCOVER RESULT:
{discover_result}

POSITION RESULT:
{position_result}

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
  "brand_personality": [
    "Reliable",
    "Insightful",
    "Community-focused",
    "Efficient"
  ],

  "traits_to_avoid": [
    "Overly technical",
    "Overpromising",
    "Aggressive",
    "Unpersonalized"
  ],

  "naming_territories": [
    {{
      "territory": "Collaboration",
      "description": "Short description.",
      "name_concepts": [
        "Name 1",
        "Name 2"
      ]
    }},
    {{
      "territory": "Matching",
      "description": "Short description.",
      "name_concepts": [
        "Name 1",
        "Name 2"
      ]
    }},
    {{
      "territory": "Accountability",
      "description": "Short description.",
      "name_concepts": [
        "Name 1",
        "Name 2"
      ]
    }}
  ],

  "tagline_directions": [
    "Tagline direction 1",
    "Tagline direction 2",
    "Tagline direction 3"
  ],

  "brand_voice": [
    {{
      "trait": "Clear and concise",
      "description": "Short explanation."
    }},
    {{
      "trait": "Empathetic",
      "description": "Short explanation."
    }},
    {{
      "trait": "Action-oriented",
      "description": "Short explanation."
    }}
  ],

  "message_hierarchy": {{
    "primary": "Primary message.",
    "support_1": "Supporting message.",
    "support_2": "Supporting message."
  }}
}}

RULES:

- Return ONLY JSON.
- Do not use markdown.
- Do not use ```json.
- Mark proposed names and messaging as PROPOSED conceptually.
- Do not claim trademark availability.
- Do not invent statistics.
- Do not invent customer research.
- Do not invent pilot results.
- Do not claim features that have not been provided by the founder.
- Avoid generic startup language.
- Keep everything concise.
- Use short strings and complete the JSON object.
"""


def shape_retry_prompt(
    discover_result,
    position_result
):

    return f"""
You are retrying the SHAPE stage because the previous response was not
valid complete JSON.

DISCOVER RESULT:
{discover_result}

POSITION RESULT:
{position_result}

Return ONLY one complete JSON object. Do not add Markdown, code fences,
explanations, or text before or after the object. Use exactly these keys:

{{
  "brand_personality": [],
  "traits_to_avoid": [],
  "naming_territories": [
    {{"territory": "", "description": "", "name_concepts": []}}
  ],
  "tagline_directions": [],
  "brand_voice": [
    {{"trait": "", "description": ""}}
  ],
  "message_hierarchy": {{
    "primary": "",
    "support_1": "",
    "support_2": ""
  }}
}}

Keep values concise. Treat names and messaging as proposed. Do not invent
statistics, research, pilot results, legal claims, trademark claims, or
unimplemented features. Complete every brace before stopping.
"""


# ============================================================
# CHALLENGE
# ============================================================

def challenge_prompt(
    position_result,
    shape_result
):

    return f"""
You are the CHALLENGE stage of BrandForge AI.

Your job is to critically examine the positioning and brand shape.

Find:
- weak assumptions
- generic language
- unsupported claims
- audience risks
- positioning contradictions
- messaging problems

POSITION RESULT:
{position_result}

SHAPE RESULT:
{shape_result}

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
  "problems": [
    {{
      "problem": "Problem 1",
      "severity": "High",
      "why_it_matters": "Short explanation.",
      "correction": "Specific improvement."
    }},
    {{
      "problem": "Problem 2",
      "severity": "High",
      "why_it_matters": "Short explanation.",
      "correction": "Specific improvement."
    }},
    {{
      "problem": "Problem 3",
      "severity": "Medium",
      "why_it_matters": "Short explanation.",
      "correction": "Specific improvement."
    }},
    {{
      "problem": "Problem 4",
      "severity": "Medium",
      "why_it_matters": "Short explanation.",
      "correction": "Specific improvement."
    }},
    {{
      "problem": "Problem 5",
      "severity": "Medium",
      "why_it_matters": "Short explanation.",
      "correction": "Specific improvement."
    }}
  ],

  "generic_language": [
    "Phrase 1",
    "Phrase 2",
    "Phrase 3",
    "Phrase 4",
    "Phrase 5"
  ],

  "unsupported_claims": [
    "Claim 1",
    "Claim 2",
    "Claim 3",
    "Claim 4",
    "Claim 5"
  ],

  "audience_positioning_risks": [
    "Risk 1",
    "Risk 2",
    "Risk 3"
  ],

  "final_corrections": {{
    "positioning": "Corrected positioning direction.",
    "personality": "Corrected personality direction.",
    "naming": "Corrected naming direction.",
    "tagline": "Corrected tagline direction.",
    "messaging": "Corrected messaging direction."
  }},

  "final_decisions": {{
    "audience": "Final target audience.",
    "problem": "Final problem.",
    "promise": "Careful, non-overclaiming promise.",
    "differentiator": "Final differentiator.",
    "personality": [
      "Trait 1",
      "Trait 2",
      "Trait 3"
    ],
    "naming_direction": "Proposed naming direction.",
    "tagline_direction": "Proposed tagline direction.",
    "voice": [
      "Voice trait 1",
      "Voice trait 2",
      "Voice trait 3"
    ]
  }}
}}

RULES:

- Return ONLY JSON.
- Do not use markdown.
- Do not use ```json.
- Be critical.
- Do not restart the strategy.
- Do not invent facts.
- Do not invent statistics.
- Do not invent research.
- Do not invent pilot results.
- Do not make legal claims.
- Do not make trademark claims.
- Do not claim features are implemented unless explicitly provided.
- Do not use "proven", "guaranteed", "best", or "only"
  unless directly supported by the founder.
- Prefer "proposed", "could", "may", or "designed to"
  when evidence is unavailable.
- Severity must be High, Medium, or Low.
- Keep every field concise.
"""


# ============================================================
# VISUALIZE
# ============================================================

def visualize_prompt(
    challenge_result
):

    return f"""
You are the VISUALIZE stage of BrandForge AI.

Create a structured visual identity system using ONLY
the corrected decisions from the Challenge stage.

CHALLENGE RESULT:
{challenge_result}

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
  "visual_concept": "Two concise sentences describing the visual concept.",

  "logo_direction": "Two concise sentences describing the logo direction.",

  "colors": {{
    "primary": "#004E92",
    "secondary": "#009688",
    "accent": "#FF9800",
    "background": "#FFFFFF",
    "text": "#333333"
  }},

  "typography": {{
    "heading": "Font name and weight.",
    "body": "Font name and weight."
  }},

  "graphic_language": "Short description of graphic style.",

  "imagery": "Short description of imagery direction.",

  "ui_direction": [
    "UI direction 1",
    "UI direction 2",
    "UI direction 3",
    "UI direction 4"
  ],

  "avoid": [
    "Visual thing to avoid 1",
    "Visual thing to avoid 2",
    "Visual thing to avoid 3",
    "Visual thing to avoid 4"
  ],

  "visual_rationale": "Two concise sentences explaining why the visual direction supports the brand."
}}

RULES:

- Return ONLY JSON.
- Do not use markdown.
- Do not use ```json.
- Use only decisions supported by Challenge.
- Do not invent research.
- Do not invent statistics.
- Do not claim that colors are scientifically proven.
- Do not claim accessibility compliance.
- Do not claim legal compliance.
- Do not claim product features.
- Use valid HEX colors.
- Keep every field concise.
- Complete every required field.
"""


# ============================================================
# DELIVER
# ============================================================

def deliver_prompt(
    challenge_result,
    visualize_result
):

    return f"""
You are the FINAL DELIVER stage of BrandForge AI.

Create the final structured launch-ready brand system.

Do NOT use old raw Discover, Position or Shape outputs.

Use ONLY:

CHALLENGE RESULT:
{challenge_result}

VISUALIZE RESULT:
{visualize_result}

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
  "brand_foundation": {{
    "brand_name": "Proposed brand name.",
    "category": "Product category.",
    "core_problem": "Core problem.",
    "target_audience": "Target audience.",
    "value_proposition": "Value proposition.",
    "differentiator": "Differentiator.",
    "positioning_statement": "Positioning statement."
  }},

  "brand_personality": {{
    "traits": [
      "Trait 1",
      "Trait 2",
      "Trait 3",
      "Trait 4"
    ],
    "traits_to_avoid": [
      "Trait 1",
      "Trait 2",
      "Trait 3",
      "Trait 4"
    ]
  }},

  "brand_voice": {{
    "tone": "Tone.",
    "communication_style": "Communication style.",
    "words_to_use": [
      "Word 1",
      "Word 2",
      "Word 3",
      "Word 4"
    ],
    "words_to_avoid": [
      "Word 1",
      "Word 2",
      "Word 3",
      "Word 4"
    ]
  }},

  "final_messaging": {{
    "primary": "Primary message.",
    "support_1": "Supporting message.",
    "support_2": "Supporting message.",
    "support_3": "Supporting message.",
    "tagline": "Proposed tagline.",
    "cta": "Proposed CTA."
  }},

  "visual_brand_kit": {{
    "logo": "Logo direction.",
    "primary_color": "#004E92",
    "secondary_color": "#009688",
    "accent_color": "#FF9800",
    "background_color": "#FFFFFF",
    "text_color": "#333333",
    "typography_heading": "Heading font.",
    "typography_body": "Body font.",
    "graphics": "Graphic direction.",
    "imagery": "Imagery direction."
  }},

  "launch_assets": {{
    "landing_headline": "Landing page headline.",
    "landing_subheadline": "Landing page subheadline.",
    "landing_cta": "Landing page CTA.",
    "product_description": "Maximum two sentences.",
    "linkedin_post": "Maximum three sentences.",
    "instagram_caption": "Maximum two sentences."
  }},

  "consistency_guardian": {{
    "positioning_vs_personality": {{
      "status": "Aligned",
      "reason": "Short explanation."
    }},
    "positioning_vs_voice": {{
      "status": "Aligned",
      "reason": "Short explanation."
    }},
    "positioning_vs_visuals": {{
      "status": "Aligned",
      "reason": "Short explanation."
    }},
    "positioning_vs_tagline": {{
      "status": "Aligned",
      "reason": "Short explanation."
    }},
    "positioning_vs_launch_message": {{
      "status": "Aligned",
      "reason": "Short explanation."
    }}
  }},

  "final_summary": {{
    "who": "Who is this for?",
    "problem": "What problem does it address?",
    "promise": "What does it aim to provide?",
    "differentiator": "What makes the concept distinct?",
    "personality": "Brand personality summary.",
    "voice": "Brand voice summary.",
    "visual": "Visual identity summary."
  }}
}}

RULES:

- Return ONLY JSON.
- Do not use markdown.
- Do not use ```json.
- Complete every section.
- Keep every string to 12 words or fewer.
- Keep every array to 3 items unless the structure shows fewer.
- Use short phrases instead of explanatory paragraphs.
- Keep every field concise.
- Do not invent statistics.
- Do not invent research.
- Do not invent pilot results.
- Do not claim unimplemented features.
- Do not claim legal compliance.
- Do not claim trademark availability.
- Do not use "proven", "guaranteed", "best", or "only"
  unless explicitly supported by the founder.
- Use proposed language where validation is unavailable.
- Consistency status must be one of:
  "Aligned"
  "Needs Review"
  "Conflict"
"""