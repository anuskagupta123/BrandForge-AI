"""Deterministic sample data for demonstrating the BrandForge workflow."""

from copy import deepcopy


DEMO_IDEA = (
    "I want to create an app that helps students find suitable teammates "
    "for group projects."
)

DEMO_CONTEXT = (
    "Designed for college students who struggle to find compatible teammates "
    "based on skills, interests, availability and project needs."
)


_DEMO_WORKFLOW = {
    "discover": {
        "core_problem": "Students struggle to find suitable teammates for group projects.",
        "target_user": "College students working on academic group projects.",
        "pain_points": [
            {
                "title": "Difficulty finding compatible teammates",
                "impact": "High",
                "description": "Students may know many classmates but still struggle to identify compatible teammates."
            },
            {
                "title": "Unclear skill compatibility",
                "impact": "Medium",
                "description": "Students may not know which classmates have complementary skills."
            },
            {
                "title": "Availability conflicts",
                "impact": "Medium",
                "description": "Potential teammates may have conflicting schedules."
            }
        ],
        "context": "College project and assignment periods.",
        "potential_value": [
            "Make teammate discovery easier.",
            "Surface complementary skills.",
            "Consider project requirements.",
            "Reduce manual searching."
        ],
        "constraints": [
            "Students must provide enough information for useful matching.",
            "Participation should remain voluntary.",
            "Privacy expectations must be considered.",
            "Matching should avoid unsupported claims.",
            "The product should remain easy to use."
        ],
        "unanswered_questions": [
            "What information will students be comfortable sharing?",
            "How should availability be represented?",
            "How should students control who can contact them?",
            "How should matching quality be evaluated?",
            "What happens when no suitable teammate is found?"
        ],
        "discovery_insight": "The product should help students make informed teammate choices rather than simply producing automatic matches."
    },
    "position": {
        "product_category": "Student team-matching platform",
        "primary_audience": "College students working on group projects",
        "value_proposition": "Help students discover potential teammates using project needs, complementary skills and availability.",
        "differentiator": [
            "Project-aware teammate discovery",
            "Focus on complementary team composition"
        ],
        "competitive_angle": "Position around thoughtful team formation rather than generic social networking.",
        "positioning_statement": "A project-focused platform that helps students discover potential teammates based on complementary needs and preferences.",
        "positioning_risks": [
            {
                "risk": "Assuming students will share detailed information",
                "severity": "High",
                "description": "The product depends on voluntary user information."
            },
            {
                "risk": "Overpromising match quality",
                "severity": "Medium",
                "description": "Matching quality cannot be guaranteed without evidence."
            }
        ],
        "assumptions": [
            "Students experience difficulty forming project teams.",
            "Some students are willing to provide matching information.",
            "Project requirements can be represented in a structured way."
        ]
    },
    "shape": {
        "brand_personality": [
            "Reliable",
            "Approachable",
            "Insightful",
            "Collaborative"
        ],
        "traits_to_avoid": [
            "Overly technical",
            "Aggressive",
            "Overpromising",
            "Impersonal"
        ],
        "naming_territories": [
            {
                "territory": "Collaboration",
                "description": "Names suggesting teamwork and shared progress.",
                "name_concepts": ["CollabSync", "TeamMingle"]
            },
            {
                "territory": "Matching",
                "description": "Names suggesting thoughtful teammate discovery.",
                "name_concepts": ["PairWise", "SkillSet"]
            },
            {
                "territory": "Accountability",
                "description": "Names suggesting dependable project partnerships.",
                "name_concepts": ["CommitMate", "CohortTrack"]
            }
        ],
        "tagline_directions": [
            "Find teammates who complement your project.",
            "Build better teams for your next project.",
            "Turn project needs into potential teammates."
        ],
        "brand_voice": [
            {
                "trait": "Clear and concise",
                "description": "Use direct language and avoid jargon."
            },
            {
                "trait": "Empathetic",
                "description": "Recognize the uncertainty students face when forming teams."
            },
            {
                "trait": "Action-oriented",
                "description": "Encourage students to take practical next steps."
            }
        ],
        "message_hierarchy": {
            "primary": "Find potential teammates who complement your project needs.",
            "support_1": "Explore skills and preferences that may fit your project.",
            "support_2": "Make teammate discovery more structured and transparent."
        }
    },
    "challenge": {
        "problems": [
            {
                "problem": "The promise could imply guaranteed matching quality.",
                "severity": "High",
                "why_it_matters": "The product has no evidence proving successful matches.",
                "correction": "Use language such as potential teammates or compatible options."
            },
            {
                "problem": "Instant matching language may overpromise speed.",
                "severity": "Medium",
                "why_it_matters": "Actual matching speed depends on available information.",
                "correction": "Use discovery-focused language instead."
            },
            {
                "problem": "Privacy-first wording could become an unsupported claim.",
                "severity": "Medium",
                "why_it_matters": "Privacy claims require implemented controls and evidence.",
                "correction": "Describe specific privacy controls only when implemented."
            }
        ],
        "generic_language": [
            "Build better teams",
            "Seamless experience",
            "AI-powered matching",
            "Find the perfect teammate"
        ],
        "unsupported_claims": [
            "Guaranteed perfect matches",
            "Proven project success",
            "Only privacy-first platform"
        ],
        "audience_positioning_risks": [
            "Students may hesitate to share personal information.",
            "Different courses may require different team structures.",
            "Some students may prefer existing teammates."
        ],
        "final_corrections": {
            "positioning": "Focus on structured teammate discovery rather than guaranteed outcomes.",
            "personality": "Keep the brand approachable and trustworthy.",
            "naming": "Prefer collaborative and project-oriented naming territories.",
            "tagline": "Avoid promises of perfect or instant matching.",
            "messaging": "Describe potential value without unsupported outcome claims."
        },
        "final_decisions": {
            "audience": "College students working on group projects.",
            "problem": "Students need a structured way to discover potential teammates.",
            "promise": "Help students explore potential teammates based on project needs and preferences.",
            "differentiator": "Project-aware teammate discovery.",
            "naming_direction": "Collaborative, approachable names focused on team formation.",
            "tagline_direction": "Clear language about finding complementary teammates.",
            "voice": ["Clear", "Empathetic", "Action-oriented"]
        }
    },
    "visualize": {
        "visual_concept": "A clean, approachable identity built around student connections and shared project progress.",
        "logo_direction": "Use a simple network of connected nodes that suggests teammates forming a project group.",
        "colors": {
            "primary": "#2563EB",
            "secondary": "#14B8A6",
            "accent": "#F59E0B",
            "background": "#FFFFFF",
            "text": "#111827"
        },
        "typography": {
            "heading": "Poppins SemiBold",
            "body": "Inter Regular"
        },
        "graphic_language": "Simple connection patterns, rounded nodes and clear project pathways.",
        "imagery": "Diverse student collaboration, project planning and teamwork.",
        "ui_direction": [
            "Clear project profiles",
            "Visible skill relationships",
            "Approachable connection cues",
            "Calm collaboration surfaces"
        ],
        "avoid": [
            "Cluttered layouts",
            "Overly dark palettes",
            "Corporate stock-photo appearance"
        ],
        "visual_rationale": "The system makes collaboration feel approachable while keeping project information easy to scan."
    },
    "deliver": {
        "brand_foundation": {
            "brand_name": "PairWise",
            "category": "Student team-matching platform",
            "core_problem": "Students struggle to find suitable teammates for group projects.",
            "target_audience": "College students working on academic group projects.",
            "value_proposition": "Help students discover potential teammates using project needs, complementary skills and availability.",
            "differentiator": "Project-aware teammate discovery.",
            "positioning_statement": "A project-focused platform that helps students discover potential teammates based on complementary needs and preferences."
        },
        "brand_personality": {
            "traits": ["Reliable", "Approachable", "Insightful", "Collaborative"],
            "traits_to_avoid": ["Overly technical", "Aggressive", "Overpromising", "Impersonal"]
        },
        "brand_voice": {
            "tone": "Clear, empathetic and action-oriented",
            "communication_style": "Direct language that recognizes student uncertainty.",
            "words_to_use": ["potential", "complementary", "project", "explore"],
            "words_to_avoid": ["guaranteed", "perfect", "proven", "only"]
        },
        "final_messaging": {
            "primary": "Find potential teammates who complement your project needs.",
            "support_1": "Explore skills and preferences that may fit your project.",
            "support_2": "Make teammate discovery more structured and transparent.",
            "support_3": "Start with your project needs and compare potential fits.",
            "tagline": "Find teammates who complement your project.",
            "cta": "Explore potential teammates"
        },
        "visual_brand_kit": {
            "logo": "Connected student nodes forming a simple project group.",
            "primary_color": "#2563EB",
            "secondary_color": "#14B8A6",
            "accent_color": "#F59E0B",
            "background_color": "#FFFFFF",
            "text_color": "#111827",
            "typography_heading": "Poppins SemiBold",
            "typography_body": "Inter Regular",
            "graphics": "Node-based connection patterns and clear project pathways.",
            "imagery": "Diverse student collaboration and project planning."
        },
        "launch_assets": {
            "landing_headline": "Find potential teammates for your next project.",
            "landing_subheadline": "Explore complementary skills, preferences and availability in one place.",
            "landing_cta": "Explore potential teammates",
            "product_description": "PairWise helps students structure teammate discovery around project needs and preferences.",
            "linkedin_post": "Finding a project team can be difficult even when classmates are nearby. PairWise offers a clearer way to explore potential teammate fits.",
            "instagram_caption": "Your next project team may start with the right questions. Explore potential teammate fits with PairWise."
        },
        "consistency_guardian": {
            "positioning_vs_personality": {"status": "Aligned", "reason": "Approachable and reliable traits support structured discovery."},
            "positioning_vs_voice": {"status": "Aligned", "reason": "Clear language supports careful, non-overclaiming positioning."},
            "positioning_vs_visuals": {"status": "Aligned", "reason": "Connection graphics reinforce project-aware discovery."},
            "positioning_vs_tagline": {"status": "Aligned", "reason": "The tagline describes complementary teammates without guarantees."},
            "positioning_vs_launch_message": {"status": "Aligned", "reason": "Launch copy presents exploration rather than promised outcomes."}
        },
        "final_summary": {
            "who": "College students working on group projects.",
            "problem": "Students need a structured way to discover potential teammates.",
            "promise": "Help students explore potential teammates based on project needs and preferences.",
            "differentiator": "Project-aware teammate discovery.",
            "personality": "Reliable, approachable, insightful and collaborative.",
            "voice": "Clear, empathetic and action-oriented.",
            "visual": "Clean connection patterns with approachable student collaboration imagery."
        }
    }
}


def get_demo_workflow():
    """Return an isolated copy so demo output cannot mutate between runs."""

    return deepcopy(_DEMO_WORKFLOW)
