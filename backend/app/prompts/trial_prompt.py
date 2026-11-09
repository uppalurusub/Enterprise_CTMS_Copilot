"""
==========================================================
Enterprise CTMS Copilot
Trial Planning Prompt
==========================================================
"""

from app.config.settings import settings
logger = settings.get_logger()

from langchain_core.prompts import ChatPromptTemplate


class TrialPlanningPrompt:
    """
    Prompt builder for Trial Planning Agent.
    """

    def __init__(self):

        logger.info("Initializing Trial Planning Prompt")

    def get_prompt(self) -> ChatPromptTemplate:

        logger.info("Creating Trial Planning Prompt Template")

        system_prompt = """
You are an Enterprise Clinical Trial Management System (CTMS) Copilot.

You are an expert in:

• Clinical Trial Design
• Clinical Trial Planning
• Study Protocols
• Investigator Brochure
• ICH-GCP Guidelines
• FDA Regulations
• EMA Regulations
• Site Selection
• Trial Budget Planning
• Patient Recruitment
• Risk-Based Monitoring

Your responsibilities include:

1. Answer trial planning questions.
2. Use retrieved RAG context whenever available.
3. Use SQL results whenever available.
4. Never fabricate information.
5. If information is unavailable, clearly state that.
6. Provide concise and professional responses.
7. Cite document names whenever RAG context is used.
8. Explain assumptions.
9. Suggest next actions.
10. Follow GCP guidelines.

If SQL data is provided,
summarize the results in business language.

If RAG context is provided,
use it before relying on general knowledge.

Always produce the final answer in the following format:

Summary:
...

Key Findings:
- ...

Recommendations:
- ...

Next Steps:
- ...
"""

        human_prompt = """
Question:
{question}

Trial ID:
{trial_id}

Protocol ID:
{protocol_id}

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
                ("human", human_prompt),
            ]
        )

        logger.success("Trial Planning Prompt Created")

        return prompt

    def format_prompt(
        self,
        question: str,
        trial_id: str = "",
        protocol_id: str = "",
        sql_result: str = "",
        rag_context: str = "",
        chat_history: str = "",
    ):

        logger.info("Formatting Trial Planning Prompt")

        prompt = self.get_prompt()

        return prompt.format_messages(
            question=question,
            trial_id=trial_id,
            protocol_id=protocol_id,
            sql_result=sql_result,
            rag_context=rag_context,
            chat_history=chat_history,
        )


#########################################################################
# Singleton Instance
#########################################################################

trial_prompt = TrialPlanningPrompt()