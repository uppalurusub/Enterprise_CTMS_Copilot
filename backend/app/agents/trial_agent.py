"""
===========================================================
Enterprise CTMS Copilot
Trial Planning Agent
===========================================================
"""

from app.config.settings import settings
logger = settings.get_logger()

from app.implementations.agent_impl import BaseAgent

from app.prompts.trial_prompt import trial_prompt


class TrialAgent(BaseAgent):
    """
    Enterprise Trial Planning Agent

    Responsibilities

    • Trial Planning

    • Protocol Design

    • Study Design

    • Inclusion / Exclusion Criteria

    • Study Arms

    • Trial Timeline

    • Trial Objectives
    """

    def __init__(self):

        logger.info("Initializing Trial Planning Agent...")

        super().__init__(

            agent_name="TrialPlanningAgent",

            prompt=trial_prompt

        )

        logger.success(
            "Trial Planning Agent Initialized Successfully."
        )

    ####################################################################
    # Module Name
    ####################################################################

    def module_name(self):

        logger.info("Module : Trial Planning")

        return "trial_planning"

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
            "Building Trial Planning Prompt"
        )

        return self.prompt.format_prompt(

            question=request.question,

            trial_id=request.trial_id,

            protocol_id=request.protocol_id,

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
    ):

        logger.info(
            "Validating Trial Planning Request"
        )

        if not request.question:

            raise ValueError(
                "Question cannot be empty."
            )

        return True