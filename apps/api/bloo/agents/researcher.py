from typing import Dict, List


class ResearchAgent:
    """
    BLOO Research Agent

    Converts unresolved commercial validation questions into
    structured research tasks.

    Its job is not to invent answers.

    It determines:
    - what is still unknown
    - why the unknown matters
    - which source or connector should resolve it
    - whether the account is allowed to move toward outbound

    Later this agent can connect to:
    - web research
    - Apollo
    - Clay
    - CRM
    - LinkedIn
    - Shopify / Klaviyo
    - company systems
    """

    name = "researcher"

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
    ) -> Dict:
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
                "primary": "CRM",
                "secondary": "Company Brain",
                "purpose": (
                    "Check whether the account or contact already "
                    "exists in pipeline, history, or active ownership."
                ),
            },

            "marketing_stack": {
                "primary": "Clay",
                "secondary": "public_web",
                "purpose": (
                    "Identify likely commerce, CRM, lifecycle, "
                    "and customer-data systems."
                ),
            },

            "social_volume": {
                "primary": "public_web",
                "secondary": "social_platforms",
                "purpose": (
                    "Estimate visible engagement volume and identify "
                    "where purchase-intent conversations occur."
                ),
            },

            "campaign_social_volume": {
                "primary": "public_web",
                "secondary": "social_platforms",
                "purpose": (
                    "Measure engagement around the specific active campaign."
                ),
            },
        }

        return source_map.get(
            validation_type,
            {
                "primary": "public_web",
                "secondary": "manual_research",
                "purpose": (
                    "Resolve the unknown using current public evidence."
                ),
            },
        )

    def build_tasks_for_target(
        self,
        target: Dict,
    ) -> List[Dict]:
        """
        Turn one Scout target's unresolved questions
        into research jobs.
        """

        tasks = []

        company = target.get(
            "company",
            "Unknown company",
        )

        for index, item in enumerate(
            target.get(
                "needs_validation",
                [],
            ),
            start=1,
        ):
            validation_type = item.get(
                "type",
                "general",
            )

            source = self._recommended_source(
                validation_type
            )

            tasks.append(
                {
                    "id": (
                        f"research_{target.get('id', 'unknown')}_{index}"
                    ),

                    "account_id": target.get(
                        "id"
                    ),

                    "company": company,

                    "validation_type": validation_type,

                    "question": item.get(
                        "question"
                    ),

                    "priority": self._task_priority(
                        validation_type
                    ),

                    "recommended_source": source,

                    "status": "open",

                    "result": None,

                    "evidence_status": (
                        "unresolved"
                    ),

                    "blocks_outbound": (
                        validation_type
                        in {
                            "buyer",
                            "crm_check",
                        }
                    ),
                }
            )

        return tasks

    def build_from_scout(
        self,
        scout_output: Dict,
        limit: int = 3,
    ) -> Dict:
        """
        Convert Scout's research-required targets into
        a structured research queue.
        """

        targets = scout_output.get(
            "research_required",
            [],
        )[:limit]

        research_queue = []

        for target in targets:
            research_queue.extend(
                self.build_tasks_for_target(
                    target
                )
            )

        blocking_tasks = [
            task
            for task in research_queue
            if task["blocks_outbound"]
        ]

        high_priority = [
            task
            for task in research_queue
            if task["priority"] == "high"
        ]

        return {
            "agent": self.name,

            "received_from": "scout",

            "objective": (
                "Resolve the commercial unknowns that prevent "
                "high-priority accounts from becoming outbound-ready."
            ),

            "accounts_in_research": [
                {
                    "id": target.get(
                        "id"
                    ),
                    "company": target.get(
                        "company"
                    ),
                    "opportunity_score": target.get(
                        "opportunity_score"
                    ),
                    "readiness": target.get(
                        "readiness"
                    ),
                }
                for target in targets
            ],

            "research_queue": research_queue,

            "summary": {
                "accounts": len(
                    targets
                ),

                "tasks": len(
                    research_queue
                ),

                "high_priority_tasks": len(
                    high_priority
                ),

                "blocking_tasks": len(
                    blocking_tasks
                ),

                "outbound_allowed": (
                    len(blocking_tasks) == 0
                    and len(research_queue) == 0
                ),
            },
        }
