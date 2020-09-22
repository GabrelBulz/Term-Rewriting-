import tree 

class LpoHelper:
    def __init__(self, variables, constants, function_arity, precedence_order):
        self.variables = variables
        self.constants = constants
        self.function_arity = function_arity 
        self.precedence_order = precedence_order

    def ordering(self, left_exp, right_exp):
        if(self.check_rules(left_exp, right_exp)):
            return True
        return None 

    def check_rules(self, left_exp, right_exp):
        print('Left exp: ' + str(left_exp))
        print('Right exp: ' + str(right_exp))

        left_tree = tree.Tree(left_exp, self.variables, self.constants, self.function_arity)
        right_tree = tree.Tree(right_exp, self.variables, self.constants, self.function_arity)


        if(left_tree.get_root() == None or right_tree.get_root() == None):
            print('Invalid trees')
            return None

        #lpo1 
        if(left_tree.get_root().get_node_type() != 'VARIABLE' and right_tree.get_root().get_node_type() == 'VARIABLE'):
            print('Lpo 1 holds for ' + left_exp + " and " + right_exp)
            if(right_tree.get_root().print_expression() in left_tree.get_root().print_expression()):
                return True
            return None 
        elif(left_tree.get_root().get_node_type() != 'VARIABLE' and right_tree.get_root().get_node_type() != 'VARIABLE'):
            #lpo 2
            print("Try Lpo 2")

            if(self.is_greater(left_tree.get_root().content, right_tree.get_root().content) and self.lpo2B(left_tree, right_tree)):
                print("Lpo2B holds")
                return True
            elif(self.is_equal(left_tree.get_root().content, right_tree.get_root().content) and self.lpo2C(left_tree, right_tree)):
                print("Lpo2C holds")
                return True
            elif(self.lpo2A(left_tree, right_tree)):
                #LPO2a, last because pre-existent conditions are not as restrictive as for LPO2b and LPO2c
                print("Lpo2A holds")
                return True
        return False

    def lpo2A(self, left_tree, right_tree):
        print("apply Lpo2A on " + left_tree.get_root().print_expression() \
            + " and " + right_tree.get_root().print_expression())

        # check if there is an i for i in size(s) , where s_i >= t
        for i in range(left_tree.get_root().get_nr_of_children()):
            if(left_tree.get_root().get_children_list()[i].print_expression() == right_tree.get_root().print_expression()):
                 return True 

            if(self.check_rules(left_tree.get_root().print_expression(), right_tree.get_root().print_expression())):
                return True 

        return False

    def lpo2B(self, left_tree, right_tree):
        print("apply Lpo2B on " + left_tree.get_root().print_expression() \
            + " and " + right_tree.get_root().print_expression())

        # check if t> s_j for all j in size of t
        for j in range(right_tree.get_root().get_nr_of_children()):
            if(not self.check_rules(left_tree.get_root().print_expression(), right_tree.get_root().get_children_list()[j].print_expression())):
                return False

        return True 

    def lpo2C(self, left_tree, right_tree):
        print("apply Lpo2C on " + left_tree.get_root().print_expression() \
            + " and " + right_tree.get_root().print_expression())

        # step 1 recursively
        # t > s_j for all  j in size of t
        for j in range(right_tree.get_root().get_nr_of_children()):
            if(not(self.check_rules(left_tree.get_root().print_expression(), right_tree.get_root().get_children_list()[j].print_expression()))):
                return False 

        # step 2 for each value of i all values before i have to be eqaul, else if 1 would be higher than it would fail

        # step 3
        for i in range(left_tree.get_root().get_nr_of_children()):
            if(self.check_rules(left_tree.get_root().get_children_list()[i].print_expression(),\
                right_tree.get_root().get_children_list()[i].print_expression())):

                # if this is true all positions before the i which are true must be =
                for k in range(j):
                    if(left_tree.get_root().get_children_list()[k].print_expression() == right_tree.get_root().get_children_list()[k].print_expression()):
                        return False 

                return True 

        return False 


    def is_greater(self, left, right):
        if(self.precedence_order[left.strip()] > self.precedence_order[right.strip()]):
            return True
        return False 

    def is_equal(self, left, right):
        if(self.precedence_order[left.strip()] == self.precedence_order[right.strip()]):
            return True
        return False 