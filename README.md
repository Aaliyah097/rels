###CYPHER
- create node
- get node by id
- link two nodes
- delete node
- delete link
- get all nodes
- get all links
- set node params

**CREATE node in table (table can be not existed):**\
- `CREATE (n: TableName)`
- `CREATE (n: TableName {title: 'Title')`

**GET node by id**\
`MATCH (n: TableName) WHERE ID(n) = 1 RETURN n`

**GET nodes by property**
`MATCH (n: TableName {title: 'Title'}) RETURN n`

**DELETE table**\
`MATCH (n: TableName) DELETE n`

**SET new properties on a node**\
`MATCH (n:TableName) WHERE ID(n) = 1 SET n.title = 'Title'`

**LINK two nodes**
```
MATCH (n1:TableName), (n2:TableName)
WHERE ID(n1) = 1 AND ID(n2) = 2
CREATE (n1)-[link:LinkName]->(n2)
```

**GET all relationships**
```MATCH (n:TableName)-[r]-() RETURN r```


**GET relationship by id**
```MATCH (n:TableName)-[r]-() WHERE ID(r)=1 RETURN r```

<hr>

###LINTER

**Execute check**\
`pylint <folder or file name with extension>`

**Make conf file**\
`pylint --generate-rcfile > .pylintrc`
 
<hr>
 
###VENV
**Activate**
- on Windows: `venv/Scripts/activate`
- on Linux: `source venv/bin/activate`

**Deactivate:**\
`deactivate`

**Save packages names in file**\
`pip freeze > requirements.txt`

<hr>

###TESTS
**Run tests**\
`python tests.py`

<hr>

###RUN
**Run program**\
`python main.py`

<hr>"# rels" 
