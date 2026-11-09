"""
===========================================================
Enterprise CTMS Copilot
Implementation Layer
===========================================================
"""

import time
from datetime import datetime

from app.config.settings import settings
logger = settings.get_logger()

from app.schemas.request_model import CTMSRequest
from app.schemas.response_model import (
    CTMSResponse,
    AgentExecution
)

from app.implementations.supervisor_impl import Supervisor


class CTMSImplementation:
    """
    Enterprise CTMS Implementation Layer

    Responsibilities
    ----------------
    • Invoke Supervisor
    • Execute Multi-Agent workflow
    • Build standardized response
    • Handle implementation errors
    """

    def __init__(self):

        logger.info("Initializing CTMS Implementation...")

        self.supervisor = Supervisor()

        logger.success("CTMS Implementation Initialized Successfully.")

    ####################################################################
    # Chat
    ####################################################################

    async def chat(
        self,
        request: CTMSRequest
    ) -> CTMSResponse:

        start_time = time.perf_counter()

        logger.info("=" * 80)
        logger.info("Executing Enterprise CTMS Copilot")

        try:

            ############################################################
            # Invoke Supervisor
            ############################################################

            result = await self.supervisor.invoke(request)

            elapsed = round(
                time.perf_counter() - start_time,
                2
            )

            logger.success(
                f"Execution Completed ({elapsed} sec)"
            )

            ############################################################
            # Build Response
            ############################################################

            response = CTMSResponse(

                status="success",

                message="Request processed successfully.",

                answer=result.get(
                    "answer",
                    "No response generated."
                ),

                module=result.get(
                    "module",
                    request.module
                ),

                agent=result.get(
                    "agent",
                    "Supervisor"
                ),

                sql_execution=result.get(
                    "sql_execution"
                ),

                rag_execution=result.get(
                    "rag_execution"
                ),

                recommendations=result.get(
                    "recommendations",
                    []
                ),

                follow_up_questions=result.get(
                    "follow_up_questions",
                    []
                ),

                charts=result.get(
                    "charts",
                    []
                ),

                tables=result.get(
                    "tables",
                    []
                ),

                metadata=result.get(
                    "metadata",
                    {}
                ),

                agent_execution=AgentExecution(

                    agent_name=result.get(
                        "agent",
                        "Supervisor"
                    ),

                    module=result.get(
                        "module",
                        request.module
                    ),

                    execution_time=elapsed,

                    status="Completed"

                ),

                timestamp=datetime.utcnow().isoformat()

            )

            logger.success("CTMS Response Created Successfully")

            return response

        except Exception as ex:

            logger.exception(
                "Enterprise CTMS Copilot Execution Failed"
            )

            return CTMSResponse(

                status="failed",

                message=str(ex),

                answer="Unable to process the request.",

                module=request.module,

                agent="Supervisor",

                recommendations=[],

                follow_up_questions=[],

                charts=[],

                tables=[],

                metadata={},

                timestamp=datetime.utcnow().isoformat()
            )