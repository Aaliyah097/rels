function get_graph_data(){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    let data;
    $.ajax(
         {
             type: 'get',
             url: '/graph/',
             headers: {'X-CSRFToken': csrf_token},
             mode: 'same-origin',
             async: false,
             success : function(json)
             {
               data = json;
             },
             error : function(xhr,errmsg,err) {
                alert('Ошибка!', 'Повторите попытку позднее.');
             },
         }
     )
    return data;
}

function delete_selected_node(node_id){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax(
         {
             type: 'get',
             url: '/node/delete/' + node_id + "/",
             headers: {'X-CSRFToken': csrf_token},

             mode: 'same-origin',
             async: false,
             success : function(json)
             {
                    window.location.href = window.location.href;
             },
             error : function(xhr,errmsg,err) {
                alert('Ошибка!', 'Повторите попытку позднее.');
             },
         }
     )
}

function create_node(form){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax(
        {
            data: form.serialize(),
            type: form.attr('method'),
            url: form.attr('action'),
            headers: {'X-CSRFToken': csrf_token},
            mode: 'same-origin',
            async: true,
            success : function(json)
            {
                window.location.href = window.location.href;
            },
            error : function(xhr,errmsg,err) {
                alert('Ошибка!', "Повторите попытку позднее.")
            }
        }
    )
}

function delete_selected_link(link_id){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax(
        {
            type: 'get',
            url: '/link/delete/' + link_id + "/",
            headers: {'X-CSRFToken': csrf_token},
            mode: 'same-origin',
            async: false,
            success : function(json)
            {
                window.location.href = window.location.href;
            },
            error : function(xhr,errmsg,err) {
                alert('Ошибка!', 'Повторите попытку позднее.');
            },
        }
    )
}


function delete_router(node_id, link_in, link_out){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax(
        {
            type: "GET",
            url: `/router/delete/?node=${node_id}&route_in=${link_in}&route_out=${link_out}`,
            headers: {'X-CSRFToken': csrf_token},
            mode: 'same-origin',
            async: true,
            success : function(json)
            {
                document.getElementById(`${node_id}${link_in}${link_out}`).remove();
            },
            error : function(xhr,errmsg,err) {
                alert('Ошибка!', "Повторите попытку позднее.")
            }
        }
    )
}


function link_nodes(first_node, second_node, link_name){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    let data = {
        "first_node": first_node,
        "second_node": second_node,
        "name": link_name
    }

    $.ajax(
        {
            data: data,
            type: "POST",
            url: "/node/link/",
            headers: {'X-CSRFToken': csrf_token},
            mode: 'same-origin',
            async: true,
            success : function(json)
            {
                window.location.href = window.location.href;
            },
            error : function(xhr,errmsg,err) {
                alert('Ошибка!', "Повторите попытку позднее.")
            }
        }
    )
}

function add_router(node_id, in_link, out_link){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    let data = {
        "in_link": in_link,
        "out_link": out_link,
        "node": node_id
    }

    $.ajax(
        {
            data: data,
            type: "POST",
            url: "/router/add/",
            headers: {'X-CSRFToken': csrf_token},
            mode: 'same-origin',
            async: true,
            success : function(json)
            {
                window.location.href = window.location.href;
            },
            error : function(xhr,errmsg,err) {
                alert('Ошибка!', "Повторите попытку позднее.")
            }
        }
    )
}


function get_route(node_id, link_id){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    let data = {
        "node": node_id,
        "link": link_id
    }

    let nodes = []
    let links = []

    $.ajax(
        {
            data: data,
            type: "POST",
            url: "/graph/route/",
            headers: {'X-CSRFToken': csrf_token},
            mode: 'same-origin',
            async: false,
            success : function(json)
            {
                links = json.links;
                nodes = json.nodes;
            },
            error : function(xhr,errmsg,err) {
                alert('Ошибка!', "Повторите попытку позднее.")
            }
        }
    )

    return [nodes, links]
}


function rename_node(node_id, name){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    let data = {
        "node": node_id,
        "name": name
    }

    $.ajax(
        {
            data: data,
            type: "POST",
            url: "/node/rename/",
            headers: {'X-CSRFToken': csrf_token},
            mode: 'same-origin',
            async: true,
            success : function(json)
            {
                window.location.href = window.location.href;
            },
            error : function(xhr,errmsg,err) {
                alert('Ошибка!', "Повторите попытку позднее.")
            }
        }
    )
}

function rename_link(link_id, name){
    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    let data = {
        "link": link_id,
        "name": name
    }

    $.ajax(
        {
            data: data,
            type: "POST",
            url: "/link/rename/",
            headers: {'X-CSRFToken': csrf_token},
            mode: 'same-origin',
            async: true,
            success : function(json)
            {
                // window.location.href = window.location.href;
            },
            error : function(xhr,errmsg,err) {
                alert('Ошибка!', "Повторите попытку позднее.")
            }
        }
    )
}