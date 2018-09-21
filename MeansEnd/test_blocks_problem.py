import unittest
import json
import blocks_problem


class Test_Info(unittest.TestCase):

    def test_operate_edge_B_to_Table (self):

        node_from = {
            "id_node" : "A-T#B-C#C-T#D-B",
            "detail" : {
                "A": "Table",
                "B": "C",
                "C": "Table",
                "D": "B"
                }
            }

        result, node_test = blocks_problem.operate_edge(node_from,["D Table"])

        self.assertEqual("Table",node_test["detail"]["A"])
        self.assertEqual("C",node_test["detail"]["B"])
        self.assertEqual("Table",node_test["detail"]["C"])
        self.assertEqual("Table",node_test["detail"]["D"])
        self.assertEqual("A-T#B-C#C-T#D-T",node_test["id_node"])
        self.assertEqual(1,result)

    def test_operate_edge_C_to_D_KO (self):
    
        node_from = {
            "id_node" : "A-T#B-C#C-T#D-B",
            "detail" : {
                "A": "Table",
                "B": "C",
                "C": "Table",
                "D": "B"
                }
            }
        edge_to = ["C D"]

        result, node_test = blocks_problem.operate_edge(node_from,edge_to)

        self.assertEqual("Table",node_test["detail"]["A"])
        self.assertEqual("C",node_test["detail"]["B"])
        self.assertEqual("Table",node_test["detail"]["C"])
        self.assertEqual("B",node_test["detail"]["D"])
        self.assertEqual(0,result)

    def test_operate_edge_2_movements_OK (self):
        
        node_from = {
            "id_node" : "A-T#B-C#C-T#D-B",
            "detail" : {
                "A": "Table",
                "B": "C",
                "C": "Table",
                "D": "B"
                }
            }
        edge_to = ["D Table", "B Table"]

        result, node_test = blocks_problem.operate_edge(node_from,edge_to)

        self.assertEqual("Table",node_test["detail"]["A"])
        self.assertEqual("Table",node_test["detail"]["B"])
        self.assertEqual("Table",node_test["detail"]["C"])
        self.assertEqual("Table",node_test["detail"]["D"])
        self.assertEqual(1,result)

    def test_distance_2 (self):

        node_from = {
            "id_node" : "A-T#B-T#C-T#D-C",
            "detail" : {
                "A": "Table",
                "B": "Table",
                "C": "Table",
                "D": "C"
                }
            }
        node_to = {
            "id_node" : "A-T#B-C#C-T#D-B",
            "detail" : {
                "A": "Table",
                "B": "C",
                "C": "Table",
                "D": "B"
                }
            }
        distance = blocks_problem.node_distance(node_from,node_to)
        self.assertEqual(distance,2)

    def test_distance_0 (self):
    
        node_from = {
            "id_node" : "A-T#B-T#C-T#D-C",
            "detail" : {
                "A": "Table",
                "D": "B",
                "B": "Table",
                "C": "Table"
                }
            }
        node_to = {
            "id_node" : "A-T#B-T#C-T#D-C",
            "detail" : {
                "A": "Table",
                "B": "Table",
                "C": "Table",
                "D": "B"
                }
            }
        distance = blocks_problem.node_distance(node_from,node_to)
        self.assertEqual(distance,0)

    def test_is_final_node_no (self):
    
        node_from = {
            "id_node" : "A-T#B-T#C-T#D-C",
            "detail" : {
                "A": "Table",
                "B": "Table",
                "C": "Table",
                "D": "C"
                }
            }
        node_to = {
            "id_node" : "A-T#B-C#C-T#D-B",
            "detail" : {
                "A": "Table",
                "B": "C",
                "C": "Table",
                "D": "B"
                }
            }
        final = blocks_problem.is_final_node(node_from,node_to)
        self.assertEqual(final,0)

    def test_is_final_node_yes (self):
    
        node_from = {
            "id_node" : "A-T#B-T#C-T#D-C",
            "detail" : {
                "A": "Table",
                "D": "B",
                "B": "Table",
                "C": "Table"
                }
            }
        node_to = {
            "id_node" : "A-T#B-T#C-T#D-C",
            "detail" : {
                "A": "Table",
                "B": "Table",
                "C": "Table",
                "D": "B"
                }
            }
        final = blocks_problem.is_final_node(node_from,node_to)
        self.assertEqual(final,1)

    def test_generate_next_nodes_3 (self):
        node_init = {
            "id_node" : "A-T#B-C#C-T#D-B",
            "detail" : {
                "A": "Table",
                "B": "C",
                "C": "Table",
                "D": "B"
                }
            }
        next_nodes = []
        new_edges = []
        next_nodes, new_edges = blocks_problem.generate_next_nodes(node_init) 

        self.assertEqual(len(next_nodes),3)
        self.assertEqual(len(new_edges),3)
        self.assertEqual(next_nodes[0]["detail"]["A"], "D")
        self.assertEqual(new_edges[0]["move"], "A D")
        self.assertEqual(next_nodes[1]["detail"]["A"], "Table")
        self.assertEqual(next_nodes[1]["detail"]["B"], "C")
        self.assertEqual(next_nodes[1]["detail"]["D"], "A")
        self.assertEqual(new_edges[1]["move"], "D A")
        self.assertEqual(next_nodes[2]["detail"]["A"], "Table")
        self.assertEqual(next_nodes[2]["detail"]["C"], "Table")
        self.assertEqual(next_nodes[2]["detail"]["D"], "Table")
        self.assertEqual(new_edges[2]["move"], "D Table")


    def test_generate_next_nodes_1 (self):
        node_init = {
            "id_node" : "A-B#B-C#C-D#D-T",
            "detail" : {
                "A": "B",
                "B": "C",
                "C": "D",
                "D": "Table"
                }
            }
        next_nodes = []
        new_edges = []
        next_nodes, new_edges = blocks_problem.generate_next_nodes(node_init) 

        self.assertEqual(len(next_nodes),1)
        self.assertEqual(len(new_edges),1)
        self.assertEqual(next_nodes[0]["id_node"], "A-T#B-C#C-D#D-T")
        self.assertEqual(next_nodes[0]["detail"]["A"], "Table")
        self.assertEqual(next_nodes[0]["detail"]["D"], "Table")
        self.assertEqual(new_edges[0]["move"], "A Table")
        self.assertEqual(new_edges[0]["src"], node_init["id_node"])
        self.assertEqual(new_edges[0]["dst"], next_nodes[0]["id_node"])



if __name__ == '__main__':
	unittest.main()