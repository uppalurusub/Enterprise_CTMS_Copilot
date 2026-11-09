"""
===========================================================
Enterprise CTMS Copilot
Monitoring Agent
===========================================================
"""

from app.config.settings import settings
logger = settings.get_logger()

from app.implementations.agent_impl import BaseAgent

from app.prompts.monitoring_prompt import monitoring_prompt


class MonitoringAgent(BaseAgent):
    """
    Enterprise Monitoring Agent

    Responsibilities

    • Site Monitoring
    • Remote Monitoring
    • Monitoring Visits
    • Source Data Verification (SDV)
    • Risk-Based Monitoring (RBM)
    • Protocol Deviations
    • CAPA Management
    • Monitoring Findings
    • Audit Readiness
    • Inspection Readiness
    """

    def __init__(self):

        logger.info("Initializing Monitoring Agent...")

        super().__init__(
            agent_name="MonitoringAgent",
            prompt=monitoring_prompt
        )

        logger.success(
            "Monitoring Agent Initialized Successfully."
        )

    ####################################################################
    # Module Name
    ####################################################################

    def module_name(self) -> str:

        logger.info("Module : Monitoring")

        return "monitoring"

    ####################################################################
    # Build Prompt
    ####################################################################

    def build_prompt(
        self,
        request,
        sql_result,
        rag_context
    ):

        logger.info("Building Monitoring Prompt")

        return self.prompt.format_prompt(

            question=request.question,

            trial_id=request.trial_id,

            site_id=request.site_id,

            monitoring_visit_id=request.monitoring_visit_id,

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
            "Validating Monitoring Request"
        )

        if not request.question.strip():

            raise ValueError(
                "Question cannot be empty."
            )

        return True