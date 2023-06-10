from itertools import zip_longest

from .connector import Neo4jConnector
from .element import Element
from .link import Link
import json


def get_nodes_and_links(space_name: str) -> tuple[list[Element], list[Link]]:
    """get data to plot graph of concrete space"""

    request = f"""MATCH (n:{space_name}) OPTIONAL MATCH (n)-[r]-() RETURN n, r"""

    with Neo4jConnector(db_name="neo4j") as session:
        response = session.run(request)

        nodes, links = [], []

        for node, link in zip_longest(response.graph().nodes, response.graph().relationships):
            if node is not None:
                nodes.append(Element.from_source(node))
            if link is not None:
                links.append(Link.from_source(link))
        return nodes, links


def delete_node(space_name: str, node_id: int):
    request = f"""
        MATCH (n:{space_name}) WHERE ID(n)={node_id} OPTIONAL MATCH ()-[r1]->(n) OPTIONAL MATCH (n)-[r2]->() RETURN r1, r2, n
    """

    with Neo4jConnector(db_name="neo4j") as session:
        result = session.run(request)
        for r in result.graph().relationships:
            delete_link(space_name, int(r.element_id))

        for n in result.graph().nodes:
            if int(n.element_id) == node_id:
                request = f"""MATCH (n:{space_name}) WHERE ID(n)={node_id} DELETE n"""
                session.run(request)


def delete_link(space_name: str, link_id: int):
    request = f"""MATCH (n:{space_name})-[r]-() WHERE ID(r)={link_id} DELETE r"""

    with Neo4jConnector(db_name="neo4j") as session:
        session.run(request)

        request = f"""MATCH (n:{space_name}) RETURN n"""

        nodes = session.run(request).graph().nodes

        for node in nodes:
            router = node._properties.get('router', {})
            router = dict(json.loads(router))

            for_del_keys = []
            for key, value in router.items():
                if int(key) == link_id or int(value) == link_id:
                    for_del_keys.append(key)

            for key in for_del_keys:
                del router[key]

            request = f"""MATCH (n:{space_name}) WHERE ID(n)={node.element_id} 
                                   SET n.router = '{json.dumps(router)}'
                                   """

            session.run(request)


def create_node(space_name: str, params: dict):
    params_string = ",".join(f"{key}:'{str(value).replace(' ', '_')}'" for key, value in params.items())
    params_string = "{" + params_string + "}"

    request = f"""CREATE (n:{space_name} {params_string})"""

    with Neo4jConnector(db_name="neo4j") as session:
        session.run(request)


def link_nodes(space_name: str, first_node: int, second_node: int, link_name: str):
    link_name = link_name.replace(" ", "_")
    request = f"""
        MATCH (n1: {space_name}) WHERE ID(n1)={first_node} 
        MATCH (n2: {space_name}) WHERE ID(n2)={second_node}
        MATCH (n1)-[r]-(n2)
        RETURN r
    """
    with Neo4jConnector(db_name="neo4j") as session:
        response = session.run(request)
        for link in response.graph().relationships:
            if link.type == link_name:
                break
        else:
            request = f"""
                MATCH (n1:{space_name}), (n2:{space_name})
                WHERE ID(n1) = {first_node} AND ID(n2) = {second_node}
                CREATE (n1)-[link:{link_name}]->(n2)
            """

            session.run(request)


def add_router(space_name: str, node_id: int, in_link: int, out_link: int):
    request = f"""MATCH (n:{space_name}) WHERE ID(n)={node_id} RETURN n"""

    with Neo4jConnector(db_name='neo4j') as session:
        response = session.run(request)
        for node in response.graph().nodes:
            router = node._properties.get('router', {})
            router = dict(json.loads(router))

            router[str(in_link)] = str(out_link)

            request = f"""MATCH (n:{space_name}) WHERE ID(n)={node_id} 
            SET n.router = '{json.dumps(router)}'
            """

            session.run(request)


def delete_router(space_name: str, node_id: int, link_in_id: int, link_out_id: int):
    request = f"""MATCH (n:{space_name}) WHERE ID(n)={node_id} RETURN n"""

    with Neo4jConnector(db_name='neo4j') as session:
        response = session.run(request)
        for node in response.graph().nodes:
            router = node._properties.get('router', {})
            router = dict(json.loads(router))

            del router[str(link_in_id)]

            request = f"""MATCH (n:{space_name}) WHERE ID(n)={node_id} 
                        SET n.router = '{json.dumps(router)}'
                        """

            session.run(request)


def get_route(space_name: str, node_id: int, link_id: int) -> tuple[list[int], list[int]]:
    # все узлы и связи
    nodes, links = get_nodes_and_links(space_name)

    # текущий узел и текущая связь
    node = [n for n in nodes if n.id == node_id][0]
    link = [l for l in links if l.id == link_id][0]

    # истори\ перемещения по узлам и связям
    node_moves = [node, ]
    link_moves = [link, ]

    current_link = link

    while current_link:
        # следующий узел от текущего
        next_node = [n for n in nodes if n.id == current_link.target_el.id][0]
        node_moves.append(next_node)

        router = dict(json.loads(next_node.router))
        next_link_id = router.get(str(current_link.id), None)

        if next_link_id:
            next_link = [l for l in links if l.id == int(next_link_id) and l.source_el.id == next_node.id][0]
            link_moves.append(next_link)
            current_link = next_link
        else:
            current_link = None

    return [n.id for n in node_moves], [l.id for l in link_moves]


def change_node_name(space_name: str, node_id: int, name: str):
    request = f"""MATCH (n:{space_name}) WHERE ID(n) = {node_id} SET n.title = '{name}'"""

    with Neo4jConnector(db_name='neo4j') as session:
        session.run(request)


def change_link_name(space_name: str, link_id: int, name: str):
    request = f"""MATCH (n:{space_name})-[r]-() WHERE ID(r)={link_id} SET r.type = '{name}'"""

    with Neo4jConnector(db_name='neo4j') as session:
        session.run(request)
