"""
agents/agent4_forum_locator.py
Agent 4 — Forum Locator

Pure rule-based mapping from legal category to the appropriate
authority/forum. No LLM needed — deterministic and fast.
"""

from utils.helper import get_logger

logger = get_logger(__name__)

FORUM_MAP: dict = {
    "labor": {
        "forum": "Labor Commissioner's Office / Industrial Tribunal",
        "how_to_approach": (
            "File a written complaint with the Labor Commissioner in your district. "
            "For claims under Rs 50,000, you can also approach the Labor Court directly. "
            "For PF issues, file a grievance on the EPFO portal (epfindia.gov.in)."
        ),
        "typical_timeline": "Conciliation attempt within 45 days; tribunal hearing if unresolved",
        "cost": "Free — no court fee for labor disputes",
        "official_portal": "https://labour.gov.in",
        "helpline": "1800-11-2526 (EPFO Helpline)",
    },
    "land": {
        "forum": "Civil Court / Rent Authority (if tenancy-related)",
        "how_to_approach": (
            "File a civil suit in the local District Civil Court. "
            "For rent/deposit disputes, first try the Rent Authority under the Model Tenancy Act "
            "if your state has adopted it. Send a legal notice to the landlord first."
        ),
        "typical_timeline": "Rent Authority: 60-90 days; Civil Court: varies (months to years)",
        "cost": "Court fee applies — typically 1-7% of claim value depending on state",
        "official_portal": "https://doj.gov.in",
        "helpline": "District Legal Services Authority (DLSA) — free legal aid",
    },
    "consumer": {
        "forum": "District Consumer Disputes Redressal Commission",
        "how_to_approach": (
            "File online via the e-Daakhil portal (e-daakhil.nic.in) or in person at the "
            "District Consumer Commission. Choose District/State/National based on claim value: "
            "District up to Rs 50 lakhs, State up to Rs 2 crores, National above Rs 2 crores."
        ),
        "typical_timeline": "Legally meant to be resolved within 3-5 months",
        "cost": "Nominal fee — Rs 200 to Rs 2,000 depending on claim value",
        "official_portal": "https://e-daakhil.nic.in",
        "helpline": "1800-11-4000 (National Consumer Helpline)",
    },
    "family": {
        "forum": "Family Court / Magistrate (for DV Act cases)",
        "how_to_approach": (
            "File a petition in the Family Court for maintenance/divorce matters. "
            "For domestic violence, file an application with a Magistrate or approach the "
            "local Protection Officer. Free legal aid is available via DLSA."
        ),
        "typical_timeline": "Interim maintenance orders: within weeks; full case: longer",
        "cost": "Minimal court fee; free legal aid via District Legal Services Authority (DLSA)",
        "official_portal": "https://nalsa.gov.in",
        "helpline": "181 (Women Helpline)",
    },
    "cyber": {
        "forum": "National Cyber Crime Reporting Portal / Local Cyber Cell",
        "how_to_approach": (
            "Report immediately at cybercrime.gov.in or call helpline 1930 for financial fraud "
            "(to attempt transaction freeze — must be done within hours). "
            "Also file a complaint at the nearest Cyber Cell or police station."
        ),
        "typical_timeline": "Immediate for portal reporting; freeze requests need to happen within hours",
        "cost": "Free",
        "official_portal": "https://cybercrime.gov.in",
        "helpline": "1930 (Cyber Crime Helpline)",
    },
    "police": {
        "forum": "Local Police Station / Superintendent of Police",
        "how_to_approach": (
            "Approach the police station with jurisdiction (or file a Zero FIR at any station). "
            "If FIR is refused, escalate in writing to the Superintendent of Police, "
            "or approach a Magistrate under BNSS Section 175(3)."
        ),
        "typical_timeline": "FIR registration is immediate/mandatory by law for cognizable offenses",
        "cost": "Free",
        "official_portal": "https://www.mha.gov.in",
        "helpline": "100 (Police), 112 (Emergency)",
    },
    "other": {
        "forum": "District Legal Services Authority (DLSA)",
        "how_to_approach": (
            "Visit or call your District Legal Services Authority for free preliminary legal "
            "guidance — they can direct you to the correct forum for your specific issue."
        ),
        "typical_timeline": "Varies by issue",
        "cost": "Free legal aid and consultation",
        "official_portal": "https://nalsa.gov.in",
        "helpline": "15100 (NALSA Legal Aid Helpline)",
    },
}


def locate_forum(category: str) -> dict:
    """
    Return forum details for a given legal category.

    Args:
        category: Legal category string from Agent 2.

    Returns:
        Dict with forum name, approach instructions, timeline, cost, portal, and helpline.
    """
    forum = FORUM_MAP.get(category, FORUM_MAP["other"])
    logger.info("Forum for category '%s': %s", category, forum["forum"])
    return forum


# Quick standalone test
if __name__ == "__main__":
    for cat in [*FORUM_MAP.keys(), "unknown_category"]:
        result = locate_forum(cat)
        print(f"\nCategory: {cat}")
        print(f"  Forum: {result['forum']}")
        print(f"  Helpline: {result['helpline']}")
