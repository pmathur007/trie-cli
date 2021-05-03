from flask import Flask, request
from py2neo import Graph, Node, Relationship

app = Flask(__name__)

graph = Graph("bolt://3.239.254.72:7687", auth=("neo4j", "troop-travel-incentive"))

def validate_input(word):
    if word is None:
        return (False, "ERROR: please enter a keyword.\n")
    if not word.isalpha():
        return (False, "ERROR: keyword must consist of letters only.\n")
    return (True, word.lower())

@app.route("/insert", methods=["PUT"])
def insert():
    keyword = request.json["keyword"]
    result, message = validate_input(keyword)
    if not result:
        return message
    keyword = message

    existingNode = graph.nodes.match(name=("_"+keyword)).first()
    if existingNode is not None and existingNode["isEnd"]:
        return f"Keyword {keyword} already exists in trie.\n"

    tx = graph.begin()
    if graph.nodes.match(name="_").first() is None:
        cur = Node("node", name="_", isEnd=False)
        tx.create(cur)
    else:
        cur = graph.nodes.match(name="_").first()
    
    for i in range(len(keyword)):
        childRel = graph.match(nodes=(cur, None), r_type=keyword[i]).first()
        if childRel is None:
            child = Node("node", isEnd=False, name=(cur["name"]+keyword[i]))
            childRel = Relationship(cur, keyword[i], child)

            tx.create(child)
            tx.create(childRel)
        else:
            child = childRel.end_node
        cur = child
    cur["isEnd"] = True
    tx.push(cur)

    tx.commit()
    return f"Successfully added {keyword} to the trie.\n"

@app.route("/delete", methods=["DELETE"])
def delete():
    keyword = request.args.get("keyword")
    result, message = validate_input(keyword)
    if not result:
        return message
    keyword = message

    tx = graph.begin()

    cur = graph.nodes.match(name=("_"+keyword)).first()
    if cur is None or not cur["isEnd"]:
        return "ERROR: keyword not found in trie.\n"
    cur["isEnd"] = False
    tx.push(cur)
    if not graph.match(nodes=(cur, None)).all():
        for i in reversed(range(0, len(keyword))):
            if cur["isEnd"] or len(graph.match(nodes=(cur, None)).all()) > 1:
                break
            tx.delete(cur)
            cur = graph.nodes.match(name=("_"+keyword[:i])).first()

    tx.commit()
    return f"Sucessfully deleted {keyword} from the trie.\n"


@app.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("keyword")
    result, message = validate_input(keyword)
    if not result:
        return message
    keyword = message
    
    kwNode = graph.nodes.match(name=("_"+keyword)).first()
    if kwNode is None or not kwNode["isEnd"]:
        return "False\n"
    return "True\n"

def dfsAutocomplete(node):
    matches = ""
    if node["isEnd"]:
        matches += node["name"][1:] + "\n"
    
    for rel in graph.match(nodes=(node, None)).all():
        matches += dfsAutocomplete(rel.end_node)
    return matches

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    prefix = request.args.get("prefix")
    result, message = validate_input(prefix)
    if not result:
        return message
    prefix = message
    
    prefixNode = graph.nodes.match(name=("_"+prefix)).first()
    if prefixNode is None:
        return "No matches.\n"
    matches = dfsAutocomplete(prefixNode)
    if matches == "":
        return "No matches\n"
    return matches


def dfsDisplay(node, depth):
    if node["name"] == "_":
        dispTrie = "_\n"
    else:
        dispTrie = "  "*depth + f" -{node['name'][-1]}-> {node['name']}{'*' if node['isEnd'] else ''}\n"

    for rel in graph.match(nodes=(node, None)).all():
        dispTrie += dfsDisplay(rel.end_node, depth+1)
    return dispTrie

@app.route("/display", methods=["GET"])
def display():
    root = graph.nodes.match(name="_").first()
    if root is None:
        return "Trie is empty.\n"
    else:
        return dfsDisplay(root, 0)
    