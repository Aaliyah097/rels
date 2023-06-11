new Vue({
  el: '#graph',
  data() {
    return{
      selected_node: null,
      selected_link: null,
      width: function(){
        if ($(document).width() <= 600){return $(document).width() * 0.95;}
        else{return $(document).width() * 0.6525;}
      },
      height: $(document).height() * 0.8,
      simulation: d3.forceSimulation(),
      graph: get_graph_data(),
      links: null,
      nodes: null,
      search_input: "",
      pair_node_1: null,
      pair_node_2: null,
      new_link_name: null,
      markers: null,
      link_labels: null,
      myModal: new bootstrap.Modal(document.getElementById('myModal'), {
        keyboard: false
      })
    }
  },
  computed: {
    is_active_node: function(){
      return (!this.selected_node)
    },
    is_active_link: function(){
      return (!this.selected_link)
    }
  },
  watch: {
    'search_input': {
      handler: function(v) {
        this.get_node_by_name(v);
        this.get_link_by_name(v);
      },
      deep: true
    },
  },
  mounted(){
    this.split_links();
    this.initialize_svg();
    this.initialize_simulation();

    this.initialize_markers();
    this.initialize_links();
    this.initialize_link_labels();
    this.initialize_node_labels();
    this.initialize_nodes();

  },
  methods: {
    changeLinkTitle(){
      let name_el = document.createElement("input");
      name_el.className = "form-control";
      name_el.type = "text";
      name_el.name = "link_new_name";
      name_el.id = "link_new_name";

      let modal_body = document.getElementById("modal_body");
      modal_body.innerHTML = "";

      let header = document.createElement("h5");
      header.textContent = "Новое имя"
      modal_body.appendChild(header);

      let head_text = document.getElementById("modal_title");
      head_text.textContent = `Связь ${this.selected_link.cat}`;

      let create_button = document.createElement("button");
      create_button.className = "btn btn-success";
      create_button.textContent = "Переименовать";
      create_button.type = "button";
      create_button.onclick = () => {
        rename_link(
            this.selected_link.id,
            document.getElementById("link_new_name").value
        )
      }

      let br = document.createElement("br");

      modal_body.appendChild(name_el);
      modal_body.appendChild(br);
      modal_body.appendChild(create_button);

      this.myModal.toggle();
    },
    changeNodeTitle(){
      let name_el = document.createElement("input");
      name_el.className = "form-control";
      name_el.type = "text";
      name_el.name = "node_new_name";
      name_el.id = "node_new_name";
      name_el.value = this.selected_node.title;

      let modal_body = document.getElementById("modal_body");
      modal_body.innerHTML = "";

      let header = document.createElement("h5");
      header.textContent = "Новое имя"

      let head_text = document.getElementById("modal_title");
      head_text.textContent = `Узел ${this.selected_node.title}`;

      let color_header = document.createElement("h5");
      color_header.textContent = "Новый цвет";

      let new_color = document.createElement("select");
      new_color.name = "node_new_color";
      new_color.id = "node_new_color";
      new_color.className = "form-select";
      let colors = {
        "Черный": "#000000",
        "Синий": "#0D6EFD",
        "Красный": "#DC3545",
        "Желтый": "#FFC107"
      }
      for (let color in colors){
        let option_el = document.createElement("option");
        option_el.text = color;
        option_el.value = colors[color];
        option_el.style.color = colors[color];

        if (colors[color] === this.selected_node.color){
            option_el.selected = true;
        }

        new_color.appendChild(option_el)
      }

      let create_button = document.createElement("button");
      create_button.className = "btn btn-success";
      create_button.textContent = "Применить";
      create_button.type = "button";
      create_button.onclick = () => {
          rename_node(
              this.selected_node.id,
              document.getElementById("node_new_name").value,
              document.getElementById("node_new_color").value
          )
      }

      let br = document.createElement("br");
      let br2 = document.createElement("br");

      modal_body.appendChild(header);
      modal_body.appendChild(name_el);
      modal_body.appendChild(br);
      modal_body.appendChild(br2);
      modal_body.appendChild(color_header)
      modal_body.appendChild(new_color);
      modal_body.appendChild(br);
      modal_body.appendChild(create_button);

      this.myModal.toggle();
    },
    // разделить связи на группы и присвоить каждой номер группы
    split_links(){
      for (let i = 0; i < this.graph.links.length; i++) {
        if (i !== 0 &&
            this.graph.links[i].source.id === this.graph.links[i - 1].source.id &&
            this.graph.links[i].target.id === this.graph.links[i - 1].target.id) {
          this.graph.links[i].linknum = this.graph.links[i - 1].linknum + 1;
        }
        else {
          this.graph.links[i].linknum = 1;
        }
      }
    },
    // выбрать событие
    selectRoute(){
      let modal_header = document.getElementById("modal_header");

      let head_text = document.getElementById("modal_title");
      head_text.textContent = `Узел ${this.selected_node.title}`;

      let modal_body = document.getElementById("modal_body");
      modal_body.innerHTML = "";

      let header = document.createElement("h5");
      header.textContent = "Выберите событие"
      modal_body.appendChild(header);

      let br = document.createElement("br");

      let routing_form = document.createElement("form");
      routing_form.method = "POST";
      routing_form.action = "/graph/route/";
      routing_form.onsubmit = this.getRoute;

      let outgoing_select = document.createElement("select");
      outgoing_select.name = "out_link";
      outgoing_select.id = "out_links";
      outgoing_select.className = "form-select";

      for (let i = 0; i< this.graph.links.length; i++) {
        if (this.graph.links[i].source.id === this.selected_node.id) {
          let option_el = document.createElement("option");
          option_el.text = this.graph.links[i].cat;
          outgoing_select.add(option_el);
        }
      }

      routing_form.appendChild(outgoing_select);
      routing_form.appendChild(br);

      let create_button = document.createElement("button");
      create_button.className = "btn btn-success";
      create_button.textContent = "Запустить";
      routing_form.appendChild(create_button);

      modal_body.appendChild(routing_form);

      this.myModal.toggle();

    },
    // получить цепь
    getRoute(event){
      event.preventDefault();
      let form = $(event.target);

      if (form.serializeArray().length < 1){
        return;
      }

      let link_name = form.serializeArray()[0].value;
      let link = null;

      for (let i = 0; i < this.graph.links.length; i++){
        if (this.graph.links[i].cat === link_name &&
            this.graph.links[i].source.id === this.selected_node.id){
          link = this.graph.links[i];
        }
      }

      if (link != null){
        let result = get_route(this.selected_node.id, link.id);
        this.color_chain(result[0], result[1])
      }

    },
    // выделение цепи цветом
    color_chain(nodes, links){
      d3.select("svg").selectAll('circle')
          .attr("fill", function (n){
            if (nodes.includes(n.id)){
                return "green";
            }
            else{
              return "black";
            }
          });
      d3.select("svg").selectAll('path')
          .attr("style", function (l){
            if (links.includes(l.id)){
                return "stroke: green";
            }
            else{
              return "stroke: #aaa";
            }
          })
    },
    // информация по узлу
    setRouter(event){
      event.preventDefault();
      let form = $(event.target);

      if (form.serializeArray().length < 2){
        return
      }

      let incoming_link_name = form.serializeArray()[0].value;
      let incoming_link = null;
      let outgoing_link_name = form.serializeArray()[1].value;
      let outgoing_link = null;

      for (let i = 0; i < this.graph.links.length; i++){
        if (this.graph.links[i].cat === incoming_link_name &&
            this.graph.links[i].target.id === this.selected_node.id){
          incoming_link = this.graph.links[i];
        }
        if (this.graph.links[i].cat === outgoing_link_name &&
            this.graph.links[i].source.id === this.selected_node.id){
          outgoing_link = this.graph.links[i];
        }
      }
      if (incoming_link != null && outgoing_link != null){
        add_router(
            this.selected_node.id,
            incoming_link.id,
            outgoing_link.id
        )
      }
    },
    getRouter(){
      let modal_header = document.getElementById("modal_header");
      let head_text = document.getElementById("modal_title");
      head_text.textContent = `Узел ${this.selected_node.title}`

      let modal_body = document.getElementById("modal_body");
      modal_body.innerHTML = "";

      let router = JSON.parse(this.selected_node.router);

      let header = document.createElement("h5");
      header.textContent = "Текущие маршруты";
      modal_body.appendChild(header);

      for (let key in router){
        let route_el = document.createElement("input");
        route_el.className = "form-control";
        route_el.type = "text";
        route_el.readOnly = true;

        let key_link = this.get_link_by_id(key);
        let value_link = this.get_link_by_id(router[key]);

        if (!key_link || !value_link){
          continue
        }

        route_el.value = `${key_link.cat} → ${value_link.cat}`;

        let delete_link = document.createElement("a");
        delete_link.href = "";
        delete_link.style.color = "red";
        delete_link.textContent = "удалить";
        delete_link.onclick = () =>{
          delete_router(
              this.selected_node.id,
              key_link.id,
              value_link.id
          )
          return false;
        };

        let route_block = document.createElement("div");
        route_block.id = `${this.selected_node.id}${key_link.id}${value_link.id}`;

        route_block.appendChild(route_el);
        route_block.appendChild(delete_link);

        modal_body.appendChild(route_block);

      }

      let br = document.createElement("br");
      modal_body.appendChild(br);
      let hr = document.createElement("hr");
      modal_body.appendChild(hr);

      header = document.createElement("h5");
      header.textContent = "Новый маршрут";
      modal_body.appendChild(header);

      let routing_form = document.createElement("form");
      routing_form.method = "POST";
      routing_form.action = "/router/add/";
      routing_form.onsubmit = this.setRouter;

      let incoming_select = document.createElement("select");
      incoming_select.name = "incoming_link";
      incoming_select.id = "incoming_link";
      incoming_select.className = "form-select";

      let outgoing_select = document.createElement("select");
      outgoing_select.name = "outgoing_link";
      outgoing_select.id = "outgoing_link";
      outgoing_select.className = "form-select";


      for (let i = 0; i< this.graph.links.length; i++) {
        if (this.graph.links[i].target.id === this.selected_node.id) {
          let option_el = document.createElement("option");
          option_el.text = this.graph.links[i].cat;
          incoming_select.add(option_el);
        }
        if (this.graph.links[i].source.id === this.selected_node.id) {
          let option_el = document.createElement("option");
          option_el.text = this.graph.links[i].cat;
          outgoing_select.add(option_el);
        }
      }

      let in_label = document.createElement("label");
      in_label.setAttribute("for", "incoming_link");
      in_label.textContent = "Входящее событие";

      let out_label = document.createElement("label");
      out_label.setAttribute("for", "outgoing_link");
      out_label.textContent = "Исходящее событие";

      routing_form.appendChild(in_label);
      routing_form.appendChild(incoming_select);

      br = document.createElement("br");
      routing_form.appendChild(br);

      routing_form.appendChild(out_label);
      routing_form.appendChild(outgoing_select);

      let create_button = document.createElement("button");
      create_button.className = "btn btn-success";
      create_button.textContent = "Связать";

      br = document.createElement("br");
      routing_form.appendChild(br);
      routing_form.appendChild(create_button);

      modal_body.appendChild(routing_form);

      this.myModal.toggle();
    },
    // информация по связи
    getLinkInfo(){
      let myModal = new bootstrap.Modal(document.getElementById('myModal'), {
        keyboard: false
      })
      let modal_header = document.getElementById("modal_header");
      modal_header.innerText = `Связь ${this.selected_link.cat}`;

      myModal.toggle();
    },
    // удаление связи
    deleteLink(){
      if (this.selected_link != null){
        delete_selected_link(this.selected_link.id);
      }
    },
    // удаление узла
    deleteNode(){
      if (this.selected_node != null){
        delete_selected_node(this.selected_node.id);
      }
    },
    // очистка графика
    clearSelections(event){
      if (event.target.tagName === 'svg'){
        this.selected_node = null;
        this.selected_link = null;

        this.nodes.attr('fill',function (node){ return node.color});
        this.links.attr('style', "stroke: #aaa");
        this.markers.attr('style', "fill: #aaa");
      }
    },
    // получение связи по имени
    get_link_by_name(link_name){
      let searched_link = null;
      d3.select("svg").selectAll('path')
          .each((line) => {
            if (line.cat === link_name){
              this.selectLink(line);
              searched_link = line;
            }
          });
      return searched_link;
    },
    // получение узла по имени
    get_node_by_name(node_name){
      let searched_node = null;
      d3.select("svg").selectAll('circle')
          .each((node) => {
            if (node.title === node_name){
              this.selectNode(node);
              searched_node = node;
            }
          });
      return searched_node;
    },
    // получение связи по id
    get_link_by_id(link_id){
      let searched_link = null;
      for (let i = 0; i < this.graph.links.length; i++){
        if (this.graph.links[i].id === Number(link_id)){
          searched_link = this.graph.links[i];
          break
        }
      }
      return searched_link
    },
    // связывание узлов
    linkNodes(event){
      let pair_node_1 = this.get_node_by_name(this.pair_node_1);
      let pair_node_2 = this.get_node_by_name(this.pair_node_2);

      if (this.new_link_name && pair_node_1 && pair_node_2){
        link_nodes(pair_node_1.id, pair_node_2.id, this.new_link_name);
      }
    },
    // создание узла
    createNode(event){
      create_node($(event.target));
    },
    // svg
    initialize_svg(){
      d3.select('#graph_board').select("svg").selectAll("*").remove();
      d3.select('#graph_board').select("svg")
          .attr('width', this.width())
          .attr('height', this.height)
          .style("pointer-events", "all")
      .call(d3.zoom().scaleExtent([1 / 2, 4]).on("zoom", this.zoomed))
          .append("g");

    },
    // зум
    zoomed(){
      d3.select('#graph_board').select("svg").select("g").attr("transform", d3.event.transform)
    },
    // simulation
    initialize_simulation(){
      this.simulation
          .force("link", d3.forceLink()
              .id(function (d) {
                return d.id;
              })
              //.distance(50)
              //.strength(0.5)
          )
          .force("charge", d3.forceManyBody())
          .force("center", d3.forceCenter(this.width() / 2, this.height / 2))
          .force('collision', d3.forceCollide().radius(function(d){
            return 150
          }));

      this.simulation
          .nodes(this.graph.nodes)
          .on("tick", this.ticked);

      this.simulation.force("link")
          .links(this.graph.links);

    },
    // узлы
    initialize_nodes(){
      this.nodes = d3.select('#graph_board').select("svg").select("g").append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(this.graph.nodes)
          .enter().append("circle")
          .attr("fill", function (node) {return node.color})
          .attr("id", function(node) { return "node_" + node.id})
          .attr("name", function(node) { return node.title})
          .call(d3.drag()
              .on("start", this.dragStarted)
              .on("drag", this.dragged)
              .on("end", this.dragEnded)
          )
          .on("click", this.selectNode)
    },
    // связи
    initialize_links(){
      this.links = d3.select('#graph_board').select("svg").select("g").append("g")
          .attr("class", "links")
          .selectAll("path")
          .data(this.graph.links)
          .enter().append("path")
          .attr("marker-end", function(d){return `url(#marker_${d.id})`})
          .on("click", this.selectLink)
          .attr("id", function(d, i) {
            return "link_" + d.id;
          })
      ;
    },
    // маркеры
    initialize_markers(){
      this.markers = d3.select('#graph_board').select("svg").select("g").append("g")
          .attr("class", "markers")
          .selectAll("marker")
          .append("svg:defs")
          .data(this.graph.links)
          .enter()
          .append("svg:marker")
          .attr("id", function(d) {return "marker_" + d.id})
          .attr("viewBox", "0 -3 6 6")
          .attr("refX", 11.3)
          .attr("refY", -0.2)
          .attr("markerWidth", 4)
          .attr("markerHeight", 4)
          .attr("orient", "auto")
          .append("svg:path")
          .attr("d", "M0,-3L6,0L0,3");
    },
    // подписи к связям
    initialize_link_labels(){
      this.link_labels = d3.select('#graph_board').select("svg").select("g").append("g")
          .attr("class", "links_labels")
          .selectAll(".link_label")
          .data(this.graph.links)
          .enter()
          .append("text")
          .attr("class", "link_label")
          .attr("paint-order", "stroke")
          .attr("stroke", "transparent")
          .attr("stroke-width", 4)
          .attr("stroke-opacity", 1)
          .attr("stroke-linecap", "butt")
          .attr("stroke-linejoin", "miter")
          .attr("startOffset", "50%")
          .style("text-anchor", "middle")
          .style("dominant-baseline", "central")
          .attr("xlink:href", function(d, i) {
            return "#link_" + d.id;
          })
          .text(function(d, i) {
            return d.cat + `(${d.id})`;
          });
    },
    openNodeContextMenu(selectedNode){
      this.selectNode(selectedNode);
    },
    // подписи к узлам
    initialize_node_labels(){
      this.node_labels = d3.select('#graph_board').select("svg").select("g").append('g')
          .attr("class", "labels")
          .selectAll("text")
          .data(this.graph.nodes)
          .enter().append("text")
          .text(node => node.title + `(${node.id})`)
          // .attr("dx", 15)
          // .attr("dy", 7)
    },
    // отрисовка
    ticked(){
      this.links
          .attr("d", this.get_link_coords);

      this.node_labels
          .attr("x", function (label) {
            return label.x - 20;
          })
          .attr("y", function (label) {
            return label.y -20;
          });

      this.link_labels
          .attr("x", function(d) {
            let pathLength = d3.select("#link_" + d.id).node().getTotalLength();
            d.point = d3.select("#link_" + d.id).node().getPointAtLength(pathLength / 2);
            return d.point.x
          })
          .attr("y", function(d) {
            return d.point.y
          })
      this.nodes.attr("transform", function(d) {
      return ("translate(" + d.x + "," + d.y + ")");
    });
    },
    // перемещение
    dragStarted(node) {
      if (!d3.event.active) this.simulation.alphaTarget(0.3).restart();
      node.fx = node.x;
      node.fy = node.y;
    },
    // перемещение
    dragged(node) {
      node.fx = d3.event.x;
      node.fy = d3.event.y;
    },
    // перемещение
    dragEnded(node) {
      if (!d3.event.active) this.simulation.alphaTarget(0);
      node.fx = null;
      node.fy = null;
    },
    // выбрать узел текущим
    selectNode(selectedNode) {

      this.selected_node = selectedNode;

      this.nodes.attr('fill', function (node) {
        if (node.id === selectedNode.id){
          return "green";
        }
        else{
          return node.color;
        }
      })
    },
    // выбрать связь текущим
    selectLink(selectedLink) {
      this.selected_link = selectedLink;

      this.markers.attr('style', function (link) {
        if(link.id === selectedLink.id){
          return "fill: green";
        }
        else{
          return "fill: #aaa";
        }
      })

      this.links.attr('style', function (link) {
        if(link.id === selectedLink.id){
          return "stroke: green";
        }
        else{
          return "stroke: #aaa";
        }
      })
    },
    // координаты связей
    get_link_coords(link){
      let link_groups = [];

      for (let i = 0; i < this.graph.links.length; i++){
        if (this.graph.links[i].source.id === link.source.id &&
            this.graph.links[i].target.id === link.target.id){
          link_groups.push(this.graph.links[i].id)
        }
      }

      let sign = -1;

      let median = link_groups.length / 2 + 0.5;

      let multiplier = 5 * link_groups.length;

      for (let i = 0; i <= link_groups.length; i += 1) {
        if (link_groups[i] === link.id){
          if (i + 1 < median){
            sign = -1 * link_groups.length;
            break
          }
          if (i + 1 > median){
            sign = 1
            break
          }
          else{
            sign = 0;
            break
          }
        }
      }

      multiplier = multiplier * sign;

      let dx = link.target.x - link.source.x,
          dy = link.target.y - link.source.y;

      let ds = Math.sqrt ((dx * dx) + (dy * dy));
      let qx = (dy / ds) * multiplier * link.linknum,
          qy = -(dx / ds) * multiplier * link.linknum;

      let qx1 = (link.source.x + (dx / 2)) + qx,
          qy1 = (link.source.y + (dy / 2)) + qy;
      return "M"+link.source.x+" "+link.source.y+" C" + link.source.x + " " + link.source.y + " " + qx1 + " " + qy1 + " " + link.target.x + " " + link.target.y;
    },
  }
})
