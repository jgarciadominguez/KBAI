import json

semantic_init = {
 "nodes": [
    {
    "id_node" : "A-T#B-C#C-T#D-B",
    "detail" : {
        "A": "Table",
        "B": "C",
        "C": "Table",
        "D": "B"
        },
    "final" : "no"
    }
 ],
 "edges": [
    ]
}

goal_node =     {
    "id_node" : "A-B#B-C#C-D#D-T",
    "detail" : {
        "A": "B",
        "B": "C",
        "C": "D",
        "D": "Table"
        }
    }


def generate_id_node (detail):
    return ("A"+"-"+detail["A"][:1]+"#"+"B"+"-"+detail["B"][:1]+"#"+"C"+"-"+detail["C"][:1]+"#"+"D"+"-"+detail["D"][:1])


def is_on_top (node, block_selected):
    for block, on_block in node["detail"].iteritems():
        if str(on_block) == block_selected:
            return 0
    return 1

def operate_edge (node_init, edge):

    A = node_init["detail"]["A"]
    B = node_init["detail"]["B"]
    C = node_init["detail"]["C"]
    D = node_init["detail"]["D"]

    new_node = node_init

    for e in edge:
        block = e.split(" ")[0]
        on_block = e.split(" ")[1]

        if is_on_top(new_node, block)==1:
            if block == "A":
                A = on_block
            if block == "B":
                B = on_block
            if block == "C":
                C = on_block
            if block == "D":
                D = on_block
            
            new_node = {
                "id_node" : "A"+"-"+A[:1]+"#"+"B"+"-"+B[:1]+"#"+"C"+"-"+C[:1]+"#"+"D"+"-"+D[:1],
                "detail" : {
                    "A": A,
                    "B": B,
                    "C": C,
                    "D": D
                },
                "final" : "no"
            }
        else:
            return 0,node_init

    result = 1

    return result, new_node

def validate_node (node_init):
    return 1

def exists_node (node_init, list_nodes):
    for node in list_nodes:
        if node["id_node"] == node_init["id_node"]:
            return 1
    return 0

def exists_edge (edge_init, list_edge):
    for edge in list_edge:
        if (edge["src"] == edge_init["src"]) and (edge["dst"] == edge_init["dst"] ):
            return 1
        if (edge["src"] == edge_init["dst"]) and (edge["dst"] == edge_init["src"] ):
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

def is_final_node (node_init, node_end):
    if node_distance (node_init, node_end) == 0:
        return 1
    else:
        return 0

def node_distance (node_init, node_end):
    
    distance = 0

    for block, on_block in node_init["detail"].iteritems():
        if on_block != node_end["detail"][block]:
            distance = distance + 1

    return distance 

def generate_next_nodes (node_init):
    moves = []
    new_edges = []
    nodes = []

    for block, on_block in node_init["detail"].iteritems():
        if (is_on_top(node_init,block)):
            for to_block, to_onblock in node_init["detail"].iteritems():
                if (block != to_block) and (is_on_top(node_init, to_block)) and ( block+" "+to_block != block+" "+on_block):  
                        moves.append(block+" "+to_block)
            if (on_block != "Table"):
                moves.append(block+" "+"Table")
    
    for move in moves:
        v_move = []
        v_move.append (move)
        result, new_node = operate_edge(node_init,v_move)
        if result == 1:
            nodes.append(new_node)
            edge = {
                "src" : node_init["id_node"],
                "dst" : new_node["id_node"],
                "move" : str(move),
            }
            new_edges.append(edge)
    
    return nodes,new_edges

queue_nodes = []
queue_nodes.append(semantic_init["nodes"][0])
end = "no"
best_distance = 999
best_node = {}

while end == "no":
    node_i = queue_nodes.pop(0)
    if node_distance(node_i,goal_node) != 0:
        new_nodes, new_edge = generate_next_nodes (node_i)

        for node in new_nodes:
            actual_distance = node_distance(node, goal_node)
            if actual_distance <= best_distance:
                best_node = node
                best_distance = actual_distance
        new, semantic_init = insert_node(best_node, semantic_init)
        if new == 1:
            queue_nodes.append(node)
        else:
            end = "yes"

        for edge in new_edge:
            if edge["src"] == node_i["id_node"] and edge["dst"] == best_node["id_node"]:
                new, semantic_init = insert_edge(edge, semantic_init)
    else:
        end = "yes"
        node_i["final"] = "yes"

print semantic_init