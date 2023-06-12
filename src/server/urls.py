from flask import render_template, request

from app import app
from ..graph_db.repository import (
    get_nodes_and_links,
    delete_node,
    create_node,
    link_nodes,
    delete_link,
    add_router,
    get_route,
    delete_router,
    change_node_name,
    change_link_name
)


@app.route("/")
def index():
    return render_template('index.html')


# получение графа
@app.route("/graph/")
# @cache.cached(timeout=300)
def graph():
    nodes, links = get_nodes_and_links(space_name="Nodes")
    return {"nodes": nodes, "links": links}


# создание узла
@app.route("/node/create/", methods=['POST'])
def node_create():
    form = request.form
    label = form.get("label", None)
    color = form.get("color", None)

    if label:
        create_node(
            space_name="Nodes",
            params={'title': label,
                    'color': color,
                    'router': {}}
        )
    return "OK", 200


# удаление узла
@app.route("/node/delete/<int:node_id>/")
def node_delete(node_id: int):
    delete_node(space_name="Nodes", node_id=node_id)
    return "OK", 200


# удаление связи
@app.route("/link/delete/<int:link_id>/")
def link_delete(link_id: int):
    delete_link(space_name="Nodes", link_id=link_id)
    return "OK", 200


# создание связи между узлами
@app.route("/node/link/", methods=['POST'])
def node_link():
    form = request.form

    first_node = form.get("first_node", None)
    second_node = form.get("second_node", None)
    name = form.get("name", None)

    if first_node and second_node and name:
        link_nodes(
            space_name="Nodes",
            first_node=int(first_node),
            second_node=int(second_node),
            link_name=name
        )

    return "OK", 200


# добавление маршрута для узла
@app.route("/router/add/", methods=['POST'])
def router_add():
    form = request.form

    in_link = form.get('in_link', None)
    out_link = form.get('out_link', None)
    node_id = form.get('node', None)

    if in_link and out_link and node_id:
        add_router(
            space_name="Nodes",
            node_id=int(node_id),
            in_link=int(in_link),
            out_link=int(out_link)
        )

    return "OK", 200


@app.route("/graph/route/", methods=['POST'])
def route_get():
    form = request.form

    link_id = form.get('link', None)
    node_id = form.get('node', None)

    nodes = []
    links = []

    if link_id and node_id:
        nodes, links = get_route(
            space_name="Nodes",
            node_id=int(node_id),
            link_id=int(link_id)
        )

    return {
               'nodes': nodes,
               'links': links
           }, 200


@app.route("/router/delete/", methods=["GET"])
def router_delete():
    params = request.args

    node_id = params.get("node", None)
    link_in_id = params.get("route_in", None)
    link_out_id = params.get("route_out", None)

    if node_id and link_in_id and link_out_id:
        delete_router(
            space_name="Nodes",
            node_id=int(node_id),
            link_in_id=int(link_in_id),
            link_out_id=int(link_out_id)
        )

    return "OK", 200


@app.route("/node/rename/", methods=['POST'])
def node_rename():
    form = request.form

    name = form.get('name', None)
    node_id = form.get("node", None)
    color = form.get("color", None)

    if name and node_id and color:
        change_node_name(
            space_name="Nodes",
            node_id=int(node_id),
            name=name,
            color=color
        )

    return "OK", 200


@app.route("/link/rename/", methods=['POST'])
def link_rename():
    form = request.form

    name = form.get('name', None)
    link_id = form.get("link", None)

    if name and link_id:
        change_link_name(
            space_name="Nodes",
            link_id=int(link_id),
            name=name
        )

    return "OK", 200
