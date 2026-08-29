from copy import deepcopy
from typing import Dict, List, Optional


# ============================================================
# BLOO COMMERCIAL INTELLIGENCE
# ============================================================
#
# This module deliberately separates:
#
# 1. VERIFIED PUBLIC SIGNALS
# 2. COMMERCIAL HYPOTHESES
# 3. BLOO-COMPUTED SCORES
#
# The Scout Agent should never pretend a hypothesis is a fact.
# In production these records can be populated by live research
# connectors, CRM data, enrichment APIs, and company systems.
# ============================================================


COMMERCIAL_ACCOUNTS: List[Dict] = [
    {
        "id": "target_merit_beauty",
        "company": "MERIT Beauty",
        "industry": "Beauty / DTC",
        "website": "https://www.meritbeauty.com",
        "status": "research_candidate",

        "verified_signals": [
            {
                "type": "business_model",
                "statement": (
                    "MERIT operates a direct-to-consumer beauty "
                    "commerce business alongside retail distribution."
                ),
                "source_type": "public_web",
                "verification_status": "needs_refresh",
            },
            {
                "type": "social_commerce_fit",
                "statement": (
                    "Beauty is a visually driven category where "
                    "creator, social, product-discovery and customer "
                    "conversation signals can influence purchase."
                ),
                "source_type": "category_observation",
                "verification_status": "hypothesis",
            },
        ],

        "commercial_hypothesis": {
            "problem": (
                "High-intent social engagement may contain purchase "
                "signals that are difficult to convert into owned "
                "customer relationships and attributable revenue."
            ),
            "blueberry_wedge": (
                "Turn high-intent social interactions into personalized "
                "1:1 conversations, customer capture and attributable "
                "commerce outcomes."
            ),
            "why_now": (
                "Test whether creator and social engagement can become "
                "a measurable lifecycle and commerce channel."
            ),
        },

        "fit_dimensions": {
            "social_intensity": 19,
            "commerce_fit": 20,
            "personalization_value": 19,
            "lifecycle_value": 18,
            "enterprise_expansion": 18.5,
        },
    },

    {
        "id": "target_glossier",
        "company": "Glossier",
        "industry": "Beauty / DTC",
        "website": "https://www.glossier.com",
        "status": "research_candidate",

        "verified_signals": [
            {
                "type": "business_model",
                "statement": (
                    "Glossier is a consumer beauty brand with "
                    "direct digital commerce and retail presence."
                ),
                "source_type": "public_web",
                "verification_status": "needs_refresh",
            },
            {
                "type": "community_fit",
                "statement": (
                    "The brand has historically emphasized community, "
                    "content and customer participation."
                ),
                "source_type": "public_brand_history",
                "verification_status": "needs_refresh",
            },
        ],

        "commercial_hypothesis": {
            "problem": (
                "Large volumes of community and social engagement may "
                "contain intent that does not automatically become "
                "personalized lifecycle journeys."
            ),
            "blueberry_wedge": (
                "Create individualized conversations from social intent "
                "and connect those conversations to customer identity "
                "and measurable commerce."
            ),
            "why_now": (
                "Evaluate social conversation as an owned customer "
                "acquisition and lifecycle channel."
            ),
        },

        "fit_dimensions": {
            "social_intensity": 19,
            "commerce_fit": 19,
            "personalization_value": 18,
            "lifecycle_value": 19,
            "enterprise_expansion": 18,
        },
    },

    {
        "id": "target_liquid_death",
        "company": "Liquid Death",
        "industry": "Beverage / Consumer",
        "website": "https://liquiddeath.com",
        "status": "research_candidate",

        "verified_signals": [
            {
                "type": "brand_model",
                "statement": (
                    "Liquid Death operates a consumer beverage brand "
                    "with a highly distinctive content-led identity."
                ),
                "source_type": "public_web",
                "verification_status": "needs_refresh",
            },
            {
                "type": "engagement_fit",
                "statement": (
                    "A content-heavy consumer brand can generate large "
                    "volumes of audience interaction that may contain "
                    "different levels of commercial intent."
                ),
                "source_type": "commercial_hypothesis",
                "verification_status": "hypothesis",
            },
        ],

        "commercial_hypothesis": {
            "problem": (
                "High social engagement may be difficult to segment "
                "into actionable purchase intent and owned customer data."
            ),
            "blueberry_wedge": (
                "Identify commercially meaningful interactions and "
                "convert selected engagement into personalized "
                "conversations and measurable customer actions."
            ),
            "why_now": (
                "Test whether an unusually strong social brand can turn "
                "audience participation into attributable commerce."
            ),
        },

        "fit_dimensions": {
            "social_intensity": 20,
            "commerce_fit": 17,
            "personalization_value": 18,
            "lifecycle_value": 17,
            "enterprise_expansion": 18,
        },
    },
]


def _calculate_opportunity_score(account: Dict) -> float:
    """
    Calculate a transparent commercial-fit score.

    Each dimension is intentionally capped at 20.
    Maximum score = 100.

    This is a BLOO-generated prioritization score,
    not a verified company metric.
    """

    dimensions = account.get("fit_dimensions", {})

    score = sum(
        float(value)
        for value in dimensions.values()
    )

    return round(score, 1)


def _count_verified_signals(account: Dict) -> int:
    """
    Count signals currently marked as verified.

    Records marked needs_refresh or hypothesis do not count
    as verified evidence.
    """

    return sum(
        1
        for signal in account.get("verified_signals", [])
        if signal.get("verification_status") == "verified"
    )


def _count_unverified_signals(account: Dict) -> int:
    """
    Count evidence records that still require validation.
    """

    return sum(
        1
        for signal in account.get("verified_signals", [])
        if signal.get("verification_status") != "verified"
    )


def _enrich_account(account: Dict) -> Dict:
    """
    Return an account with BLOO-computed intelligence fields.
    """

    enriched = deepcopy(account)

    enriched["opportunity_score"] = (
        _calculate_opportunity_score(enriched)
    )

    enriched["evidence_summary"] = {
        "verified": _count_verified_signals(enriched),
        "requires_validation": _count_unverified_signals(enriched),
    }

    return enriched


def get_commercial_accounts() -> List[Dict]:
    """
    Return all commercial accounts ranked by opportunity score.
    """

    accounts = [
        _enrich_account(account)
        for account in COMMERCIAL_ACCOUNTS
    ]

    return sorted(
        accounts,
        key=lambda account: account["opportunity_score"],
        reverse=True,
    )


def get_commercial_account(
    account_id: str,
) -> Optional[Dict]:
    """
    Return one commercial account by ID.
    """

    for account in get_commercial_accounts():
        if account["id"] == account_id:
            return account

    return None


def commercial_intelligence_summary() -> Dict:
    """
    Produce a compact system-level summary.
    """

    accounts = get_commercial_accounts()

    if not accounts:
        return {
            "accounts": 0,
            "top_account": None,
            "top_score": None,
            "verified_signals": 0,
            "signals_requiring_validation": 0,
        }

    return {
        "accounts": len(accounts),
        "top_account": accounts[0]["company"],
        "top_score": accounts[0]["opportunity_score"],
        "verified_signals": sum(
            account["evidence_summary"]["verified"]
            for account in accounts
        ),
        "signals_requiring_validation": sum(
            account["evidence_summary"]["requires_validation"]
            for account in accounts
        ),
    }
