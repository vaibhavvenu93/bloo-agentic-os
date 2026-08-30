import os
from typing import Dict, List, Optional

import httpx

from apps.api.bloo.connectors.enrichment import (
    ContactCandidate,
    EnrichmentConnector,
    EnrichmentRequest,
    EnrichmentResult,
)


class ApolloConnector(EnrichmentConnector):
    """
    BLOO Apollo Connector

    Uses Apollo People Search to discover likely buying-committee
    members for an account.

    Important:
    Apollo People Search does not return email addresses.
    Email enrichment should be handled by a separate enrichment
    step after candidate discovery.

    Authentication:
    APOLLO_API_KEY environment variable
    """

    provider_name = "apollo"

    base_url = "https://api.apollo.io/api/v1"

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout_seconds: float = 20.0,
    ):
        self.api_key = (
            api_key
            or os.getenv("APOLLO_API_KEY")
        )

        self.timeout_seconds = timeout_seconds

    def is_configured(self) -> bool:
        """
        Return True only when an API key is available.
        """

        return bool(self.api_key)

    def health(self) -> Dict:
        """
        Validate that Apollo credentials work.

        This does not expose the API key.
        """

        if not self.api_key:
            return {
                "provider": self.provider_name,
                "configured": False,
                "healthy": False,
                "status": "api_key_missing",
            }

        try:
            response = httpx.get(
                f"{self.base_url}/auth/health",
                headers=self._headers(),
                timeout=self.timeout_seconds,
            )

            return {
                "provider": self.provider_name,
                "configured": True,
                "healthy": response.status_code == 200,
                "status_code": response.status_code,
                "status": (
                    "healthy"
                    if response.status_code == 200
                    else "authentication_failed"
                ),
            }

        except httpx.HTTPError as exc:
            return {
                "provider": self.provider_name,
                "configured": True,
                "healthy": False,
                "status": "connection_error",
                "error": str(exc),
            }

    def _headers(self) -> Dict[str, str]:
        """
        Build Apollo authentication headers.
        """

        if not self.api_key:
            return {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": self.api_key,
        }

    def _organization_domain(
        self,
        request: EnrichmentRequest,
    ) -> Optional[str]:
        """
        Convert a website/domain into a clean organization domain.
        """

        if not request.domain:
            return None

        domain = request.domain.strip()

        domain = domain.replace(
            "https://",
            "",
        )

        domain = domain.replace(
            "http://",
            "",
        )

        domain = domain.split("/")[0]

        if domain.startswith("www."):
            domain = domain[4:]

        return domain or None

    def _search_people(
        self,
        request: EnrichmentRequest,
    ) -> Dict:
        """
        Run Apollo People Search.

        This discovers candidates only.
        It does not claim email verification.
        """

        if not self.api_key:
            return {
                "status": "api_key_missing",
                "people": [],
                "pagination": {},
            }

        payload: Dict = {
            "person_titles": (
                request.target_roles
            ),
            "include_similar_titles": True,
            "page": 1,
            "per_page": request.max_results,
        }

        domain = self._organization_domain(
            request
        )

        if domain:
            payload[
                "q_organization_domains_list"
            ] = [
                domain
            ]
        else:
            payload[
                "q_organization_name"
            ] = request.company

        if request.geography:
            payload[
                "person_locations"
            ] = [
                request.geography
            ]

        response = httpx.post(
            (
                f"{self.base_url}"
                "/mixed_people/api_search"
            ),
            headers=self._headers(),
            json=payload,
            timeout=self.timeout_seconds,
        )

        response.raise_for_status()

        data = response.json()

        return {
            "status": "success",
            "people": data.get(
                "people",
                [],
            ),
            "pagination": data.get(
                "pagination",
                {},
            ),
        }

    def _map_person(
        self,
        person: Dict,
        company: str,
    ) -> ContactCandidate:
        """
        Normalize one Apollo person into BLOO's
        provider-independent contact model.
        """

        first_name = person.get(
            "first_name"
        ) or ""

        last_name = person.get(
            "last_name"
        ) or ""

        full_name = (
            person.get("name")
            or (
                f"{first_name} {last_name}"
            ).strip()
            or "Unknown"
        )

        organization = person.get(
            "organization"
        ) or {}

        current_company = (
            organization.get("name")
            or person.get(
                "organization_name"
            )
            or company
        )

        linkedin_url = (
            person.get("linkedin_url")
        )

        person_id = (
            person.get("id")
            or (
                f"apollo_{full_name}"
                .lower()
                .replace(" ", "_")
            )
        )

        evidence = []

        if person.get("title"):
            evidence.append(
                (
                    "Apollo returned current title: "
                    f"{person.get('title')}"
                )
            )

        if current_company:
            evidence.append(
                (
                    "Apollo associated candidate with "
                    f"{current_company}"
                )
            )

        return ContactCandidate(
            id=str(person_id),

            full_name=full_name,

            title=person.get(
                "title"
            ),

            company=current_company,

            # People Search does not return email.
            email=None,

            linkedin_url=linkedin_url,

            location=person.get(
                "city"
            ),

            seniority=person.get(
                "seniority"
            ),

            department=person.get(
                "departments",
                [None],
            )[0]
            if person.get(
                "departments"
            )
            else None,

            source="apollo_people_search",

            source_record_id=person.get(
                "id"
            ),

            confidence=0.8,

            email_status="not_enriched",

            verification_status=(
                "candidate"
            ),

            evidence=evidence,
        )

    def enrich_buying_committee(
        self,
        request: EnrichmentRequest,
    ) -> EnrichmentResult:
        """
        Discover likely members of the target account's
        buying committee.

        This step identifies candidates.
        It does not yet enrich their emails.
        """

        if not self.api_key:
            return EnrichmentResult(
                provider=self.provider_name,

                account_id=request.account_id,

                company=request.company,

                status="api_key_missing",

                contacts=[],

                searched_roles=(
                    request.target_roles
                ),

                total_contacts=0,

                warnings=[
                    (
                        "APOLLO_API_KEY is not configured."
                    )
                ],

                metadata={
                    "outbound_safe": False,
                    "buyer_research_resolved": False,
                    "email_enrichment_required": True,
                    "synthetic_contacts_used": False,
                },
            )

        try:
            search_result = (
                self._search_people(
                    request
                )
            )

            contacts: List[
                ContactCandidate
            ] = [
                self._map_person(
                    person,
                    request.company,
                )
                for person
                in search_result.get(
                    "people",
                    [],
                )
            ]

            return EnrichmentResult(
                provider=self.provider_name,

                account_id=request.account_id,

                company=request.company,

                status=(
                    "candidates_found"
                    if contacts
                    else "no_candidates"
                ),

                contacts=contacts,

                searched_roles=(
                    request.target_roles
                ),

                total_contacts=len(
                    contacts
                ),

                warnings=(
                    [
                        (
                            "Candidate discovery succeeded, "
                            "but email enrichment is still required."
                        )
                    ]
                    if contacts
                    else [
                        (
                            "Apollo returned no candidate buyers "
                            "for the supplied filters."
                        )
                    ]
                ),

                metadata={
                    "outbound_safe": False,
                    "buyer_research_resolved": (
                        len(contacts) > 0
                    ),
                    "email_enrichment_required": True,
                    "synthetic_contacts_used": False,
                    "pagination": (
                        search_result.get(
                            "pagination",
                            {},
                        )
                    ),
                },
            )

        except httpx.HTTPStatusError as exc:
            return EnrichmentResult(
                provider=self.provider_name,

                account_id=request.account_id,

                company=request.company,

                status="apollo_http_error",

                contacts=[],

                searched_roles=(
                    request.target_roles
                ),

                total_contacts=0,

                warnings=[
                    (
                        "Apollo returned HTTP "
                        f"{exc.response.status_code}."
                    )
                ],

                metadata={
                    "outbound_safe": False,
                    "buyer_research_resolved": False,
                    "email_enrichment_required": True,
                    "synthetic_contacts_used": False,
                },
            )

        except httpx.HTTPError as exc:
            return EnrichmentResult(
                provider=self.provider_name,

                account_id=request.account_id,

                company=request.company,

                status="apollo_connection_error",

                contacts=[],

                searched_roles=(
                    request.target_roles
                ),

                total_contacts=0,

                warnings=[
                    str(exc)
                ],

                metadata={
                    "outbound_safe": False,
                    "buyer_research_resolved": False,
                    "email_enrichment_required": True,
                    "synthetic_contacts_used": False,
                },
            )
