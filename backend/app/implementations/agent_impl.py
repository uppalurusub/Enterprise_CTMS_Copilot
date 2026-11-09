"""
===========================================================
Enterprise CTMS Copilot
Base Agent Implementation
===========================================================
"""

import time
from abc import ABC
from abc import abstractmethod

from app.config.settings import settings
logger = settings.get_logger()



from app.implementations.rag_impl import rag

from app.implementations.sql_impl import sql_agent

from app.observability.langsmith_usage import invoke_llm_with_usage
from langsmith import traceable

class BaseAgent(ABC):
    """
    Base Class for all CTMS Agents

    TrialAgent
    BudgetAgent
    MonitoringAgent
    SiteAgent
    RecruitmentAgent
    """

    def __init__(
        self,
        agent_name: str,
        prompt
    ):

        self.agent_name = agent_name

        self.prompt = prompt

        self.rag = rag

        self.sql = sql_agent

        self.llm = settings.get_model_client()

        logger.info(f"{agent_name} Initialized.")

    ##################################################################
    # Main Execution
    ##################################################################

    @traceable(name="CTMS Agent Execution", run_type="chain")
    async def execute(self, request):

        logger.info("=" * 80)
        logger.info(f"{self.agent_name} Started")

        start = time.perf_counter()

        try:

            ###########################################################
            # SQL
            ###########################################################

            sql_result = ""

            sql_execution = None

            if request.enable_sql_agent:

                logger.info("Executing SQL Agent")

                sql_response = self.sql.ask(
                    request.question
                )

                sql_result = sql_response.get(
                    "output",
                    ""
                )

                sql_execution = {
                    "executed": True,
                    "query": sql_response.get(
                        "intermediate_steps",
                        ""
                    ),
                    "rows_returned": 0,
                    "data": []
                }

            ###########################################################
            # RAG
            ###########################################################

            rag_context = ""

            rag_execution = None

            if request.enable_rag:

                logger.info("Executing RAG")

                rag_result = self.rag.retrieve(

                    question=request.question,

                    top_k=request.top_k,

                    metadata=request.filters

                )

                rag_context = rag_result["context"]

                rag_execution = rag_result[
                    "rag_execution"
                ]

            ###########################################################
            # Prompt
            ###########################################################

            logger.info("Building Prompt")

            messages = self.build_prompt(

                request=request,

                sql_result=sql_result,

                rag_context=rag_context
            )

            ###########################################################
            # LLM
            ###########################################################

            logger.info("Calling LLM")

            response, llm_usage = invoke_llm_with_usage(
                self.llm,
                messages,
                agent_name=self.agent_name,
            )

            elapsed = round(

                time.perf_counter() - start,

                2
            )

            logger.success(

                f"{self.agent_name} Finished ({elapsed}s)"

            )

            ###########################################################
            # Return
            ###########################################################

            return {

                "module": self.module_name(),

                "agent": self.agent_name,

                "answer": response.content,

                "sql_execution": sql_execution,

                "rag_execution": rag_execution,

                "recommendations": [],

                "follow_up_questions": [],

                "charts": [],

                "tables": [],

                "metadata": {
                    "execution_time": elapsed,
                    "llm_usage": llm_usage,
                }
            }

        except Exception as ex:

            logger.exception(ex)

            raise

    ##################################################################
    # Build Prompt
    ##################################################################

    @abstractmethod
    def build_prompt(
        self,
        request,
        sql_result,
        rag_context
    ):
        """
        Implemented in child class
        """

    ##################################################################
    # Module Name
    ##################################################################

    @abstractmethod
    def module_name(self):
        """
        Implemented in child class
        """