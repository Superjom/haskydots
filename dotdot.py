from typing import *
from plumbum import local


class Node(object):
    count: int = 0

    classes: dict[str, List[Callable['Node', 'Node']]] = {}

    def __init__(self, graph: 'Graph', class_: str = ''):
        self.__graph: 'Graph' = graph
        self.label: str = None
        self.name: str = self.__gen_name()
        self.attrs: dict[str, Any] = {}
        if class_:
            Node.classes[class_](self)

    @staticmethod
    def add_class(name: str, func: Callable[None, 'Node']):
        Node.classes[name] = func

    def add_attr(self, key: str, value: str) -> 'Node':
        self.attrs[key] = value
        return self

    def _check_valid(self) -> None:
        assert self.name
        assert self.label

    def _connect(self, other) -> 'Edge':
        return self.__graph.add_edge(self, other)

    def __gen_name(self) -> str:
        Node.count += 1
        return 'n%d' % (Node.count)

    def __sub__(self, other: 'Node'):
        return self._connect(other)

    def __repr__(self):
        self._check_valid()

        other_attrs = []
        for item in self.attrs.items():
            other_attrs.append("%s=%s" % (item[0], item[1]))

        return '{name} [label="{label}" {other_attrs}]'.format(name=self.name,
                                                               label=self.label,
                                                               other_attrs=' '.join(other_attrs))


class Edge(object):
    classes: dict[str, List[Callable[None, 'Edge']]] = {}

    def __init__(self, node0: Node, node1: Node):
        self.source: Node = node0
        self.target: Node = node1
        self.attrs: dict[str, str] = {}

    def add_attr(self, key: str, value: str) -> None:
        self.attrs[key] = value

    @staticmethod
    def add_class(name: str, func: Callable['Edge', 'Edge']):
        Edge.classes[name] = func

    def __str__(self):
        return '{source} -> {target} [ {attrs} ]'.format(
            source=self.source.name,
            target=self.target.name,
            attrs=' '.join(["%s=%s" % (item[0], item[1]) for item in self.attrs.items()])
        )


class Graph(object):

    def __init__(self):
        self.nodes: List[Node] = []
        self.edges: dict[Tuple[Node, Node], Edge] = {}

    def add_node(self, label: str, class_: str = '') -> 'Node':
        self.nodes.append(Node(self, class_=class_))
        self.nodes[-1].label = label
        return self.nodes[-1]

    def add_edge(self, node0: Node, node1: Node, class_: str = '') -> 'Edge':
        self.edges[(node0, node1)] = Edge(node0, node1)
        return self.edges[(node0, node1)]

    def __str__(self):
        lines: List[str] = [
            "digraph G {",
        ]

        indent: int = 2
        indent_str: str = indent * ' '

        for n in self.nodes:
            lines.append(indent_str + str(n))

        for e in self.edges.items():
            lines.append(indent_str + str(e[1]))

        lines.append('}')

        return '\n'.join(lines)

    def display(self) -> None:
        code: str = str(self)
        with open('/tmp/1.dot', 'w') as f:
            f.write(code)
        dot = local["dot"]
        open_file = local["open"]
        dot["-Tpng", "/tmp/1.dot", "-o", "/tmp/1.png"]()
        open_file["/tmp/1.png"]()


if __name__ == '__main__':
    def node_class(node: Node) -> Node:
        node.add_attr("shape", "box")
        return node


    Node.add_class("class0", node_class)

    g = Graph()
    n0 = g.add_node("某个节点", 'class0')
    n1 = g.add_node("b")
    (n0 - n1).add_attr('color', 'red')

    g.display()

    print(g)
