from dot import *

def repr(s):
    return '"' + s + '"'

BlockBegin("digraph G",
    bgcolor = repr('grey'),
    style = repr('filled'),
    )

def NodeLabelTpl(name, kind="", size="", mathcode=""):
    '''
    paddle node with math
    '''
    tpl = ''.join(
        cur_prefix_space() + i for i in  [
        "<<table>\n",
        "   <tr><td colspan=\"2\"><font color=\"blue\">{name}</font></td></tr>\n",
        "   <tr><td>{kind}</td><td>{size}</td></tr>\n",
        "   <tr><td colspan=\"2\"><img src=\"{img}\"/></td></tr>\n" if mathcode else "",
        "</table>>\n",
        ])
    return tpl.format(
        name = name,
        kind = kind,
        size = size,
        img = math_img( name, mathcode) if mathcode else "",
        )

update_node_class("base", 
    shape = "record",
    style = repr("rounded,filled"),
    fontname = repr("Monaco"),
    color = repr("white"),
    )
update_edge_class("base",
    fontcolor="slategray", 
    fontsize="12", 
    fontname="Monaco",
    )
Math.output_root = '_tmp/'


###################################################
Node("raw_query_word", "base", 
        color="yellow")
Node("raw_query_embeding", "base", 
    label = NodeLabelTpl("raw_query_embeding",
            mathcode = "x_i", 
        )
    )
Node("new_query_word", "base", 
        color="yellow",
        label = NodeLabelTpl("new_query_word",
                "DataLayer",
                "latent_dim",
            ),
    )
Node("new_query_next_word", "base",
    label = NodeLabelTpl("new_query_next_word",
        "DataLayer",
        ),
    color = "yellow"
    )
Node("new_query_embedding", "base",
    label = NodeLabelTpl("new_query_embedding",
            mathcode = "y_i",
        )
    )

Edge("new_query_word", "new_query_embedding", "base",
        label = "TableProjection")
Edge("raw_query_word", "raw_query_embeding", "base",
        label = "TableProjection")


#  Encoder configs 
BlockBegin("subgraph Encoder",
    label = "Encoder",
    color = "black",
    style = repr("filled, rounded"),
    )

Node("annotation_forward", "base",
    label = NodeLabelTpl("annotation_forward",
        kind = "GatedRecurrentLayerGroup",
        mathcode = r"\overrightarrow{h_i}")
    )
Node("annotation_backward", "base",
    label = NodeLabelTpl("annotation_backward",
        kind = "GatedRecurrentLayerGroup",
        mathcode = r"\overleftarrow{h_i}")
    )

Edge("raw_query_embeding", "annotation_forward", "base",
    label = "FullMatrixProjection")
Edge("raw_query_embeding", "annotation_backward", "base",
    label = "FullMatrixProjection")

Node("annotation", "base",
    label = NodeLabelTpl("annotation",
        mathcode = r'''
            \left[ 
                \begin{matrix}
                    \overrightarrow{h_i} \\
                            \overleftarrow{h_i}
                \end{matrix}
            \right]  
        '''))
Edge("annotation_forward", "annotation", "base")
Edge("annotation_backward", "annotation", "base")

Node("annotation_backward_last", "base", kind = "seqfirstins") 
Edge("annotation_backward", "annotation_backward_last", "base")

Node("annotation_last_projected", "base")
Edge("annotation_backward_last", "annotation_last_projected", "base", 
        label = "FullMatrixProjection")

BlockEnd("Encoder")
    

BlockEnd("G")
