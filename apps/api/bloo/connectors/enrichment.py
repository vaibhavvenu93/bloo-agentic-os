from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class EnrichmentRequest(BaseModel):
    """
    A structured request created by BLOO when the Research Agent
    needs buyer or stakeholder information for a target account.
    """

    account_id: str
    company: str

    domain: Optional[str] = None

    target_roles: List[str] = Field(
        default_factory=lambda: [
            "Chief Marketing Officer",
            "Chief Growth Officer",
            "VP Growth",
            "VP Ecommerce",
            "Head of Ecommerce",
            "Head of Lifecycle Marketing",
            "Head of CRM",
            "Head of Social",
        ]
    )

    geography: Optional[str] = None

    max_results: int = Field(
        default=10,
        ge=1,
        le=50,
    )


class ContactCandidate(BaseModel):
    """
    One potential member of the buying committee.

    Nothing is treated as verified unless an enrichment provider
    actually returns evidence for it.
    """

    id: str

    full_name: str

    title: Optional[str] = None

    company: str

    email: Optional[str] = None

    linkedin_url: Optional[str] = None

    location: Optional[str] = None

    seniority: Optional[str] = None

    department: Optional[str] = None

    source: str

    source_record_id: Optional[str] = None

    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
    )

    email_status: str = "unknown"

    verification_status: str = "unverified"

    evidence: List[str] = Field(
        default_factory=list
    )


class EnrichmentResult(BaseModel):
    """
    Normalized output returned by any enrichment provider.

    Apollo and Clay should eventually return this same contract,
    allowing the rest of BLOO to remain provider-agnostic.
    """

    provider: str

    account_id: str

    company: str

    status: str

    contacts: List[ContactCandidate] = Field(
        default_factory=list
    )

    searched_roles: List[str] = Field(
        default_factory=list
    )

    total_contacts: int = 0

    warnings: List[str] = Field(
        default_factory=list
    )

    metadata: Dict = Field(
        default_factory=dict
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )


class EnrichmentConnector(ABC):
    """
    Provider-independent enrichment connector.

    Implementations may later include:

    - ApolloConnector
    - ClayConnector
    - HubSpotConnector
    - SalesforceConnector
    - LinkedIn-approved data source
    """

    provider_name = "unknown"

    @abstractmethod
    def enrich_buying_committee(
        self,
        request: EnrichmentRequest,
    ) -> EnrichmentResult:
        """
        Resolve likely buyer and stakeholder candidates.
        """
        raise NotImplementedError


class DisabledEnrichmentConnector(
    EnrichmentConnector
):
    """
    Safe connector used before real provider credentials exist.

    Crucially, this connector DOES NOT generate fake contacts.

    It returns a structured 'connector_required' result so BLOO
    knows the research task remains unresolved.
    """

    provider_name = "not_connected"

    def enrich_buying_committee(
        self,
        request: EnrichmentRequest,
    ) -> EnrichmentResult:

        return EnrichmentResult(
            provider=self.provider_name,

            account_id=request.account_id,

            company=request.company,

            status="connector_required",

            contacts=[],

            searched_roles=request.target_roles,

            total_contacts=0,

            warnings=[
                (
                    "No live enrichment provider is connected. "
                    "Buyer research remains unresolved."
                ),
                (
                    "Connect Apollo or Clay before using "
                    "contact data for outbound."
                ),
            ],

            metadata={
                "outbound_safe": False,
                "synthetic_contacts_used": False,
                "requested_max_results": (
                    request.max_results
                ),
            },
        )


def build_enrichment_request(
    account: Dict,
) -> EnrichmentRequest:
    """
    Convert a BLOO commercial account into a normalized
    enrichment request.

    We intentionally infer ROLE TYPES only.
    We do not invent names or email addresses.
    """

    industry = account.get(
        "industry",
        "",
    )

    target_roles = [
        "Chief Marketing Officer",
        "Chief Growth Officer",
        "VP Growth",
        "VP Ecommerce",
        "Head of Ecommerce",
        "Head of Lifecycle Marketing",
        "Head of CRM",
        "Head of Social",
    ]

    if "Beauty" in industry:
        target_roles.extend(
            [
                "VP Digital",
                "Head of Digital",
                "Head of Global Marketing",
            ]
        )

    # Remove duplicates while preserving order.
    unique_roles = list(
        dict.fromkeys(
            target_roles
        )
    )

    return EnrichmentRequest(
        account_id=account.get(
            "id",
            "unknown",
        ),

        company=account.get(
            "company",
            "Unknown company",
        ),

        domain=account.get(
            "website"
        ),

        target_roles=unique_roles,

        max_results=10,
    )


def enrichment_summary(
    result: EnrichmentResult,
) -> Dict:
    """
    Small operating summary for agents and UI.
    """

    verified_contacts = [
        contact
        for contact in result.contacts
        if contact.verification_status
        == "verified"
    ]

    contacts_with_email = [
        contact
        for contact in result.contacts
        if contact.email
    ]

    return {
        "provider": result.provider,

        "status": result.status,

        "company": result.company,

        "contacts_found": len(
            result.contacts
        ),

        "verified_contacts": len(
            verified_contacts
        ),

        "contacts_with_email": len(
            contacts_with_email
        ),

        "buyer_research_resolved": (
            len(
                verified_contacts
            ) > 0
        ),

        "outbound_safe": (
            result.metadata.get(
                "outbound_safe",
                False,
            )
        ),
    }
