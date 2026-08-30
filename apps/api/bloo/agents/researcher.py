from typing import Any, Dict, List

from apps.api.bloo.connectors.apollo import ApolloConnector
from apps.api.bloo.connectors.enrichment import (
    EnrichmentRequest,
    enrichment_summary,
)


class ResearchAgent:
    """
    BLOO Research Agent.

    Converts unresolved commercial validation questions into
    structured research tasks.

    Its job is not to invent answers.

    It determines:
    - what is still unknown
    - why the unknown matters
    - which source or connector should resolve it
    - whether the account is allowed to move toward outbound

    For buyer research, the agent can use Apollo when an API
    connection is available.

    Important:
    Connector failure never becomes synthetic evidence.
    If buyer identity or contactability cannot be verified,
    outbound remains blocked.
    """

    name = "researcher"

    BUYER_TITLES = [
        "Chief Marketing Officer",
        "Chief Growth Officer",
        "VP Growth",
        "VP Ecommerce",
        "Head of Ecommerce",
        "Head of Lifecycle Marketing",
        "Head of CRM",
        "Head of Social",
        "VP Digital",
        "Head of Digital",
        "Head of Global Marketing",
    ]

    def _task_priority(
        self,
        validation_type: str,
    ) -> str:
        """
        Assign research priority based on how strongly the
        unknown affects commercial execution.
        """

        high_priority = {
            "buyer",
            "crm_check",
            "marketing_stack",
        }

        medium_priority = {
            "social_volume",
            "campaign_social_volume",
        }

        if validation_type in high_priority:
            return "high"

        if validation_type in medium_priority:
            return "medium"

        return "low"

    def _recommended_source(
        self,
        validation_type: str,
    ) -> Dict[str, str]:
        """
        Recommend the most useful source or connector
        for resolving a research question.
        """

        source_map = {
            "buyer": {
                "primary": "Apollo",
                "secondary": "Clay",
                "purpose": (
                    "Identify likely economic buyer, champion, "
                    "and relevant operating stakeholders."
                ),
            },
            "crm_check": {
                "primary": "company_site",
                "secondary": "manual_research",
                "purpose": (
                    "Validate CRM, lifecycle, ecommerce, or "
                    "customer-engagement infrastructure."
                ),
            },
            "marketing_stack": {
                "primary": "company_site",
                "secondary": "manual_research",
                "purpose": (
                    "Validate the company's observable marketing "
                    "and ecommerce stack without inventing tooling."
                ),
            },
            "social_volume": {
                "primary": "social_platforms",
                "secondary": "manual_research",
                "purpose": (
                    "Estimate whether social engagement volume "
                    "is commercially meaningful."
                ),
            },
            "campaign_social_volume": {
                "primary": "social_platforms",
                "secondary": "manual_research",
                "purpose": (
                    "Validate engagement around the specific "
                    "campaign or commercial trigger."
                ),
            },
        }

        return source_map.get(
            validation_type,
            {
                "primary": "manual_research",
                "secondary": "web_research",
                "purpose": (
                    "Resolve the unknown using current public evidence."
                ),
            },
        )

    def _build_tasks_for_target(
        self,
        target: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Turn one Scout target's unresolved questions
        into research jobs.
        """

        tasks: List[Dict[str, Any]] = []

        company = target.get(
            "company",
            "Unknown company",
        )

        account_id = (
            target.get("account_id")
            or target.get("id")
            or target.get("slug")
            or company.lower().replace(" ", "-")
        )

        unresolved = (
            target.get("needs_validation")
            or target.get("unresolved_questions")
            or target.get("validation_required")
            or []
        )

        for item in unresolved:
            if isinstance(item, str):
                validation_type = item
                question = item
            else:
                validation_type = (
                    item.get("type")
                    or item.get("validation_type")
                    or item.get("key")
                    or "manual_research"
                )

                question = (
                    item.get("question")
                    or item.get("description")
                    or validation_type
                )

            source = self._recommended_source(validation_type)

            task = {
                "account_id": account_id,
                "company": company,
                "validation_type": validation_type,
                "question": question,
                "priority": self._task_priority(validation_type),
                "recommended_source": source,
                "status": "open",
                "blocks_outbound": validation_type
                in {
                    "buyer",
                    "crm_check",
                    "marketing_stack",
                },
            }

            tasks.append(task)

        return tasks

    def _find_domain(
        self,
        target: Dict[str, Any],
    ) -> str:
        """
        Resolve the most likely domain field without
        pretending one exists when Scout did not provide it.
        """

        return (
            target.get("domain")
            or target.get("website_domain")
            or target.get("website")
            or ""
        )

    def _run_buyer_research(
        self,
        target: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Attempt live buyer discovery through Apollo.

        The connector is treated as an evidence source,
        never as ground truth by default.

        A candidate is not considered outbound-safe merely
        because Apollo returned a person.
        """

        company = target.get(
            "company",
            "Unknown company",
        )

        account_id = (
            target.get("account_id")
            or target.get("id")
            or target.get("slug")
            or company.lower().replace(" ", "-")
        )

        domain = self._find_domain(target)

        if not domain:
            return {
                "provider": "apollo",
                "status": "domain_required",
                "company": company,
                "contacts": [],
                "contacts_found": 0,
                "buyer_research_resolved": False,
                "outbound_safe": False,
                "warnings": [
                    "No verified company domain was available for buyer discovery."
                ],
            }

        try:
            connector = ApolloConnector()

            request = EnrichmentRequest(
                account_id=account_id,
                company=company,
                domain=domain,
                target_titles=self.BUYER_TITLES,
            )

            result = connector.enrich_buying_committee(request)

            summary = enrichment_summary(result)

            contacts = [
                contact.model_dump()
                for contact in result.contacts
            ]

            return {
                **summary,
                "contacts": contacts,
                "warnings": list(result.warnings),
            }

        except Exception as exc:
            return {
                "provider": "apollo",
                "status": "connector_error",
                "company": company,
                "contacts": [],
                "contacts_found": 0,
                "buyer_research_resolved": False,
                "outbound_safe": False,
                "warnings": [
                    (
                        "Apollo buyer research could not complete. "
                        f"{type(exc).__name__}: {exc}"
                    )
                ],
            }

    def _attach_live_research(
        self,
        target: Dict[str, Any],
        tasks: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Execute only the research that has a safe,
        explicitly configured live connector.

        Other tasks remain research jobs.
        """

        buyer_tasks = [
            task
            for task in tasks
            if task["validation_type"] == "buyer"
        ]

        if not buyer_tasks:
            return {
                "buyer_research": None,
            }

        buyer_research = self._run_buyer_research(target)

        resolved = bool(
            buyer_research.get("buyer_research_resolved")
        )

        outbound_safe = bool(
            buyer_research.get("outbound_safe")
        )

        for task in buyer_tasks:
            task["connector_result"] = buyer_research

            if resolved and outbound_safe:
                task["status"] = "resolved"
                task["blocks_outbound"] = False
            else:
                task["status"] = "blocked"
                task["blocks_outbound"] = True

        return {
            "buyer_research": buyer_research,
        }

    def build_from_scout(
        self,
        scout_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Build the research layer from Scout recommendations.

        Research may add evidence, but it cannot silently
        manufacture certainty.
        """

        targets = (
            scout_result.get("recommended_targets")
            or scout_result.get("targets")
            or scout_result.get("recommendations")
            or []
        )

        research_queue: List[Dict[str, Any]] = []
        live_research: List[Dict[str, Any]] = []

        for target in targets:
            target_tasks = self._build_tasks_for_target(target)

            live_result = self._attach_live_research(
                target,
                target_tasks,
            )

            research_queue.extend(target_tasks)

            live_research.append(
                {
                    "account_id": (
                        target.get("account_id")
                        or target.get("id")
                        or target.get("slug")
                    ),
                    "company": target.get("company"),
                    **live_result,
                }
            )

        blocking_tasks = [
            task
            for task in research_queue
            if task["blocks_outbound"]
            and task["status"] != "resolved"
        ]

        high_priority = [
            task
            for task in research_queue
            if task["priority"] == "high"
        ]

        outbound_safe = bool(targets) and len(blocking_tasks) == 0

        return {
            "agent": self.name,
            "received_from": "scout",
            "research_queue": research_queue,
            "live_research": live_research,
            "blocking_tasks": blocking_tasks,
            "high_priority": high_priority,
            "blocking_count": len(blocking_tasks),
            "outbound_safe": outbound_safe,
            "research_complete": outbound_safe,
            "policy": {
                "synthetic_contacts_allowed": False,
                "unverified_contacts_allowed_for_outbound": False,
                "connector_failure_unlocks_outbound": False,
            },
        }
