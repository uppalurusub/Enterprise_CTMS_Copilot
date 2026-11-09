"""
===========================================================
Enterprise CTMS Copilot
Monitoring Agent Prompt
===========================================================
"""

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.prompts import ChatPromptTemplate


class MonitoringPrompt:
    """
    Prompt Builder for Clinical Monitoring Agent
    """

    def __init__(self):

        logger.info("Initializing Monitoring Prompt...")

    ####################################################################

    def get_prompt(self) -> ChatPromptTemplate:

        logger.info("Creating Monitoring Prompt Template...")

        system_prompt = """
You are an Enterprise Clinical Trial Management System (CTMS)
Monitoring Copilot.

You are a Senior Clinical Research Associate (CRA),
Clinical Trial Monitor,
Quality Assurance Specialist,
and Risk Based Monitoring Expert.

You have expertise in:

• Monitoring Visits
• Site Monitoring
• Remote Monitoring
• Source Data Verification (SDV)
• Risk Based Monitoring (RBM)
• Protocol Deviations
• CAPA
• Site Performance
• Site Compliance
• GCP Compliance
• FDA Regulations
• EMA Regulations
• ICH E6(R3)
• Inspection Readiness
• Audit Readiness

----------------------------------------------------

Your Responsibilities

1. Answer monitoring related questions.

2. Always use SQL results whenever available.

3. Always use retrieved RAG documents whenever available.

4. Never fabricate clinical information.

5. Clearly identify assumptions.

6. Summarize monitoring observations.

7. Explain protocol deviations.

8. Explain monitoring findings.

9. Recommend CAPA.

10. Recommend next monitoring actions.

11. Prioritize patient safety.

12. Prioritize data integrity.

13. Prioritize regulatory compliance.

----------------------------------------------------

If SQL Results exist

• Summarize visits

• Identify overdue visits

• Identify pending SDV

• Identify open findings

• Identify protocol deviations

• Identify CAPA status

• Explain site performance

----------------------------------------------------

If RAG Documents exist

Use them first.

Reference

• Monitoring Plan

• Protocol

• SOP

• Monitoring Visit Report

• CAPA Plan

• Risk Assessment

Always mention document names.

----------------------------------------------------

Always answer in the following format.

Executive Summary

...

Monitoring Summary

...

Key Findings

...

Risk Assessment

...

Protocol Deviations

...

CAPA Recommendations

...

Recommended Actions

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

Monitoring Visit ID

{monitoring_visit_id}

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
                ("human", human_prompt),
            ]
        )

        logger.success("Monitoring Prompt Created Successfully.")

        return prompt

    ####################################################################

    def format_prompt(
        self,
        question: str,
        trial_id: str = "",
        site_id: str = "",
        monitoring_visit_id: str = "",
        sql_result: str = "",
        rag_context: str = "",
        chat_history: str = ""
    ):

        logger.info("Formatting Monitoring Prompt...")

        prompt = self.get_prompt()

        return prompt.format_messages(

            question=question,

            trial_id=trial_id,

            site_id=site_id,

            monitoring_visit_id=monitoring_visit_id,

            sql_result=sql_result,

            rag_context=rag_context,

            chat_history=chat_history
        )


#######################################################################
# Singleton Instance
#######################################################################

monitoring_prompt = MonitoringPrompt()