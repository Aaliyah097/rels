import neo4j
from neo4j import GraphDatabase


class Neo4jConnector:
    def __init__(self, db_name: str,
                 uri: str = "bolt://83.167.124.57:7687",
                 user: str = "neo4j",
                 password: str = "aaoem097"):
        self.driver: neo4j.Driver = GraphDatabase.driver(uri=uri, auth=(user, password))
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
