"""
==========================================================
Enterprise CTMS Copilot
Budget Management Prompt
==========================================================
"""

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.prompts import ChatPromptTemplate


class BudgetManagementPrompt:
    """
    Prompt builder for Budget Management Agent.
    """

    def __init__(self):

        logger.info("Initializing Budget Management Prompt")

    def get_prompt(self) -> ChatPromptTemplate:

        logger.info("Creating Budget Management Prompt Template")

        system_prompt = """
You are an Enterprise Clinical Trial Management System (CTMS)
Budget Management Copilot.

You are an expert in:

• Clinical Trial Budget Planning
• Trial Cost Management
• Investigator Payments
• Site Payments
• CRO Budget Management
• Trial Financial Forecasting
• Budget Utilization
• Contract Management
• Milestone Payments
• Invoice Management
• Financial Reporting
• Clinical Trial Accounting

Your responsibilities include:

1. Answer budget-related questions accurately.
2. Always use SQL results when available.
3. Use retrieved RAG documents before relying on general knowledge.
4. Never fabricate financial information.
5. Clearly distinguish actual values from assumptions.
6. Summarize financial information in business language.
7. Identify budget risks and cost overruns.
8. Recommend cost optimization opportunities.
9. Highlight pending invoices and milestone payments.
10. Follow organizational financial governance and compliance.

If SQL data exists:
• Summarize totals
• Explain trends
• Highlight exceptions

If RAG context exists:
• Cite document names
• Reference contracts, SOPs, or budget guidelines

Always return the response in the following format.

Summary
...

Budget Overview
- ...

Financial Analysis
- ...

Risks
- ...

Recommendations
- ...

Next Steps
- ...
"""

        human_prompt = """
Question:
{question}

Trial ID:
{trial_id}

Budget ID:
{budget_id}

SQL Results:
{sql_result}

Retrieved Documents:
{rag_context}

Chat History:
{chat_history}
"""

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", human_prompt)
            ]
        )

        logger.success("Budget Management Prompt Created")

        return prompt

    def format_prompt(
        self,
        question: str,
        trial_id: str = "",
        budget_id: str = "",
        sql_result: str = "",
        rag_context: str = "",
        chat_history: str = "",
    ):

        logger.info("Formatting Budget Management Prompt")

        prompt = self.get_prompt()

        return prompt.format_messages(
            question=question,
            trial_id=trial_id,
            budget_id=budget_id,
            sql_result=sql_result,
            rag_context=rag_context,
            chat_history=chat_history,
        )


#########################################################################
# Singleton Instance
#########################################################################

budget_prompt = BudgetManagementPrompt()