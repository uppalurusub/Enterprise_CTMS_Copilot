import os

from contextlib import contextmanager

from dotenv import load_dotenv

from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import URL
from sqlalchemy import text
from app.config.settings import settings
logger = settings.get_logger()

load_dotenv()


class Database:

    def __init__(self):

        self.host = os.getenv("MYSQL_HOST")
        self.port = os.getenv("MYSQL_PORT")
        self.database = os.getenv("MYSQL_DATABASE")
        self.username = os.getenv("MYSQL_USERNAME")
        self.password = os.getenv("MYSQL_PASSWORD")

        self.pool_size = int(os.getenv("DB_POOL_SIZE", 20))
        self.max_overflow = int(os.getenv("DB_MAX_OVERFLOW", 30))
        self.pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", 30))
        self.pool_recycle = int(os.getenv("DB_POOL_RECYCLE", 1800))

        self.connection_url = URL.create(
            drivername="mysql+pymysql",
            username=self.username,
            password=self.password,
            host=self.host,
            port=int(self.port),
            database=self.database,
        )

        logger.info("Initializing MySQL Database...")

        self.engine = create_engine(
            self.connection_url,
            pool_pre_ping=True,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_timeout=self.pool_timeout,
            pool_recycle=self.pool_recycle,
            future=True,
            echo=False
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

        logger.success("MySQL Database Connected Successfully.")

    def get_session(self) -> Session:
        """
        Create a new database session.
        """
        return self.SessionLocal()

    @contextmanager
    def session_scope(self):
        """
        Transaction scope.
        """

        session = self.SessionLocal()

        try:

            yield session

            session.commit()

        except SQLAlchemyError as ex:

            session.rollback()

            logger.exception(f"Database Error : {ex}")

            raise

        except Exception as ex:

            session.rollback()

            logger.exception(f"Unexpected Error : {ex}")

            raise

        finally:

            session.close()

    def health_check(self):

        try:

            with self.engine.connect() as connection:

                connection.execute(text("SELECT 1"))

            logger.success("Database Health Check Passed")

            return True

        except Exception as ex:

            logger.error(ex)

            return False


database = Database()

engine = database.engine

SessionLocal = database.SessionLocal

Base = declarative_base()