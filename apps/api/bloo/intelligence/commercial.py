from copy import deepcopy
from typing import Dict, List, Optional


# ============================================================
# BLOO COMMERCIAL INTELLIGENCE
# ============================================================
#
# Evidence states:
#
# VERIFIED
#   Supported by current public evidence.
#
# NEEDS_VALIDATION
#   Important to the sales motion, but not yet confirmed.
#
# HYPOTHESIS
#   BLOO inference. Never presented as company fact.
#
# opportunity_score is a BLOO prioritisation score,
# not a metric reported by the target company.
# ============================================================


COMMERCIAL_ACCOUNTS: List[Dict] = [

    # ========================================================
    # 1. MERIT BEAUTY
    # ========================================================

    {
        "id": "target_merit_beauty",
        "company": "MERIT Beauty",
        "domain": "meritbeauty.com",
        "industry": "Beauty / DTC",
        "status": "active_research",

        "why_this_account": (
            "MERIT has a dated international retail launch approaching, "
            "strong DTC characteristics, visible social-commerce activity, "
            "and a narrow time window in which Blueberry could help turn "
            "launch attention into identifiable customers and attributable revenue."
        ),

        "verified_signals": [
            {
                "id": "merit_anz_launch",
                "type": "international_expansion",
                "statement": (
                    "MERIT is scheduled to launch in-store and online "
                    "with Sephora Australia and New Zealand on "
                    "September 30, 2026."
                ),
                "published_at": "2026-08-27",
                "source_name": "News.com.au",
                "source_key": "merit_anz_sephora_launch",
                "verification_status": "verified",
                "confidence": 0.99,
            },
            {
                "id": "merit_anz_store_count",
                "type": "retail_expansion",
                "statement": (
                    "The launch is expected to cover 37 Sephora stores "
                    "across Australia and New Zealand, plus Sephora "
                    "web and app channels."
                ),
                "published_at": "2026-08-27",
                "source_name": "News.com.au / Marie Claire Australia",
                "source_key": "merit_anz_37_stores",
                "verification_status": "verified",
                "confidence": 0.99,
            },
            {
                "id": "merit_early_access",
                "type": "campaign_timing",
                "statement": (
                    "Sephora Beauty Pass members are expected to receive "
                    "app-only early access beginning September 28, 2026."
                ),
                "published_at": "2026-08-24",
                "source_name": "Marie Claire Australia",
                "source_key": "merit_sephora_early_access",
                "verification_status": "verified",
                "confidence": 0.98,
            },
            {
                "id": "merit_tiktok_collection",
                "type": "social_commerce",
                "statement": (
                    "MERIT currently maintains a TikTok Bestsellers "
                    "campaign collection on its commerce site."
                ),
                "observed_at": "2026-08-29",
                "source_name": "MERIT Beauty",
                "source_key": "merit_tiktok_bestsellers",
                "verification_status": "verified",
                "confidence": 0.99,
            },
        ],

        "needs_validation": [
            {
                "type": "marketing_stack",
                "question": (
                    "Which lifecycle, CRM, CDP and commerce systems "
                    "currently own MERIT customer identity and activation?"
                ),
            },
            {
                "type": "social_volume",
                "question": (
                    "How much purchase-intent engagement is expected "
                    "around the ANZ Sephora launch?"
                ),
            },
            {
                "type": "buyer",
                "question": (
                    "Who owns social commerce, lifecycle growth and "
                    "ANZ launch performance?"
                ),
            },
            {
                "type": "crm_check",
                "question": (
                    "Is MERIT already present in Blueberry's CRM "
                    "or active pipeline?"
                ),
            },
        ],

        "commercial_hypothesis": {
            "problem": (
                "The September ANZ launch could create a temporary surge "
                "of product questions, comments, influencer engagement "
                "and purchase intent that may not automatically become "
                "known lifecycle customers."
            ),
            "blueberry_wedge": (
                "Use Blueberry around the launch to turn high-intent "
                "social engagement into personalized conversations, "
                "customer capture and attributable commerce."
            ),
            "pilot": (
                "Run a launch-specific social-to-revenue pilot around "
                "the September 28-30 Sephora activation window."
            ),
            "why_now": (
                "There is a specific launch date and therefore a "
                "commercial reason to begin the conversation now."
            ),
            "status": "hypothesis",
        },

        "fit_dimensions": {
            "social_intensity": 19.5,
            "commerce_fit": 20.0,
            "urgency": 20.0,
            "personalization_value": 18.5,
            "expansion_value": 18.0,
        },
    },

    # ========================================================
    # 2. SARAH CREAL BEAUTY
    # ========================================================

    {
        "id": "target_sarah_creal_beauty",
        "company": "Sarah Creal Beauty",
        "domain": "sarahcreal.com",
        "industry": "Beauty / DTC",
        "status": "active_research",

        "why_this_account": (
            "Sarah Creal Beauty combines rapid revenue growth, "
            "retail expansion, international expansion and a highly "
            "specific customer segment. That creates both urgency "
            "and unusually strong personalization potential."
        ),

        "verified_signals": [
            {
                "id": "scb_first_year_revenue",
                "type": "growth",
                "statement": (
                    "Sarah Creal Beauty reportedly generated approximately "
                    "$10 million in turnover during its first year."
                ),
                "published_at": "2026-08-25",
                "source_name": "Financial Times",
                "source_key": "sarah_creal_first_year_turnover",
                "verification_status": "verified",
                "confidence": 0.96,
            },
            {
                "id": "scb_sephora_expansion",
                "type": "retail_expansion",
                "statement": (
                    "The brand has expanded into 102 Sephora stores."
                ),
                "published_at": "2026-08-25",
                "source_name": "Financial Times",
                "source_key": "sarah_creal_sephora_102",
                "verification_status": "verified",
                "confidence": 0.97,
            },
            {
                "id": "scb_uk_launch",
                "type": "international_expansion",
                "statement": (
                    "Sarah Creal Beauty is launching in the UK "
                    "through Space NK."
                ),
                "published_at": "2026-08-25",
                "source_name": "Financial Times",
                "source_key": "sarah_creal_space_nk",
                "verification_status": "verified",
                "confidence": 0.97,
            },
            {
                "id": "scb_growth_outlook",
                "type": "growth",
                "statement": (
                    "The business is expected to post triple-digit "
                    "growth during 2026."
                ),
                "published_at": "2026-08-25",
                "source_name": "Financial Times",
                "source_key": "sarah_creal_2026_growth",
                "verification_status": "verified",
                "confidence": 0.94,
            },
            {
                "id": "scb_segment",
                "type": "customer_segment",
                "statement": (
                    "The brand is explicitly focused on beauty products "
                    "designed for customers aged 40 and above."
                ),
                "published_at": "2026-08-25",
                "source_name": "Financial Times",
                "source_key": "sarah_creal_40_plus",
                "verification_status": "verified",
                "confidence": 0.99,
            },
        ],

        "needs_validation": [
            {
                "type": "social_volume",
                "question": (
                    "Which social channels generate the strongest "
                    "product education and purchase-intent conversations?"
                ),
            },
            {
                "type": "marketing_stack",
                "question": (
                    "Which CRM, lifecycle and commerce systems "
                    "currently power customer activation?"
                ),
            },
            {
                "type": "buyer",
                "question": (
                    "Who owns international growth, ecommerce "
                    "and customer lifecycle?"
                ),
            },
            {
                "type": "crm_check",
                "question": (
                    "Is Sarah Creal Beauty already known to Blueberry?"
                ),
            },
        ],

        "commercial_hypothesis": {
            "problem": (
                "Fast retail and international expansion can create "
                "large volumes of education-heavy customer questions "
                "while the brand needs to preserve a highly specific "
                "voice and customer experience."
            ),
            "blueberry_wedge": (
                "Use AI-powered personalized conversations to answer "
                "product questions, understand mature-skin needs, "
                "capture customer identity and connect social interest "
                "to commerce and lifecycle journeys."
            ),
            "pilot": (
                "Start with one high-engagement product or UK launch "
                "campaign and measure conversation-to-customer conversion."
            ),
            "why_now": (
                "The business is simultaneously scaling revenue, "
                "retail footprint and geography."
            ),
            "status": "hypothesis",
        },

        "fit_dimensions": {
            "social_intensity": 17.5,
            "commerce_fit": 19.0,
            "urgency": 19.5,
            "personalization_value": 20.0,
            "expansion_value": 18.0,
        },
    },

    # ========================================================
    # 3. GLOSSIER
    # ========================================================

    {
        "id": "target_glossier",
        "company": "Glossier",
        "domain": "glossier.com",
        "industry": "Beauty / DTC",
        "status": "active_research",

        "why_this_account": (
            "Glossier currently has a live, culturally driven campaign "
            "with product, partnership, physical activation and community "
            "engagement components — exactly the kind of moment where "
            "Blueberry could test social conversation as a measurable channel."
        ),

        "verified_signals": [
            {
                "id": "glossier_iloveny",
                "type": "campaign",
                "statement": (
                    "Glossier is currently running an I Love NY "
                    "Balm Dotcom campaign."
                ),
                "observed_at": "2026-08-29",
                "source_name": "Glossier",
                "source_key": "glossier_i_love_ny",
                "verification_status": "verified",
                "confidence": 0.99,
            },
            {
                "id": "glossier_ny_tourism",
                "type": "partnership",
                "statement": (
                    "The campaign is being run in partnership "
                    "with the New York State Tourism Board."
                ),
                "observed_at": "2026-08-29",
                "source_name": "Glossier",
                "source_key": "glossier_ny_tourism_partnership",
                "verification_status": "verified",
                "confidence": 0.99,
            },
            {
                "id": "glossier_balmdega",
                "type": "physical_activation",
                "statement": (
                    "Glossier's NYC Balmdega activation runs from "
                    "July 14 through the end of August."
                ),
                "observed_at": "2026-08-29",
                "source_name": "Glossier",
                "source_key": "glossier_balmdega",
                "verification_status": "verified",
                "confidence": 0.99,
            },
            {
                "id": "glossier_limited_product",
                "type": "product_launch",
                "statement": (
                    "The campaign includes a limited-edition "
                    "apple-flavored I Love NY Balm Dotcom."
                ),
                "observed_at": "2026-08-29",
                "source_name": "Glossier",
                "source_key": "glossier_i_love_ny_product",
                "verification_status": "verified",
                "confidence": 0.99,
            },
        ],

        "needs_validation": [
            {
                "type": "campaign_social_volume",
                "question": (
                    "How much social interaction is the I Love NY "
                    "campaign currently generating?"
                ),
            },
            {
                "type": "marketing_stack",
                "question": (
                    "Which lifecycle and customer-data systems "
                    "currently receive social-originated identity?"
                ),
            },
            {
                "type": "buyer",
                "question": (
                    "Who owns campaign growth, social commerce "
                    "and lifecycle marketing?"
                ),
            },
            {
                "type": "crm_check",
                "question": (
                    "Is Glossier already in Blueberry's CRM or pipeline?"
                ),
            },
        ],

        "commercial_hypothesis": {
            "problem": (
                "A culturally relevant campaign can generate substantial "
                "conversation, but much of that interaction may remain "
                "anonymous and disconnected from lifecycle marketing."
            ),
            "blueberry_wedge": (
                "Turn I Love NY campaign engagement into personalized "
                "1:1 conversations, known customer profiles and "
                "attributable product revenue."
            ),
            "pilot": (
                "Use one campaign conversation stream to test "
                "social engagement → customer identity → commerce."
            ),
            "why_now": (
                "The activation is currently live, creating an immediate "
                "campaign rather than a theoretical future use case."
            ),
            "status": "hypothesis",
        },

        "fit_dimensions": {
            "social_intensity": 19.0,
            "commerce_fit": 18.5,
            "urgency": 18.5,
            "personalization_value": 18.0,
            "expansion_value": 17.0,
        },
    },
]


# ============================================================
# SCORING
# ============================================================


def _calculate_opportunity_score(
    account: Dict,
) -> float:
    """
    Transparent BLOO prioritisation score.

    Five dimensions.
    Each dimension max = 20.
    Total max = 100.
    """

    dimensions = account.get(
        "fit_dimensions",
        {},
    )

    return round(
        sum(
            float(value)
            for value in dimensions.values()
        ),
        1,
    )


def _count_verified_signals(
    account: Dict,
) -> int:

    return sum(
        1
        for signal in account.get(
            "verified_signals",
            [],
        )
        if signal.get(
            "verification_status"
        ) == "verified"
    )


def _count_validation_items(
    account: Dict,
) -> int:

    return len(
        account.get(
            "needs_validation",
            [],
        )
    )


def _research_readiness(
    account: Dict,
) -> str:

    verified = _count_verified_signals(
        account
    )

    validation = _count_validation_items(
        account
    )

    if verified >= 3 and validation <= 2:
        return "outbound_ready"

    if verified >= 2:
        return "commercially_relevant_research"

    return "research_required"


def _enrich_account(
    account: Dict,
) -> Dict:

    enriched = deepcopy(
        account
    )

    enriched[
        "opportunity_score"
    ] = _calculate_opportunity_score(
        enriched
    )

    enriched[
        "evidence_summary"
    ] = {
        "verified": _count_verified_signals(
            enriched
        ),
        "requires_validation": _count_validation_items(
            enriched
        ),
        "readiness": _research_readiness(
            enriched
        ),
    }

    return enriched


# ============================================================
# PUBLIC API
# ============================================================


def get_commercial_accounts() -> List[Dict]:

    accounts = [
        _enrich_account(
            account
        )
        for account in COMMERCIAL_ACCOUNTS
    ]

    return sorted(
        accounts,
        key=lambda item: item[
            "opportunity_score"
        ],
        reverse=True,
    )


def get_commercial_account(
    account_id: str,
) -> Optional[Dict]:

    for account in get_commercial_accounts():

        if account[
            "id"
        ] == account_id:
            return account

    return None


def commercial_intelligence_summary() -> Dict:

    accounts = get_commercial_accounts()

    if not accounts:
        return {
            "accounts": 0,
            "top_account": None,
            "top_score": None,
            "verified_signals": 0,
            "validation_items": 0,
        }

    return {
        "accounts": len(
            accounts
        ),

        "top_account": accounts[
            0
        ]["company"],

        "top_score": accounts[
            0
        ]["opportunity_score"],

        "verified_signals": sum(
            account[
                "evidence_summary"
            ]["verified"]
            for account in accounts
        ),

        "validation_items": sum(
            account[
                "evidence_summary"
            ]["requires_validation"]
            for account in accounts
        ),
    }
