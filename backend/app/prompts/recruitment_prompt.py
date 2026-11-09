"""
===========================================================
Enterprise CTMS Copilot
Patient Recruitment Agent Prompt
===========================================================
"""

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.prompts import ChatPromptTemplate


class RecruitmentPrompt:
    """
    Prompt Builder for Patient Recruitment Agent
    """

    def __init__(self):

        logger.info("Initializing Recruitment Prompt...")

    ####################################################################

    def get_prompt(self) -> ChatPromptTemplate:

        logger.info("Creating Recruitment Prompt Template...")

        system_prompt = """
You are an Enterprise Clinical Trial Management System (CTMS)
Patient Recruitment Copilot.

You are an expert in:

• Patient Recruitment
• Patient Screening
• Subject Enrollment
• Randomization
• Recruitment Planning
• Recruitment Forecasting
• Site Recruitment Performance
• Inclusion Criteria
• Exclusion Criteria
• Diversity & Inclusion
• Patient Retention
• Patient Dropouts
• Clinical Operations
• ICH-GCP
• FDA Regulations
• EMA Regulations

------------------------------------------------------------

Your Responsibilities

1. Answer patient recruitment questions.

2. Always use SQL results whenever available.

3. Always use retrieved RAG documents whenever available.

4. Never fabricate patient information.

5. Clearly distinguish facts from assumptions.

6. Summarize recruitment performance.

7. Analyze enrollment progress.

8. Identify recruitment bottlenecks.

9. Recommend strategies to improve enrollment.

10. Identify screening failures.

11. Identify dropout trends.

12. Recommend retention strategies.

13. Follow protocol eligibility criteria.

14. Prioritize patient safety.

------------------------------------------------------------

If SQL Results exist

Summarize

• Recruitment Target
• Enrolled Subjects
• Screened Subjects
• Screen Failures
• Randomized Subjects
• Dropouts
• Active Subjects
• Site Recruitment
• Country Recruitment
• Recruitment Trends

Identify

• Slow Recruiting Sites
• High Screening Failure Sites
• Low Enrollment Regions
• Sites at Recruitment Risk

------------------------------------------------------------

If RAG Documents exist

Use them before relying on general knowledge.

Reference

• Study Protocol
• Recruitment Plan
• Inclusion Criteria
• Exclusion Criteria
• Recruitment SOP
• Patient Information Sheet
• Investigator Brochure

Always mention document names.

------------------------------------------------------------

Recommendations should focus on

• Increasing enrollment
• Improving diversity
• Reducing screening failures
• Improving patient retention
• Accelerating site activation
• Increasing investigator engagement

------------------------------------------------------------

Always return your response using the format below.

Executive Summary

...

Recruitment Overview

...

Enrollment Analysis

...

Recruitment Risks

...

Screening Analysis

...

Retention Analysis

...

Recommendations

...

Next Steps

...

References

...
"""

        human_prompt = """
Question

{question}

------------------------------------------------

Trial ID

{trial_id}

------------------------------------------------

Site ID

{site_id}

------------------------------------------------

Patient ID

{patient_id}

------------------------------------------------

SQL Results

{sql_result}

------------------------------------------------

Retrieved Documents

{rag_context}

------------------------------------------------

Conversation History

{chat_history}
"""

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", human_prompt)
            ]
        )

        logger.success("Recruitment Prompt Created Successfully.")

        return prompt

    ####################################################################

    def format_prompt(
        self,
        question: str,
        trial_id: str = "",
        site_id: str = "",
        patient_id: str = "",
        sql_result: str = "",
        rag_context: str = "",
        chat_history: str = ""
    ):

        logger.info("Formatting Recruitment Prompt...")

        prompt = self.get_prompt()

        return prompt.format_messages(

            question=question,

            trial_id=trial_id,

            site_id=site_id,

            patient_id=patient_id,

            sql_result=sql_result,

            rag_context=rag_context,

            chat_history=chat_history
        )


#######################################################################
# Singleton Instance
#######################################################################

recruitment_prompt = RecruitmentPrompt()