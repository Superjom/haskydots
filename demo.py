from dot import *

Node("node1", "base", color="red")

ClasterBegin()
register_node_class("node_class1", color="blue", fontsize=12)
Node("node2", "base", 
        color="red",
        comment="hello world")
Node("node3", "node_class1", color="red")
Node("node4", "node_class1", color="red")

ClasterEnd()

Math.output_root = "_tmp"
a1 = Math("x1", r"x^2")
print a1.img_path
