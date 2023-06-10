import unittest

from src.graph_db import (
    repository as graph_repo,
    link,
    element
)


class TestNeo4jRepo(unittest.TestCase):
    def test_get_graph_data(self):
        """check that all nodes and links in repo result converts correctly"""
        nodes, links = graph_repo.get_nodes_and_links("Nodes")
        self.assertTrue(
            all([type(el) == element.Element for el in nodes])
        )
        self.assertTrue(
            all([type(el) == link.Link for el in links])
        )


if __name__ == '__main__':
    unittest.main()
