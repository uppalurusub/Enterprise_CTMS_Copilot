"""
===========================================================
Enterprise CTMS Copilot
Application Entry Point
===========================================================
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
logger = settings.get_logger()

from app.routers.ctms_router import router as ctms_router

from app.database.db import database
from app.vectorstore.vector_db import vector_db


##############################################################################
# Application Lifecycle
##############################################################################

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("=" * 80)
    logger.info("Starting Enterprise CTMS Copilot...")

    ############################################################
    # Database Health Check
    ############################################################

    if database.health_check():

        logger.success("MySQL Connection Established")

    else:

        logger.error("Unable to connect to MySQL")

    ############################################################
    # Vector Database
    ############################################################

    try:

        info = vector_db.info()

        logger.success(
            f"Chroma Collection : {info['collection']}"
        )

        logger.info(
            f"Documents : {info['documents']}"
        )

    except Exception as ex:

        logger.exception(ex)

    logger.success("Application Startup Completed")

    yield

    ############################################################

    logger.info("Shutting Down Enterprise CTMS Copilot")

    logger.success("Shutdown Completed")


##############################################################################
# FastAPI
##############################################################################

app = FastAPI(

    title="Enterprise CTMS Copilot",

    description="""
Enterprise Clinical Trial Management System Copilot

Modules

• Trial Planning

• Budget Management

• Monitoring

• Site Management

• Patient Recruitment

Technologies

• LangChain

• Multi-Agent

• SQL Agent

• RAG

• ChromaDB

• MySQL
""",

    version="1.0.0",

    docs_url="/docs",

    redoc_url="/redoc",

    lifespan=lifespan
)

##############################################################################
# Middleware
##############################################################################

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

##############################################################################
# Routers
##############################################################################

app.include_router(ctms_router)

##############################################################################
# Root
##############################################################################

@app.get("/")
async def root():

    logger.info("Root Endpoint Invoked")

    return {

        "application": "Enterprise CTMS Copilot",

        "version": "1.0.0",

        "status": "Running"
    }


##############################################################################
# Readiness
##############################################################################

@app.get("/ready")
async def readiness():

    logger.info("Readiness Check")

    db = database.health_check()

    chroma = vector_db.info()

    return {

        "status": "READY",

        "database": db,

        "vector_store": chroma
    }


##############################################################################
# Liveness
##############################################################################

@app.get("/live")
async def liveness():

    logger.info("Liveness Check")

    return {

        "status": "ALIVE"
    }


##############################################################################
# Startup Banner
##############################################################################

logger.success("=" * 80)
logger.success("Enterprise CTMS Copilot Initialized")
logger.success("=" * 80)


