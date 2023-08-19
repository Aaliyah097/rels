import neo4j
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os


class Neo4jConnector:
    def __init__(self, db_name: str,
                 uri: str = None,
                 user: str = None,
                 password: str = None):
        load_dotenv()

        self.driver: neo4j.Driver = GraphDatabase.driver(
            uri=uri or os.environ.get("DB_URL"),
            auth=(
                user or os.environ.get("DB_USER"),
                password or os.environ.get("PASSWORD")
            )
        )
        self.session: neo4j.Session | None = None
        self.db_name: str = db_name

    def __enter__(self) -> neo4j.Session:
        self.session = self.driver.session(database=self.db_name)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

    def __del__(self):
        if self.driver:
            self.driver.close()
