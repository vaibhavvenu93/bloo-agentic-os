from apps.api.bloo.brain.models import (
    Account,
    Evidence,
    EvidenceStatus,
    Insight,
    Relationship,
)


def load_mellow_sleep(brain):
    account = Account(
        id="account_mellow_sleep",
        name="Mellow Sleep",
        domain="mellowsleep.com",
        industry="DTC / Sleep",
        stage="customer",
        evidence_ids=[
            "evidence_mellow_revenue",
            "evidence_mellow_accounts",
            "evidence_mellow_optin",
            "evidence_mellow_setup",
        ],
    )

    brain.add_account(account)

    evidence = [
        Evidence(
            id="evidence_mellow_revenue",
            statement="Blueberry publicly reports that Mellow Sleep attributed $40K in revenue from fewer than five posts.",
            source="Blueberry Mellow Sleep case study",
            status=EvidenceStatus.VERIFIED,
            confidence=1.0,
        ),
        Evidence(
            id="evidence_mellow_accounts",
            statement="Blueberry publicly reports that Mellow Sleep connected 300+ accounts across brands, sub-brands, and influencers.",
            source="Blueberry Mellow Sleep case study",
            status=EvidenceStatus.VERIFIED,
            confidence=1.0,
        ),
        Evidence(
            id="evidence_mellow_optin",
            statement="Blueberry publicly reports a 67% email opt-in rate for Mellow Sleep.",
            source="Blueberry Mellow Sleep case study",
            status=EvidenceStatus.VERIFIED,
            confidence=1.0,
        ),
        Evidence(
            id="evidence_mellow_setup",
            statement="Blueberry publicly reports that Mellow Sleep was live in roughly 10 minutes.",
            source="Blueberry Mellow Sleep case study",
            status=EvidenceStatus.VERIFIED,
            confidence=1.0,
        ),
    ]

    for item in evidence:
        brain.add_evidence(item)

    brain.add_relationship(
        Relationship(
            source_id="account_mellow_sleep",
            relationship="supported_by",
            target_id="evidence_mellow_revenue",
        )
    )

    brain.add_relationship(
        Relationship(
            source_id="account_mellow_sleep",
            relationship="supported_by",
            target_id="evidence_mellow_optin",
        )
    )

    brain.add_insight(
        Insight(
            id="insight_mellow_pattern",
            title="High-intent social engagement can become owned customer data and attributable revenue",
            summary=(
                "Mellow Sleep is a strong public proof point for Blueberry's ability "
                "to turn social engagement into measurable revenue and email capture."
            ),
            confidence=0.95,
            evidence_ids=[
                "evidence_mellow_revenue",
                "evidence_mellow_optin",
            ],
        )
    )
