import json

semantic_init = {
 "nodes": [
  {
   "id_node" : "3#3#0#0#left",
   "guards_left": "3",
   "prision_left": "3",
   "guards_right": "0",
   "prision_right": "0",
   "boat" : "left",
   "final" : "no"
  }
 ],
 "edges": [
 ]
}

def operate_edge (node_init, edge):
    number_guards = edge["number_guards"]
    number_prision = edge["number_prision"]

    new_node = move_guards_prision (node_init, number_guards, number_prision)

    new_node["final"] = "yes" if is_final_node(new_node)==1 else "no"

    return new_node


def move_guards_prision (node_init, number_guards, number_prision):
    
    boat = "right" if node_init["boat"]=="left" else "left"
    if boat == "right":
        guards_right = int(node_init["guards_right"]) + number_guards
        prision_right = int(node_init["prision_right"]) + number_prision
        guards_left = int(node_init["guards_left"]) - number_guards
        prision_left = int(node_init["prision_left"]) - number_prision
    else:
        guards_left = int(node_init["guards_left"]) + number_guards
        prision_left = int(node_init["prision_left"]) + number_prision
        guards_right = int(node_init["guards_right"]) - number_guards
        prision_right = int(node_init["prision_right"]) - number_prision
    
    new_node = {
        "id_node" : ""+str(guards_left)+"#"+str(prision_left)+"#"+str(guards_right)+"#"+str(prision_right)+"#"+str(boat),
        "guards_left": str(guards_left),
        "prision_left": str(prision_left),
        "guards_right": str(guards_right),
        "prision_right": str(prision_right),
        "boat" : str(boat),
        "final" : "no"
    }

    return new_node

def validate_node (node_init):
    guards_left = int(node_init["guards_left"]) 
    prision_left = int(node_init["prision_left"]) 
    guards_right = int(node_init["guards_right"]) 
    prision_right = int(node_init["prision_right"]) 

    if ((prision_right > guards_right) and (guards_right > 0)) or ((prision_left > guards_left) and (guards_left > 0)):
        return 0
    else:
        return 1

def exists_node (node_init, list_nodes):
    for node in list_nodes:
        if node["id_node"] == node_init["id_node"]:
            return 1
    return 0

def exists_edge (edge_init, list_edge):
    for edge in list_edge:
        if (edge["src"] == edge_init["src"]) and (edge["dst"] == edge_init["dst"] )and (edge["prision"] == edge_init["prision"]) and (edge["guards"] == edge_init["guards"]):
            return 1
        if (edge["src"] == edge_init["dst"]) and (edge["dst"] == edge_init["src"] )and (edge["prision"] == edge_init["prision"]) and (edge["guards"] == edge_init["guards"]):
            return 1
    return 0


def insert_node (node, semantic_network):
    if exists_node (node, semantic_network["nodes"]) == 0:
        semantic_network["nodes"].append(node)
        return 1, semantic_network
    else:
        return 0, semantic_network

def insert_edge (edge, semantic_network):
    if exists_edge (edge, semantic_network["edges"]) == 0:
        semantic_network["edges"].append(edge)
        return 1, semantic_network
    else:
        return 0, semantic_network

def is_final_node (node_init):
    guards_left = int(node_init["guards_left"]) 
    prision_left = int(node_init["prision_left"]) 
    guards_right = int(node_init["prision_right"]) 
    prision_right = int(node_init["prision_right"]) 

    if (prision_left == 0) and (guards_left == 0) and (guards_right > 0) and (prision_right > 0):
        return 1
    else:
        return 0
    
def generate_next_nodes (node_init):
    boat = node_init["boat"]
    guards = int(node_init["guards_left"] if node_init["boat"]=="left" else node_init["guards_right"])
    prision = int(node_init["prision_left"] if node_init["boat"]=="left" else node_init["prision_right"])
    new_nodes = []
    new_edge = []

    for i_guards in range(0,guards+1):
        for i_prision in range(0,prision+1):
            if (i_prision + i_guards) <=2 and (i_prision + i_guards) >0 :
                new_node = move_guards_prision (node_init, i_guards, i_prision)
                if validate_node(new_node) == 1:
                    new_nodes.append(new_node)
                    edge = {
                        "src" : node_init["id_node"],
                        "dst" : new_node["id_node"],
                        "prision" : str(i_prision),
                        "guards" : str(i_guards),
                        "boat" : "right" if boat=="left" else "left"
                    }
                    new_edge.append(edge)
    return new_nodes, new_edge
#new_node = move_guards_prision (semantic_init["nodes"][0], 2, 2)
#print (new_node)

queue_nodes = []
queue_nodes.append(semantic_init["nodes"][0])

while len(queue_nodes) != 0:
    node_i = queue_nodes.pop(0)
    if node_i["final"]=="no":
        new_nodes, new_edge = generate_next_nodes (node_i)

        for node in new_nodes:
            new, semantic_init = insert_node(node, semantic_init)
            if new == 1:
                queue_nodes.append(node)

        for edge in new_edge:
            new, semantic_init = insert_edge(edge, semantic_init)

print semantic_init

