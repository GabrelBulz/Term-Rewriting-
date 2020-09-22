from tree import Tree 

class UnificationHelper:

    def __init__(self, variables, constants, func_arity):
        self.function_arity = func_arity
        self.variables = variables
        self.constants = constants

    def unify(self, left_lst_exp, right_lst_exp, s):
        if(len(left_lst_exp) == 1 and len(right_lst_exp) == 1):
            left_tree = Tree(left_lst_exp, self.variables, self.constants, self.function_arity)
            right_tree = Tree(right_lst_exp, self.variables, self.constants, self.function_arity)

            root_left = left_tree.get_root()
            root_right = right_tree.get_root()

            if(root_left.print_expression() == root_right.print_expression()):
                return s
            elif(root_left.get_node_type == 'VARIABLE'):
                return self.unifyVar(root_left.print_expression(), root_right.print_expression(), s)
            elif(root_right.get_node_type == 'VARIABLE'):
                return self.unifyVar(root_right.print_expression(), root_left.print_expression(), s)
            elif(root_left.get_node_type != 'VARIABLE' and root_right.get_node_type != 'VARIABLE'):
                if(left_tree.get_root().content == right_tree.get_root().content):
                    left_sub_term_lst = []

                    for child in left_tree.get_root().get_children_list:
                        left_sub_term_lst.append(child)

                    right_sub_term_lst = []

                    for child in right_tree.get_root().get_children_list:
                        right_sub_term_lst.append(child)

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
                rest_right.append(left_lst_exp[i])

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
            tree = Tree(s[i], self.variables, self.constants, self.functions_arity)
            tree.substitution(s)
            s[i] = tree.get_root().print_expression()

        return s 

    def occurCheck(self, var, x, s):
        xTree = tree(x, self.variables, self.constants, self.function_arity)

        if(var == xTree.get_root().print_expression()):
            return True 
        elif(xTree.get_root().print_expression() in s):
            return self.occurCheck(var, s[xTree.get_root().print_expression()], x)
        elif(xTree.get_root().get_node_type == 'FUNCTION'):
            for subTerm in xTree.get_root().get_children_list():
                if(self.occurCheck(var, subTerm.print_expression(), s)):
                    return True

        return False