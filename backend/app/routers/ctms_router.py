"""
===========================================================
Enterprise CTMS Copilot
FastAPI Router
===========================================================
"""

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from app.config.settings import settings
logger = settings.get_logger()

from app.schemas.request_model import CTMSRequest
from app.schemas.response_model import CTMSResponse

from app.services.ctms_service import CTMSService


router = APIRouter(
    prefix="/api/v1/ctms",
    tags=["Enterprise CTMS Copilot"]
)

service = CTMSService()


###########################################################################
# Enterprise CTMS Copilot
###########################################################################

@router.post(
    "/copilot",
    response_model=CTMSResponse,
    summary="Enterprise CTMS Copilot"
)
async def enterprise_ctms_copilot(
    request: CTMSRequest
):
    """
    Enterprise CTMS Copilot

    Supports

    • Trial Planning

    • Budget Management

    • Monitoring

    • Site Management

    • Patient Recruitment

    • SQL Agent

    • RAG

    • Multi-Agent

    """

    logger.info("=" * 80)
    logger.info("Received Enterprise CTMS Copilot Request")

    logger.info(f"Session ID : {request.session_id}")
    logger.info(f"User ID    : {request.user_id}")
    logger.info(f"Module     : {request.module}")
    logger.info(f"Question   : {request.question}")

    try:

        response = await service.chat(request)

        logger.success("Enterprise CTMS Request Completed Successfully")

        return response

    except ValueError as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex)
        )

    except RuntimeError as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error occurred."
        )


###########################################################################
# Health Check
###########################################################################

@router.get(
    "/health",
    summary="Health Check"
)
async def health():

    logger.info("Health Check Requested")

    return {
        "status": "UP",
        "service": "Enterprise CTMS Copilot"
    }


###########################################################################
# Available Modules
###########################################################################

@router.get(
    "/modules",
    summary="Available CTMS Modules"
)
async def modules():

    logger.info("Listing Available Modules")

    return {

        "modules": [

            {
                "name": "trial_planning",
                "description": "Clinical Trial Planning Agent"
            },

            {
                "name": "budget_management",
                "description": "Clinical Trial Budget Agent"
            },

            {
                "name": "monitoring",
                "description": "Monitoring Agent"
            },

            {
                "name": "site_management",
                "description": "Clinical Site Management Agent"
            },

            {
                "name": "patient_recruitment",
                "description": "Patient Recruitment Agent"
            }

        ]
    }


###########################################################################
# Agent Information
###########################################################################

@router.get(
    "/agents",
    summary="Registered Agents"
)
async def agents():

    logger.info("Returning Registered Agents")

    return {

        "supervisor": "Enterprise Supervisor",

        "agents": [

            "Trial Planning Agent",

            "Budget Management Agent",

            "Monitoring Agent",

            "Site Management Agent",

            "Patient Recruitment Agent",

            "SQL Agent",

            "RAG Agent"
        ]
    }