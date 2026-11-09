"""
===========================================================
Enterprise CTMS Copilot
Supervisor Implementation
===========================================================
"""

import re

from app.config.settings import settings
logger = settings.get_logger()

from app.agents.trial_agent import TrialAgent
from app.agents.budget_agent import BudgetAgent
from app.agents.monitoring_agent import MonitoringAgent
from app.agents.site_agent import SiteManagementAgent
from app.agents.recruitment_agent import RecruitmentAgent


class Supervisor:
    """
    Enterprise Multi-Agent Supervisor

    Responsibilities
    ----------------
    • Route requests to the correct agent
    • Support automatic routing
    • Support explicit module selection
    • Log routing decisions
    """

    def __init__(self):

        logger.info("Initializing Supervisor...")

        self.trial_agent = TrialAgent()

        self.budget_agent = BudgetAgent()

        self.monitoring_agent = MonitoringAgent()

        self.site_agent = SiteManagementAgent()

        self.recruitment_agent = RecruitmentAgent()

        logger.success("Supervisor Initialized Successfully.")

    ####################################################################
    # Entry Point
    ####################################################################

    async def invoke(self, request):

        logger.info("=" * 80)
        logger.info("Supervisor Started")

        logger.info(f"Question : {request.question}")

        logger.info(f"Module   : {request.module}")

        try:

            ############################################################
            # Explicit Module
            ############################################################

            module = (request.module or "auto").lower()

            if module != "auto":

                logger.info(f"Explicit Module Selected : {module}")

                agent = self._get_agent(module)

                return await agent.execute(request)

            ############################################################
            # Automatic Routing
            ############################################################

            logger.info("Automatic Agent Routing")

            agent = self.route(request.question)

            logger.success(
                f"Selected Agent : {agent.__class__.__name__}"
            )

            return await agent.execute(request)

        except Exception as ex:

            logger.exception("Supervisor Execution Failed")

            raise

    ####################################################################
    # Intelligent Router
    ####################################################################

    def route(self, question: str):

        question = question.lower()

        ############################################################
        # Budget
        ############################################################

        budget_keywords = [

            "budget",
            "cost",
            "invoice",
            "payment",
            "milestone",
            "financial",
            "expense",
            "revenue",
            "forecast"
        ]

        ############################################################
        # Monitoring
        ############################################################

        monitoring_keywords = [

            "monitor",
            "sdv",
            "finding",
            "visit",
            "capa",
            "deviation",
            "audit",
            "risk",
            "query"
        ]

        ############################################################
        # Recruitment
        ############################################################

        recruitment_keywords = [

            "recruit",
            "screen",
            "screening",
            "randomization",
            "dropout",
            "patient",
            "subject",
            "enrollment",
            "enrolment"
        ]

        ############################################################
        # Site
        ############################################################

        site_keywords = [

            "site",
            "investigator",
            "activation",
            "qualification",
            "feasibility",
            "site initiation",
            "closeout",
            "close-out"
        ]

        ############################################################
        # Trial
        ############################################################

        trial_keywords = [

            "trial",
            "protocol",
            "study",
            "phase",
            "endpoint",
            "arm",
            "objective",
            "schedule",
            "eligibility"
        ]

        ############################################################

        if self._contains(question, budget_keywords):

            return self.budget_agent

        if self._contains(question, monitoring_keywords):

            return self.monitoring_agent

        if self._contains(question, recruitment_keywords):

            return self.recruitment_agent

        if self._contains(question, site_keywords):

            return self.site_agent

        if self._contains(question, trial_keywords):

            return self.trial_agent

        ############################################################
        # Default
        ############################################################

        logger.warning(
            "No matching keywords found. Defaulting to Trial Agent."
        )

        return self.trial_agent

    ####################################################################
    # Agent Lookup
    ####################################################################

    def _get_agent(self, module: str):

        agents = {

            "trial": self.trial_agent,
            "trial_planning": self.trial_agent,

            "budget": self.budget_agent,
            "budget_management": self.budget_agent,

            "monitoring": self.monitoring_agent,

            "site": self.site_agent,
            "site_management": self.site_agent,

            "recruitment": self.recruitment_agent,
            "patient_recruitment": self.recruitment_agent

        }

        if module not in agents:

            raise ValueError(
                f"Unknown module : {module}"
            )

        return agents[module]

    ####################################################################
    # Keyword Search
    ####################################################################

    @staticmethod
    def _contains(
        text: str,
        keywords: list[str]
    ) -> bool:

        for keyword in keywords:

            pattern = rf"\b{re.escape(keyword)}\b"

            if re.search(pattern, text):

                return True

        return False