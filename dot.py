#encoding=gbk
import sys
import copy
import logging
import os
import inspect

cluster_no = 0
space_prefix_unit = " " * 4
cur_prefix_length = 0

node_classes = {}
edge_classes = {}

DEBUG = True

# utils
def cur_prefix_space():
    return cur_prefix_length * space_prefix_unit
def display(s, lineno=None, filename=None):
    output = cur_prefix_space() + s
    if lineno and filename:
        assert DEBUG
        output += " // %dth line from %s" % (lineno, filename)
    print output

def dic2attrs(dic):
    return ', '.join(["%s=%s" % (k,v) for k, v in dic.items()])

def register_node_class(name, **argdic):
    assert name not in node_classes
    node_classes[name] = argdic
def update_node_class(name, **argdic):
    assert name in node_classes
    node_classes[name].update(argdic)

def register_edge_class(name, **argdic):
    assert name not in edge_classes
    edge_classes[name] = argdic
def update_edge_class(name, **argdic):
    assert name in edge_classes
    edge_classes[name].update(argdic)

class _Debug(object):
    @staticmethod
    def turnon():
        global DEBUG
        DEBUG = True
    @staticmethod
    def turnoff():
        global DEBUG
        DEBUG = False
    def get_filename(self):
        assert DEBUG
        f = inspect.currentframe().f_back
        mod = f.f_code.co_filename
        return mod
    def get_lineno(self):
        assert DEBUG
        f = inspect.currentframe().f_back
        lineno = f.f_lineno
        return lineno
Debug = _Debug()

# blocks
def BlockBegin(name, **argdic):
    def dic2config(dic):
        for k,v in dic.items():
            display("%s = %s" % (k, v))
    global cur_prefix_length
    display( "%s {" % name)
    cur_prefix_length += 1
    dic2config(argdic)

def BlockEnd(name = None):
    global cur_prefix_length
    cur_prefix_length -= 1
    if name:
        display( "} // end %s" % name)
    else:
        display( "}")


def Node(name, cls_name, *al, **argdic):
    if 'comment' in argdic: 
        display("// %s" % argdic['comment'])
        del argdic['comment']
    base_attr = copy.deepcopy(node_classes[cls_name])
    base_attr['label'] = name
    base_attr.update(argdic)
    _arglist = " ".join(al)
    _argdic = dic2attrs(base_attr)
    output = "%s [ %s %s ]" % (name, _arglist, _argdic)
    mod = None; lineno = None
    if DEBUG:
        f = inspect.currentframe().f_back
        mod = f.f_code.co_filename
        lineno = f.f_lineno
    display(output, filename=mod, lineno=lineno)

def Edge(node1, node2, cls_name, **argdic):
    if 'comment' in argdic: 
        display("// %s" % argdic['comment'])
        del argdic['comment']
    base_attr = copy.deepcopy(edge_classes[cls_name])
    base_attr.update(argdic)
    base = "%s -> %s" % (node1, node2)
    if base_attr:
        base = "%s [ %s ]" % (base, dic2attrs(base_attr))
    display(base)

class Math(object):
    names = set()
    output_root = None
    def __init__(self, name, code):
        assert name not in self.names
        assert self.output_root
        self.name = name
        opath = os.path.join(self.output_root, "%s.tex" % name)
        logging.warning("write math to " + opath)
        with open(opath, 'w') as f:
            f.write(self.gen_tex_code(code))

    @property
    def img_path(self):
        return os.path.join(self.output_root, self.name + ".png")

    def set_output_root(self, root):
        self.output_root = root

    def gen_tex_code(self, code):
        code = ' '.join(code.split())
        template = '\n'.join([
            r"\documentclass[12pt]{standalone}",
            r"\usepackage{amsmath}",
            r"\DeclareMathSizes{10}{10}{10}{10}",
            r"\begin{document}",
            r"   $" + code +  r"   $",
            "\end{document}",
        ])
        return template

def math_img(name, code):
    m = Math(name, code)
    return m.img_path

register_node_class("base")
register_edge_class("base")
