"""
===========================================================
Enterprise CTMS Copilot
SQL Agent Implementation
===========================================================
"""

from typing import Any, Dict, List

from sqlalchemy import text

from app.config.settings import settings
logger = settings.get_logger()
from langchain_classic.agents import AgentExecutor

from langchain_openai import ChatOpenAI

from langchain_community.utilities import SQLDatabase

from langchain_community.agent_toolkits import create_sql_agent

from app.database.db import database


class SQLImplementation:
    """
    Enterprise SQL Implementation

    Responsibilities

    • Execute SQL

    • Natural Language → SQL

    • LangChain SQL Agent

    • Query Validation

    • Return Structured Results
    """

    def __init__(self):

        logger.info("Initializing SQL Implementation...")

        self.engine = database.engine

        self.sql_db = SQLDatabase(self.engine)

        self.llm = settings.get_model_client()

        self.agent = create_sql_agent(

            llm=self.llm,

            db=self.sql_db,

            verbose=True,
            agent_executor_kwargs={
                "handle_parsing_errors": True
            }
        )

        logger.success("SQL Implementation Initialized Successfully.")

    ####################################################################
    # Execute SQL
    ####################################################################

    def execute_query(
        self,
        sql: str
    ) -> List[Dict[str, Any]]:

        logger.info("Executing SQL Query")

        logger.debug(sql)

        try:

            with database.session_scope() as session:

                result = session.execute(
                    text(sql)
                )

                rows = result.mappings().all()

                data = [dict(row) for row in rows]

                logger.success(
                    f"{len(data)} rows returned."
                )

                return data

        except Exception as ex:

            logger.exception(ex)

            raise

    ####################################################################
    # Execute Scalar
    ####################################################################

    def execute_scalar(
        self,
        sql: str
    ):

        logger.info("Executing Scalar Query")

        with database.session_scope() as session:

            result = session.execute(
                text(sql)
            )

            return result.scalar()

    ####################################################################
    # Execute Non Query
    ####################################################################

    def execute_non_query(
        self,
        sql: str
    ):

        logger.info("Executing Update/Delete Query")

        with database.session_scope() as session:

            session.execute(
                text(sql)
            )

        logger.success("Statement Executed Successfully.")

    ####################################################################
    # Natural Language → SQL
    ####################################################################

    def ask(
        self,
        question: str
    ):

        logger.info("Executing LangChain SQL Agent")

        response = self.agent.invoke(

            {
                "input": question
            }

        )

        logger.success("SQL Agent Completed.")

        return response

    ####################################################################
    # Validate SQL
    ####################################################################

    def validate_query(
        self,
        sql: str
    ) -> bool:

        logger.info("Validating SQL")

        sql = sql.strip().lower()

        blocked = [

            "drop ",

            "truncate ",

            "delete ",

            "alter ",

            "grant ",

            "revoke "

        ]

        for keyword in blocked:

            if keyword in sql:

                logger.warning(
                    f"Blocked SQL : {keyword}"
                )

                return False

        return True

    ####################################################################
    # Explain Query
    ####################################################################

    def explain(
        self,
        sql: str
    ):

        logger.info("Generating Execution Plan")

        return self.execute_query(

            f"EXPLAIN {sql}"

        )

    ####################################################################
    # Show Tables
    ####################################################################

    def show_tables(self):

        logger.info("Fetching Tables")

        return self.execute_query(

            "SHOW TABLES"

        )

    ####################################################################
    # Describe Table
    ####################################################################

    def describe_table(
        self,
        table_name: str
    ):

        logger.info(
            f"Describe Table : {table_name}"
        )

        return self.execute_query(

            f"DESCRIBE {table_name}"

        )


##########################################################################
# Singleton Instance
##########################################################################

class _LazySQLImplementation:
    """Initialize the SQL agent only when an SQL operation is requested."""

    def __init__(self):
        self._instance = None

    def _get_instance(self):
        if self._instance is None:
            self._instance = SQLImplementation()
        return self._instance

    def __getattr__(self, name):
        return getattr(self._get_instance(), name)


sql_agent = _LazySQLImplementation()