from nodeTerm import NodeTerm
import order

class Tree:

    def __init__(self, expression, variables, constants, functions_arity):
        self.expression = expression 
        self.root = None 
        self.variables = variables
        self.constants = constants
        self.functions_arity = functions_arity
        # functions to be called if we encounter one of the symbols
        self.symbols = {'(' : self.open_br,
                        ')' : self.close_br,
                        ',' : self.split}
        
        self.parse()
        self.validate_tree()

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
        

    def validate_tree(self):
        if(self.get_root == None):
            print("root is empty")
            return
        else:
            self.check_node_valid(self.get_root())

    def check_node_valid(self, node):
        arity_node = node.get_arity()
        if(arity_node > 0):
            if(node.content in self.functions_arity):
                if(self.functions_arity[node.content] != arity_node):
                    print(self.get_root())
                    print("The expression is not valid because the function at possition " \
                         + str(node.get_position()) + " has arity " + str(arity_node) \
                         + " but it should have arity " + str(self.functions_arity[node.content]))
                    self.set_root(None)
                    return 
                else:
                    node.set_node_type('FUNCTION')
            else:
                print("The expression is not valid because the function at possition " \
                      + str(node.get_position()) + " was not declared as a function symbol")
        else:
            if(node.content in self.variables):
                node.set_node_type('VARIABLE')
            elif(node.content in self.constants):
                node.set_node_type('CONSTANT')
            else:
                print(self.get_root())
                print("The expression is not valid because the term at possition " \
                      + str(node.get_position()) + " was not declared as a variable nor a constant")
                self.set_root(None)
                return 

        if(node != None):
            for child in node.get_children_list():
                self.check_node_valid(child)

    def get_node_at_position(self, position):
        if(self.get_root() == None):
            print('The root is empty return NONE')
            return None
        else:
            return self.find_position(self.get_root(), position)

    def find_position(self, node, position):
        if(node.get_position() == " " + str(position)):
            return node
        else:
            for i in node.get_children_list():
                result = self.find_position(i, position)
                if result != None:
                    return result



class UnificationHelper:

    def __init__(self, variables, constants, func_arity):
        self.function_arity = func_arity
        self.variables = variables
        self.constants = constants

    def unify(self, left_lst_exp, right_lst_exp, s):
        if(len(left_lst_exp) == 1 and len(right_lst_exp) == 1):
            left_tree = Tree(left_lst_exp[0], self.variables, self.constants, self.function_arity)
  
            right_tree = Tree(right_lst_exp[0], self.variables, self.constants, self.function_arity)
            root_left = left_tree.get_root()
            root_right = right_tree.get_root()

            if(root_left.print_expression() == root_right.print_expression()):
                return s
            elif(root_left.get_node_type() == 'VARIABLE'):
                return self.unifyVar(root_left.print_expression(), root_right.print_expression(), s)
            elif(root_right.get_node_type() == 'VARIABLE'):
                return self.unifyVar(root_right.print_expression(), root_left.print_expression(), s)
            elif(root_left.get_node_type() != 'VARIABLE' and root_right.get_node_type() != 'VARIABLE'):
                if(left_tree.get_root().content == right_tree.get_root().content):
                    left_sub_term_lst = []

                    for child in left_tree.get_root().get_children_list():
                        left_sub_term_lst.append(child.print_expression())

                    right_sub_term_lst = []

                    for child in right_tree.get_root().get_children_list():
                        right_sub_term_lst.append(child.print_expression())

                    return self.unify(left_sub_term_lst, right_sub_term_lst, s)
                else:
                    print('Clash Failure')
                    return 
        else:
            first_left = []
            first_left.append(left_lst_exp[0])

            rest_left = []
            for i in range(1,len(left_lst_exp)):
                rest_left.append(left_lst_exp[i])

            first_right = []
            first_right.append(right_lst_exp[0])

            rest_right = []
            for i in range(1,len(right_lst_exp)):
                rest_right.append(right_lst_exp[i])

            return self.unify(rest_left, rest_right, self.unify(first_left, first_right, s))
        return None 

    def unifyVar(self, var, x, s):
        if(var in s):
            left = []
            left.append(s[var])

            right=[]
            right.append(x)

            return self.unify(left, right, s)
        elif(x in s):
            return self.unifyVar(var, s[x] ,s)
        elif(self.occurCheck(var,x,s)):
            print('Failure Occured with: ')
            print(var,x,s)
            return None
        else:
            return self.addSubstitution(var,x, s)

    def addSubstitution(self, var, x, s):
        s[var] = x
        for i in s:
            tree = Tree(s[i], self.variables, self.constants, self.function_arity)
            tree.substitution(s)
            s[i] = tree.get_root().print_expression()
        return s 

    def occurCheck(self, var, x, s):
        xTree = Tree(x, self.variables, self.constants, self.function_arity)

        if(var == xTree.get_root().print_expression()):
            return True 
        elif(xTree.get_root().print_expression() in s):
            return self.occurCheck(var, s[xTree.get_root().print_expression()], x)
        elif(xTree.get_root().get_node_type == 'FUNCTION'):
            for subTerm in xTree.get_root().get_children_list():
                if(self.occurCheck(var, subTerm.print_expression(), s)):
                    return True

        return False


def main():

    VARIABLE = ['x']
    CONSTANTS = ['c']
    FUNCTIONS_ARITY = {'f' : 2}
    x = Tree('f(x,f(x))', VARIABLE, CONSTANTS, FUNCTIONS_ARITY)
    print(x.get_root())
    print(x.get_node_at_position('21'))
    

    VARIABLE = ['w','y','z','x']
    FUNCTIONS_ARITY = {'f':2,
                       'g':1}
    CONSTANTS = []


    left_exp = "f(g(f(y,z)),g(w))"
    left_exp_lst = []
    left_exp_lst.append(left_exp)
    lft= Tree(left_exp, VARIABLE, CONSTANTS, FUNCTIONS_ARITY)

    # tree = Tree(left_exp, VARIABLE, CONSTANTS, FUNCTIONS_ARITY)
    # print(x.get_root())

    right_exp = "f(x,x)"
    right_exp_lst = []
    right_exp_lst.append(right_exp)
    rght = Tree(right_exp, VARIABLE, CONSTANTS, FUNCTIONS_ARITY)

    print("*********************Unification for: ****************************")
    print("LEFT EXPRESSION: " + left_exp)
    print("RIGHT EXPRESSION: " + right_exp)

    unificationhelp = UnificationHelper(VARIABLE, CONSTANTS, FUNCTIONS_ARITY)
    mgu = unificationhelp.unify(left_exp_lst, right_exp_lst,{})

    print('mgu: ' + str(mgu))
    print()




    print("Exercice 4.18 from book")
    VARIABLE = ['y','a','x']
    FUNCTIONS_ARITY = {'f':2,
                       'h':1}
    CONSTANTS = []

    left_exp = "f(x,y)"
    left_exp_lst = []
    left_exp_lst.append(left_exp)

    # tree = Tree(left_exp, VARIABLE, CONSTANTS, FUNCTIONS_ARITY)
    # print(x.get_root())

    right_exp = "f(h(a),x)"
    right_exp_lst = []
    right_exp_lst.append(right_exp)

    unificationhelp = UnificationHelper(VARIABLE, CONSTANTS, FUNCTIONS_ARITY)
    mgu = unificationhelp.unify(left_exp_lst, right_exp_lst,{})

    print("*********************Unification for: ****************************")
    print("LEFT EXPRESSION: " + left_exp)
    print("RIGHT EXPRESSION: " + right_exp)
    print('mgu: ' + str(mgu))
    print()


    print("*********************ORDERING for: ****************************")
    left = "i(f(x,y))"
    right = "f(i(y),i(x))"

    VARIABLE = ['y','x']
    FUNCTIONS_ARITY = {'f':2,
                       'i':1}
    CONSTANTS = []
    precedenceMap ={'f' : 0,
                    'i' : 1}

    lpoHelp = order.LpoHelper(VARIABLE, CONSTANTS, FUNCTIONS_ARITY, precedenceMap)
    result = lpoHelp.ordering(left, right)
    print(result )


    print("*********************ORDERING for: ****************************")
    left = "f(f(x,y),z)"
    right = "f(x,f(y,z))"

    VARIABLE = ['y','x','z']
    FUNCTIONS_ARITY = {'f':2}
    CONSTANTS = []
    precedenceMap ={'f' : 0}

    lpoHelp = order.LpoHelper(VARIABLE, CONSTANTS, FUNCTIONS_ARITY, precedenceMap)
    result = lpoHelp.ordering(left, right)
    print(result )



if __name__ == "__main__":
    main()