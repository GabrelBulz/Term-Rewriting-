"Each element will be represented by a node in a tree"

class NodeTerm:
    def __init__(self, content):
        self.content = content 
        self.children = []
        self.parent = None
        self.position = None

    def add_childern_to_list(self, child):
        self.children.append(child)
        child.set_parent(self) 
    
    def get_children_list(self):
        return self.children

    def get_nr_of_children(self):
        return len(self.children)

    def set_parent(self, parent):
        self.parent = parent
    

    def __str__(self, level=0):
        ret = '|'+'------'*level + self.content + self.get_position() +'\n'
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def print_expression(self):
        string = self.content

        if len(self.children) > 0:
            string = string + "("
            delimitator = ""
            for child in self.children:
                string = string + delimitator + \
                    child.print_expression()
                delimitator = ","
            string = string + ")"

        return string

    def get_arity(self):
        return len(self.get_nr_of_children())

    def get_node_type(self):
        """
            If an element has a 0 arity   --> is a variable or a constant
                                arity > 0 --> is a term

            The element also needs to be made out of letters
        """
        if self.content.isalpha():
            if(self.get_nr_of_children() > 0):
                return "term"
            else:
                return "variable"
        else:
            return "not a term, not a variable"

    def get_position(self):
        # calculate the position recursively
        if self.parent:
            parent = self.parent
            parent_position = parent.get_position()
            child_index = parent.get_children_list().index(self) + 1
            self.position = parent_position + str(child_index)
        else:
            self.position = " "

        return self.position
            

