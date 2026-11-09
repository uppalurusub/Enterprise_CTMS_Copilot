"""
===========================================================
Enterprise CTMS Copilot
Site Management Agent
===========================================================
"""

from app.config.settings import settings
logger = settings.get_logger()

from app.implementations.agent_impl import BaseAgent

from app.prompts.site_prompt import site_prompt


class SiteManagementAgent(BaseAgent):
    """
    Enterprise Site Management Agent

    Responsibilities

    • Site Selection

    • Site Feasibility

    • Site Qualification

    • Site Activation

    • Site Initiation

    • Site Monitoring

    • Site Performance

    • Investigator Management

    • Site Staff

    • Site Compliance

    • Site Close-Out

    • Site Risk Assessment
    """

    def __init__(self):

        logger.info("Initializing Site Management Agent...")

        super().__init__(

            agent_name="SiteManagementAgent",

            prompt=site_prompt

        )

        logger.success(
            "Site Management Agent Initialized Successfully."
        )

    ####################################################################
    # Module Name
    ####################################################################

    def module_name(self) -> str:

        logger.info("Module : Site Management")

        return "site_management"

    ####################################################################
    # Build Prompt
    ####################################################################

    def build_prompt(

        self,

        request,

        sql_result,

        rag_context

    ):

        logger.info(
            "Building Site Management Prompt"
        )

        return self.prompt.format_prompt(

            question=request.question,

            trial_id=request.trial_id,

            site_id=request.site_id,

            country=request.filters.get(
                "country",
                ""
            ),

            sql_result=sql_result,

            rag_context=rag_context,

            chat_history=request.chat_history

        )

    ####################################################################
    # Optional Validation
    ####################################################################

    def validate_request(
        self,
        request
    ) -> bool:

        logger.info(
            "Validating Site Management Request"
        )

        if not request.question.strip():

            raise ValueError(
                "Question cannot be empty."
            )

        return True