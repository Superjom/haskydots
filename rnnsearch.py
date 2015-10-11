from dot import *

def repr(s):
    return '"' + s + '"'
Debug.turnon()

BlockBegin("digraph G",
    bgcolor = repr('grey'),
    style = repr('filled'),
    )

update_node_class("base", 
    shape = "plaintext",
    style = repr("rounded,filled"),
    fontname = repr("Monaco"),
    color = repr("white"),
    )
update_edge_class("base",
    fontcolor="slategray", 
    fontsize="12", 
    fontname="Monaco",
    )
register_edge_class("encoder_class",
    color = "yellow",
    fontcolor = "white",
    fontname = repr("Monaco"),
    )
register_edge_class("outer_class",
    )

Math.output_root = '_tmp/'



def NodeLabelTpl(name, kind="", size="", mathcode=""):
    '''
    paddle node with math
    '''
    tpl = ''.join(
        cur_prefix_space() + i for i in  [
        "<<table>\n",
        "   <tr><td bgcolor=\"yellow\" colspan=\"2\"><font color=\"blue\" point-size=\"18\">{name}</font></td></tr>\n",
        "   <tr><td bgcolor=\"cornsilk\">{kind}</td><td bgcolor=\"cornsilk\">{size}</td></tr>\n",
        "   <tr><td colspan=\"2\"><img src=\"{img}\"/></td></tr>\n" if mathcode else "",
        "</table>>\n",
        ])
    return tpl.format(
        name = name,
        kind = kind,
        size = size,
        img = math_img( name, mathcode) if mathcode else "",
        )

    def EdgeLabelTpl(name, mathcode=""):
        '''
        paddle edge with math
        '''
        tpl = ''.join(
            cur_prefix_space() + i for i in [
            "<<table>\n",
            "   <tr><td>{name}</td></tr>\n",
            "   <tr><td><img src=\"{img}\"/></td></tr>" if mathcode else "",
            "</table>>\n"
            ])
        return tpl.format(
            name = name,
            img = math_img( name, mathcode) if mathcode else "",
            )
###################################################
Node("raw_query_word", "base", 
        color="yellow",
        label = NodeLabelTpl(
            name = "raw_query_word",
            mathcode = "x_i",
        ))
Node("raw_query_embeding", "base", 
    label = NodeLabelTpl("raw_query_embeding",
            mathcode = "E_{x_i}", 
        )
    )
Node("new_query_word", "base", 
        color="yellow",
        label = NodeLabelTpl("new_query_word",
                kind = "DataLayer",
                size = "latent_dim",
                mathcode = r'''
                    y_{i-1}
                '''
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
            mathcode = "E{y_{i-1}}",
        )
    )

Edge("new_query_word", "new_query_embedding", "encoder_class",
        label = "TableProjection")
Edge("raw_query_word", "raw_query_embeding", "encoder_class",
        label = "TableProjection")


#  Encoder configs 
BlockBegin("subgraph cluster1",
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
        mathcode = r"\overleftarrow{h_i}"),
    )

Edge("raw_query_embeding", "annotation_forward", "encoder_class",
    label = "FullMatrixProjection")
Edge("raw_query_embeding", "annotation_backward", "encoder_class",
    label = "FullMatrixProjection")

Node("annotation", "base",
    label = NodeLabelTpl("annotation",
        kind = "concat",
        size = "2*latent_dim",
        mathcode = r'''
            h_i = \left[ 
                \begin{matrix}
                    \overrightarrow{h_i} \\
                            \overleftarrow{h_i}
                \end{matrix}
            \right]  
        '''))
Edge("annotation_forward", "annotation", "encoder_class", color="yellow")
Edge("annotation_backward", "annotation", "encoder_class")

Node("annotation_backward_last", "base", kind = "seqfirstins") 
Edge("annotation_backward", "annotation_backward_last", "encoder_class")

Node("annotation_last_projected", "base")
Edge("annotation_backward_last", "annotation_last_projected", "encoder_class", 
        label = "FullMatrixProjection")

Node("annotation_projected", "base",
        size = "latent_dim")
Edge("annotation", "annotation_projected", "encoder_class",
        label = "FullMatrixProjection")

BlockEnd("Encoder")


# decoding
BlockBegin("subgraph cluster2",
    label = "decoding_layer_group",
    style = repr("filled, rounded"),
    color = "black",
    fontcolor = "white",
    fontname="Monaco",
    )

Node("in_links", "base", color="beige")
Node("decoder_state_memory", "base",
        label = NodeLabelTpl(
            name = "decoder_state_memory",
            kind = "Memory",
            size = "latent_dim",
            mathcode = r'''
                s_{i-1}
            '''
            )
        )
Node("encoder_out_memory", "base", 
    label = NodeLabelTpl(
        name = "encoder_out_memory",
        kind = "Memory", 
        size = "sequence",
        mathcode = r'''
            h_i
        '''
    ))
Node("encoder_out_projected", "base", 
    label = NodeLabelTpl(
        name = "encoder_out_projected",
        kind = "Memory", 
        size = "latent_dim",
        mathcode = r'''
            U_a h_j
        '''
    ))
Node("decoder_state_projected", "base", 
        label = NodeLabelTpl(
            name = "decoder_state_projected",
            kind = "Memory", 
            size = "latent_dim",
        )
    )
Node("expand_decoder_state_projected", "base",
        label = NodeLabelTpl(
            name = "expand_decoder_state_projected",
            mathcode = r'''
                W_a s_{i-1}
            '''
        )
    )
Edge("decoder_state_memory", "decoder_state_projected", "encoder_class",
    label = "FullMatrixProjection")
Edge("decoder_state_projected", "expand_decoder_state_projected", "encoder_class",
    ) 
Edge("encoder_out_projected", "expand_decoder_state_projected", "encoder_class",
    label = "expand",
    )

Node("attention_vecs", "base",
        label = NodeLabelTpl(
            name = "attention_vecs",
            size = "latent_dim",
            mathcode = r'''
                W_a s_{i-1} + U_a h_j
                '''
        ))
Edge("expand_decoder_state_projected", "attention_vecs", "encoder_class",
        label = "IdentityProjection",
    )
Edge("encoder_out_projected", "attention_vecs", "encoder_class",
        label = "IdentityProjection"
    )

Node("attention_weight", "base",
        label = NodeLabelTpl(
            name = "attention_weight",
            kind = "sequence_softmax",
            mathcode = r'''
                \alpha_{ij} = \frac{\exp (e_{ij})}
                            { \sum_{k=1}^{T_x} \exp (e_{ik})}
                '''
            ))
Edge("attention_vecs", "attention_weight", "encoder_class", 
        label = "FullMatrixProjection",
        )

Node("context_vectors", "base",
        label = NodeLabelTpl(
            name = "context_vectors",
            kind = "scaling",
            mathcode = r'''
                c_i = \sum_{j=1}^{T_x} \alpha_{ij} h_j
            '''
        ))
Edge("attention_weight", "context_vectors", "encoder_class",
        )
Edge("encoder_out_memory", "context_vectors", "encoder_class",
        )

Node("context", "base",
        label = NodeLabelTpl(
            name = "context",
            kind = "average sum",
        ))
Edge("context_vectors", "context", "encoder_class")

Node("decoder_state", "base",
    label = NodeLabelTpl(
        name = "decoder_state",
        kind = "GatedRecurrentUnit",
        size = "tanh",
        mathcode = r'''
            s_i
        '''
    ))
Edge("context", "decoder_state", "encoder_class",
        label = "FullMatrixProjection")

Edge("decoder_state", "decoder_state_memory", "encoder_class",
        label="out_memory")

Node("decoder_chain", "base",
        label = NodeLabelTpl(
            name = "decoder_chain",
            kind = "tanh",
            size = "2*latent_dim",
            mathcode = r'''
                \tilde{t}_i = U_o s_{i-1} + V_o E_{y_{i-1}} + C_o c_i
            '''
        ))
Edge("context", "decoder_chain", "encoder_class",
        label = "FullMatrixProjection"
    )

Node("output", "base",
        label = NodeLabelTpl(
            name = "output",
            kind = "softmax",
            mathcode = r'''
                t_i
            '''
        ))
Edge("decoder_chain", "output", "encoder_class",
        label = "FullMatrixProjection"
    )

BlockEnd("decoding")


Edge("new_query_embedding", "decoder_state", "encoder_class",
        label = "FullMatrixProjection")
Edge("new_query_embedding", "decoder_chain", "encoder_class",
        label = "FullMatrixProjection")
Edge("new_query_embedding", "in_links", "encoder_class",
    )
Edge("annotation", "encoder_out_memory", "encoder_class",
        label = "boot", style = "dashed")
Edge("annotation_projected", "encoder_out_projected", "encoder_class",
        label = "boot", style = "dashed")
Edge("annotation_last_projected", "decoder_state_memory", "encoder_class",
        label = "boot", style = "dashed")

Node("cost", "base", 
        label = NodeLabelTpl(
            name = "cost",
            kind = "multi-class-cross-entropy",
        ),
        color = "red",
        )
Edge("output", "cost", "encoder_class")
Edge("new_query_next_word", "cost", "encoder_class")

Node("token_error_rate", "base", 
        label = NodeLabelTpl(
            name = "token_error_rate",
            kind = "classification_error",
    ))
Edge("output", "token_error_rate", "encoder_class")
Edge("new_query_next_word", "token_error_rate", "encoder_class")
    

BlockEnd("G")
