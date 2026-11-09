"""
===========================================================
Enterprise CTMS Copilot
Patient Recruitment Agent
===========================================================
"""

from app.config.settings import settings
logger = settings.get_logger()

from app.implementations.agent_impl import BaseAgent

from app.prompts.recruitment_prompt import recruitment_prompt


class RecruitmentAgent(BaseAgent):
    """
    Enterprise Patient Recruitment Agent

    Responsibilities

    • Patient Recruitment
    • Patient Screening
    • Patient Enrollment
    • Randomization
    • Recruitment Planning
    • Recruitment Forecasting
    • Recruitment Analytics
    • Site Recruitment Performance
    • Patient Retention
    • Dropout Analysis
    """

    def __init__(self):

        logger.info("Initializing Patient Recruitment Agent...")

        super().__init__(
            agent_name="PatientRecruitmentAgent",
            prompt=recruitment_prompt
        )

        logger.success(
            "Patient Recruitment Agent Initialized Successfully."
        )

    ####################################################################
    # Module Name
    ####################################################################

    def module_name(self) -> str:

        logger.info("Module : Patient Recruitment")

        return "patient_recruitment"

    ####################################################################
    # Build Prompt
    ####################################################################

    def build_prompt(
        self,
        request,
        sql_result,
        rag_context
    ):

        logger.info("Building Patient Recruitment Prompt")

        return self.prompt.format_prompt(

            question=request.question,

            trial_id=request.trial_id,

            site_id=request.site_id,

            patient_id=request.patient_id,

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
            "Validating Patient Recruitment Request"
        )

        if not request.question.strip():

            raise ValueError(
                "Question cannot be empty."
            )

        return True