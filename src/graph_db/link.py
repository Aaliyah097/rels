from dataclasses import dataclass
from neo4j.graph import Relationship
from .element import Element


@dataclass
class Link:
    """model of neo4j Relationships"""

    id: int
    source: int
    source_el: Element
    target: int
    target_el: Element
    cat: str

    @staticmethod
    def from_source(data: Relationship) -> 'Link':
        return Link(
            id=int(data.element_id),
            source=Element.from_source(data.nodes[0]).id,
            target=Element.from_source(data.nodes[1]).id,
            source_el=Element.from_source(data.nodes[0]),
            target_el=Element.from_source(data.nodes[1]),
            cat=data.type
        )
