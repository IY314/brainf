from dataclasses import dataclass
import argparse
import subprocess
import os


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
        return self.node()

    def node(self, in_loop=False):
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
                nodes.append(LoopNode(self.node(True)))
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


def compile_bf(nodes, filename, spaces=4, indent_level=1, _c_code=None):
    tab = ' ' * spaces * indent_level
    itab = ' ' * spaces * (indent_level + 1)
    if _c_code is None:
        c_code = '#include <stdio.h>\n'
        c_code += '#include <stdlib.h>\n\n'
        c_code += 'int main() {\n'
        c_code += f'{tab}int *tape = malloc(30000);\n'
        c_code += f'{tab}int ptr = 0;\n\n'
    else:
        c_code = _c_code
    for node in nodes:
        if isinstance(node, IncrementNode):
            c_code += f'{tab}tape[ptr]++;\n'
        elif isinstance(node, DecrementNode):
            c_code += f'{tab}if (tape[ptr] > 0) {{\n'
            c_code += f'{itab}tape[ptr]--;\n'
            c_code += f'{tab}}}\n'
        elif isinstance(node, MoveLeftNode):
            c_code += f'{tab}if (ptr > 0) {{\n'
            c_code += f'{itab}ptr--;\n'
            c_code += f'{tab}}}\n'
        elif isinstance(node, MoveRightNode):
            c_code += f'{tab}if (ptr < 29999) {{\n'
            c_code += f'{itab}ptr++;\n'
            c_code += f'{tab}}}\n'
        elif isinstance(node, PrintCellNode):
            c_code += f'{tab}printf("%c", tape[ptr]);\n'
        elif isinstance(node, GetInputNode):
            c_code += f'{tab}tape[ptr] = (int) getchar();\n'
        elif isinstance(node, LoopNode):
            c_code += f'{tab}while (tape[ptr] != 0) {{\n'
            c_code = compile_bf(
                node.nodes, filename, spaces, indent_level + 1, c_code
            )
            c_code += f'{tab}}}\n'
    
    if _c_code is not None:
        return c_code
    c_code += f'{tab}return 0;\n}}\n'
    with open(f'{filename}.c', 'w+') as f:
        f.write(c_code)
    subprocess.run(['gcc', f'{filename}.c', '-o', f'{filename.rstrip(".bf")}'])
    os.remove(f'{filename}.c')


def evaluate_bf(nodes, context=None):
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
        elif isinstance(node, GetInputNode):
            pass
        elif isinstance(node, LoopNode):
            while context.storage[context.pointer] != 0:
                evaluate_bf(node.nodes, context)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--shell', '-s', action='store_true', help='Activate in shell mode'
    )
    parser.add_argument(
        '--file', '-f', help='the input file'
    )
    args = parser.parse_args()
    if args.shell:
        while True:
            text = input('bf : ')
            tokens = make_tokens(text)
            parser = Parser(tokens)
            nodes = parser.parse()
            evaluate_bf(nodes)
            print()
    elif args.file is not None:
        with open(args.file) as f:
            text = f.read()
            tokens = make_tokens(text)
            parser = Parser(tokens)
            nodes = parser.parse()
            compile_bf(nodes, args.file)
    else:
        print('No input files or shell specified')


if __name__ == '__main__':
    main()
