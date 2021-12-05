from dataclasses import dataclass


def make_tokens(text):
    return list(filter(lambda char: char in '+-,.<>[]', text))


class Node:
    pass


class IncrementNode(Node):
    pass


class DecrementNode(Node):
    pass


class MoveLeftNode(Node):
    pass


class MoveRightNode(Node):
    pass


class PrintCellNode(Node):
    pass


class GetInputNode(Node):
    pass


@dataclass
class LoopNode:
    nodes: list[Node]

    def __repr__(self):
        return str(self.nodes)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_tok = None
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.current_tok = self.tokens[self.tok_idx] \
            if self.tok_idx < len(self.tokens) \
            else None

    def parse(self):
        return self.instruction()

    def instruction(self, in_loop=False):
        nodes = []
        while self.current_tok is not None:
            if self.current_tok == '+':
                nodes.append(IncrementNode())
                self.advance()
            elif self.current_tok == '-':
                nodes.append(DecrementNode())
                self.advance()
            elif self.current_tok == '<':
                nodes.append(MoveLeftNode())
                self.advance()
            elif self.current_tok == '>':
                nodes.append(MoveRightNode())
                self.advance()
            elif self.current_tok == '.':
                nodes.append(PrintCellNode())
                self.advance()
            elif self.current_tok == ',':
                nodes.append(GetInputNode())
                self.advance()
            elif self.current_tok == '[':
                self.advance()
                nodes.append(LoopNode(self.instruction(True)))
            elif self.current_tok == ']':
                self.advance()
                if in_loop:
                    return nodes
                raise Exception('Invalid syntax')
        return nodes


@dataclass
class Context:
    pointer: int
    storage: list[int]


def evaluate(nodes, context=None):
    if context is None:
        context = Context(0, [0])
    for node in nodes:
        if isinstance(node, IncrementNode):
            context.storage[context.pointer] += 1
        elif isinstance(node, DecrementNode):
            if context.storage[context.pointer] > 0:
                context.storage[context.pointer] -= 1
        elif isinstance(node, MoveLeftNode):
            if context.pointer > 0:
                context.pointer -= 1
        elif isinstance(node, MoveRightNode):
            context.pointer += 1
            if context.pointer >= len(context.storage):
                context.storage.append(0)
        elif isinstance(node, PrintCellNode):
            print(chr(context.storage[context.pointer]), end='')
        elif isinstance(node, LoopNode):
            while context.storage[context.pointer] != 0:
                evaluate(node.nodes, context)


def main():
    while True:
        text = input('bf : ')
        tokens = make_tokens(text)
        parser = Parser(tokens)
        nodes = parser.parse()
        evaluate(nodes)
        print()


if __name__ == '__main__':
    main()
