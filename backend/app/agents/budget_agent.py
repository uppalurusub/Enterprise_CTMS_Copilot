"""
===========================================================
Enterprise CTMS Copilot
Budget Management Agent
===========================================================
"""

from app.config.settings import settings
logger = settings.get_logger()

from app.implementations.agent_impl import BaseAgent

from app.prompts.budget_prompt import budget_prompt


class BudgetAgent(BaseAgent):
    """
    Enterprise Budget Management Agent

    Responsibilities

    • Trial Budget Planning

    • Budget Allocation

    • Budget Utilization

    • Investigator Payments

    • Site Payments

    • CRO Payments

    • Milestone Payments

    • Invoice Management

    • Financial Forecasting

    • Budget Variance Analysis
    """

    def __init__(self):

        logger.info("Initializing Budget Management Agent...")

        super().__init__(
            agent_name="BudgetManagementAgent",
            prompt=budget_prompt
        )

        logger.success(
            "Budget Management Agent Initialized Successfully."
        )

    ####################################################################
    # Module Name
    ####################################################################

    def module_name(self) -> str:

        logger.info("Module : Budget Management")

        return "budget_management"

    ####################################################################
    # Build Prompt
    ####################################################################

    def build_prompt(
        self,
        request,
        sql_result,
        rag_context
    ):

        logger.info("Building Budget Management Prompt")

        return self.prompt.format_prompt(

            question=request.question,

            trial_id=request.trial_id,

            budget_id=request.budget_id,

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
            "Validating Budget Management Request"
        )

        if not request.question.strip():

            raise ValueError(
                "Question cannot be empty."
            )

        return True