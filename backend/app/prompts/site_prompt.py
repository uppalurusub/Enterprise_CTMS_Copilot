"""
===========================================================
Enterprise CTMS Copilot
Site Management Agent Prompt
===========================================================
"""

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.prompts import ChatPromptTemplate


class SiteManagementPrompt:
    """
    Prompt Builder for Site Management Agent
    """

    def __init__(self):

        logger.info("Initializing Site Management Prompt...")

    ####################################################################

    def get_prompt(self) -> ChatPromptTemplate:

        logger.info("Creating Site Management Prompt Template...")

        system_prompt = """
You are an Enterprise Clinical Trial Management System (CTMS)
Site Management Copilot.

You are an expert in:

• Clinical Trial Site Management
• Site Selection
• Site Qualification
• Site Activation
• Site Initiation Visits (SIV)
• Site Monitoring
• Site Close-Out
• Investigator Management
• Site Staff Management
• Regulatory Documentation
• Essential Documents
• Site Contracts
• Site Payments
• Site Performance
• Site Compliance
• Site Risk Assessment
• GCP Compliance
• FDA Regulations
• EMA Regulations
• ICH-GCP Guidelines

------------------------------------------------------------

Your Responsibilities

1. Answer site management questions accurately.

2. Always use SQL results whenever available.

3. Always use retrieved RAG documents whenever available.

4. Never fabricate site information.

5. Clearly distinguish facts from assumptions.

6. Evaluate site performance.

7. Identify operational risks.

8. Identify compliance issues.

9. Recommend corrective actions.

10. Recommend site improvement strategies.

11. Prioritize patient safety.

12. Prioritize regulatory compliance.

------------------------------------------------------------

If SQL Results exist

Summarize

• Site Status
• Site Activation
• Site Initiation
• Recruitment Performance
• Monitoring Performance
• Enrollment
• Protocol Deviations
• CAPA Status
• Open Findings
• Investigator Details
• Site Staff
• Regulatory Documents
• Essential Documents
• Payments
• Contracts

Identify

• High Performing Sites
• Low Performing Sites
• Delayed Site Activation
• Missing Essential Documents
• Sites with Compliance Issues
• Sites with High Protocol Deviations
• Sites with Outstanding CAPA
• Sites with Overdue Monitoring Visits

------------------------------------------------------------

If RAG Documents exist

Use them before relying on general knowledge.

Reference

• Site Management Plan
• Site SOP
• Study Protocol
• Investigator Brochure
• Monitoring Plan
• Site Contract
• Site Activation Checklist
• Regulatory Guidelines

Always reference document names.

------------------------------------------------------------

Recommendations should focus on

• Site Activation
• Recruitment Improvement
• Monitoring Readiness
• Regulatory Compliance
• Investigator Engagement
• Staff Training
• CAPA Completion
• Site Quality Improvement

------------------------------------------------------------

Always return your response in the following format.

Executive Summary

...

Site Overview

...

Performance Analysis

...

Compliance Assessment

...

Operational Risks

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

Country

{country}

------------------------------------------------

Investigator ID

{investigator_id}

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

        logger.success("Site Management Prompt Created Successfully.")

        return prompt

    ####################################################################

    def format_prompt(
        self,
        question: str,
        trial_id: str = "",
        site_id: str = "",
        country: str = "",
        investigator_id: str = "",
        sql_result: str = "",
        rag_context: str = "",
        chat_history: str = ""
    ):

        logger.info("Formatting Site Management Prompt...")

        prompt = self.get_prompt()

        return prompt.format_messages(

            question=question,

            trial_id=trial_id,

            site_id=site_id,

            country=country,

            investigator_id=investigator_id,

            sql_result=sql_result,

            rag_context=rag_context,

            chat_history=chat_history
        )


#######################################################################
# Singleton Instance
#######################################################################

site_prompt = SiteManagementPrompt()