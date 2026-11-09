"""
===========================================================
Enterprise CTMS Copilot
Service Layer
===========================================================
"""

import time

from app.config.settings import settings
logger = settings.get_logger()

from app.schemas.request_model import CTMSRequest
from app.schemas.response_model import CTMSResponse

from app.implementations.ctms_impl import CTMSImplementation
import mlflow
from datetime import datetime
import time

mlflow.set_tracking_uri(
    "http://localhost:5000"
)

mlflow.set_experiment(
    "Enterprise_CTMS_Copilot_Interface"
)

class CTMSService:
    """
    Enterprise CTMS Service Layer

    Responsibilities
    ----------------
    • Validate incoming request
    • Delegate to implementation layer
    • Log execution
    • Handle service exceptions
    """

    def __init__(self):

        logger.info("Initializing CTMS Service...")

        self.ctms_impl = CTMSImplementation()

        logger.success("CTMS Service Initialized Successfully.")

    ####################################################################
    # Chat
    ####################################################################

    async def chat(
        self,
        request: CTMSRequest
    ) -> CTMSResponse:

        start_time = time.perf_counter()

        logger.info("=" * 80)
        logger.info("Processing CTMS Request")

        logger.info(f"Session ID : {request.session_id}")
        logger.info(f"User ID    : {request.user_id}")
        logger.info(f"Module     : {request.module}")
        logger.info(f"Question   : {request.question}")

        try:

            ############################################################
            # Validation
            ############################################################

            if not request.question.strip():

                raise ValueError("Question cannot be empty.")

            if request.top_k <= 0:

                raise ValueError("top_k must be greater than zero.")

            ############################################################
            # Delegate to Implementation Layer
            ############################################################

            start_ti = datetime.now()
            start_ts = time.time()

            with mlflow.start_run(
                run_name=
                f"Enterprise_CTMS_Copilot_Chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            ):
                # Log to MLflow
                mlflow.log_param(
                    "start_time",
                    start_ti.strftime("%Y-%m-%d %H:%M:%S")
                )
                mlflow.log_param(
                    "input_text",
                    request
                )

                response = await self.ctms_impl.chat(request)

                mlflow.log_param(
                    "response",
                    response
                )

                mlflow.set_tag(
                    "source",
                    "FastAPI"
                )

                mlflow.set_tag(
                    "endpoint",
                    "ctms/copilot"
                )

                end_time = datetime.now()
                end_ts = time.time()

                execution_time = end_ts - start_ts

                mlflow.log_param(
                    "end_time",
                    end_time.strftime("%Y-%m-%d %H:%M:%S")
                )

                mlflow.log_metric(
                    "execution_time_seconds",
                    round(execution_time, 4)
                )



                elapsed = round(time.perf_counter() - start_time, 2)

            logger.success(
                f"CTMS Request Completed Successfully ({elapsed} sec)"
            )

            return response

        except ValueError as ex:

            logger.error(f"Validation Error : {ex}")

            raise

        except Exception as ex:

            logger.exception("CTMS Service Failed")

            raise RuntimeError(str(ex)) from ex