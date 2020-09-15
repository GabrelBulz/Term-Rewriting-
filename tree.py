from nodeTerm import NodeTerm

class Tree:

    def __init__(self, expression):
        self.expression = expression 
        self.root = None 
        # functions to be called if we encounter one of the symbols
        self.symbols = {'(' : self.open_br,
                        ')' : self.close_br,
                        ',' : self.split}
        
        self.parse()

    def get_root(self):
        return self.root 

    def set_root(self, node):
        self.root = node 

    """
        return a new node containing the specified content
        set parent as an option
    """
    def create_new_node(self, content, parent=None):
        if(len(content) > 0):
            new_node = NodeTerm(content)

            if(parent):
                new_node.set_parent(parent)

            return new_node 
        return None

    """
        curr node will always point to the current
        node in the tree ... other children will be link
        to this one
    """
    def parse(self):
        curr_val = ''
        curr_node = None

        for position, char in enumerate(self.expression):
            if(char in self.symbols):
                try:
                    result = self.symbols[char](position, curr_val, curr_node)
                    if(result):
                        curr_node = result
                        if(not self.get_root()):
                            self.set_root(curr_node)
                except :
                    print("Error at position "+ str(position))
                    self.root = None
                    return
                curr_val = ''
            else:
                curr_val += char 

        if(self.root is None and len(curr_val) > 0):
            new_node = self.create_new_node(curr_val)
            if new_node:
                self.set_root(new_node)
                return
            else:
                print("empty item")
        
        if(len(curr_val) > 0):
            print("Invalid expression, not enought close parantheses")
            self.set_root(None)

    def open_br(self, possition, curr_val, curr_node):
        new_node = self.create_new_node(curr_val, curr_node)
        if new_node:
            # curr_node.add_childern_to_list(new_node)
            return new_node
        else:
            raise Exception()

    def split(self, possition, curr_val, curr_node):
        new_node = self.create_new_node(curr_val, curr_node)
        if new_node:
            curr_node.add_childern_to_list(new_node)
            return curr_node
        if curr_node:
            curr_node.parent.add_childern_to_list(curr_node)
            return curr_node.parent
        else:
            raise Exception()

    def close_br(self, possition, curr_val, curr_node):
        new_node = self.create_new_node(curr_val, curr_node)
        if new_node:
            curr_node.add_childern_to_list(new_node)
            return curr_node
        if curr_node:
            curr_node.parent.add_childern_to_list(curr_node)
            return curr_node.parent
        else:
            raise Exception()

    def substitution(self, substitution_map):
        if(substitution_map != {}):
            self.substitute_in_tree(substitution_map, self.get_root())

    """
        Create a new subtree from the substitution map
        and replace a certain node with that tree

        We have to check if the node we want to replace is a 
        varible or a term
    """
    def substitute_in_tree(self, substitution_map, node):

        if node.content in substitution_map:
            if node.get_node_type() == 'variable':
                replacement = substitution_map[node.content]
                sub_tree = Tree(replacement)

                print("Replace " + node.content + " with \n" + str(sub_tree.get_root()))

                parent = node.parent
                sub_tree.get_root().set_parent(parent)
                index_child = parent.get_children_list().index(node)
                parent.get_children_list()[index_child] = sub_tree.get_root()
            else:
                print('could not replace ' + node.content + 'because it is not a variable')
        else:
            for i in node.get_children_list():
                self.substitute_in_tree(substitution_map, i)
        
def main():
    x = Tree('t(x,Y,g(f(h,x)))')
    print('Tree 1')
    print('Exrpession: ' + x.get_root().print_expression())
    print('Tree:')
    print(x.get_root())

    substitution = {'Y' : 'z',
                    'x' : 'u(q)'}
    x.substitution(substitution)

    print('Tree 1 after substitution:')
    print(x.get_root())




    print('Tree 2')
    x = Tree('f(g(x,y),z)')
    print('Exrpession: ' + x.get_root().print_expression())
    print('Tree:')
    print(x.get_root())



if __name__ == "__main__":
    main()