from dataclasses import dataclass
from neo4j.graph import Node


@dataclass
class Element:
    """model of neo4j Nodes"""

    id: int
    title: str
    router: str
    color: str

    @staticmethod
    def from_source(data: Node) -> 'Element':
        return Element(
            id=int(data.element_id),
            title=data._properties.get('title', None),
            router=data._properties.get("router", None),
            color=data._properties.get("color", None)
        )
