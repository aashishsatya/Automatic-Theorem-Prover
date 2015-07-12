
"""
Python script that implements the data structure for knowledge base
and clauses.
Defines several other utilities for manipulating classes as well.

Created on Wed Jun 17 23:04:42 2015

@author: Aashish Satyajith.
"""

import FolBC

OPERATORS = ['&', '|', '~', '==>']

#______________________________________________________________________________

class KnowledgeBase:
    
    """
    Implements the knowledge base for the program.
    """
    
    def __init__(self, initial_clauses = []):
        # we will use the operator of the clauses for indexing
        self.clauses = {}
        for clause in initial_clauses:
            self.tell(clause)
            
    def tell(self, clause):
        if is_definite_clause(clause):
            self.predicate_index(clause, clause)
        else:
            print 'Clause not definite, ignored:', clause
            
    def ask(self, query):
        return FolBC.fol_bc_ask(self, query)
        
    def predicate_index(self, main_clause, inside_clause):
        
        """
        Indexes the clause by each predicate for efficient unification.
        main_clause will be the clause that we're asked to add to the knowledge base.
        inside_clause will be the clause that exists inside the main_clause
        """
        
        if is_predicate(inside_clause):
            # simply add the main clause to the kb giving the name of the 
            # predicate as the key
            if inside_clause.op in self.clauses:
                # check if the clause already exists
                if main_clause not in self.clauses[inside_clause.op]:
                    self.clauses[inside_clause.op].append(main_clause)
            else:
                # create a new entry
                self.clauses[inside_clause.op] = [main_clause]
        elif inside_clause.op == '~':
            self.predicate_index(main_clause, inside_clause.args[0])
        else:
            # one of the other operators
            # add both its arguments to the dictionary
            self.predicate_index(main_clause, inside_clause.args[0])
            self.predicate_index(main_clause, inside_clause.args[1])
            
    
    def fetch_rules_for_goal(self, goal):
        try:
            predicate = self.retrieve_predicate(goal)
            if predicate in self.clauses:
                return self.clauses[predicate]
        except IndexError:
            # we've received a simple letter goal, say 'x'
            # no option other than to send all the clauses
            all_clauses = []
            for key in self.clauses.keys():
                all_clauses += self.clauses[key]
            # simply returning all_clauses might result in a lot of duplicates
            # for e.g. P ==> Q is stored both under keys P and Q
            # set() removes all duplicates, list() converts them back into a list
            return list(set(all_clauses))
    
    def retrieve_predicate(self, goal):
        
        """
        Retrieve atleast one predicate that is in the goal so that it can be
        looked up in the self.clauses dict
        """
        
        if is_predicate(goal):
            return goal.op
        else:
            # works if op is '~' or any other symbol
            # because there is always one argument if the symbol is a logical symbol
            return self.retrieve_predicate(goal.args[0])

#______________________________________________________________________________

class Clause:
    
    """
    A class that holds each clause.
    A clause may be
        - an atomic term, such as Likes(Aashish, Chocolate)
        - [~]clause (and / or) [~]clause where [~] denotes an optional negation sign
    A clause such as Likes(Aashish, Chocolate) will be stored as:
    Op will be 'Likes'
    Args will be ['Aashish', 'Chocolate']
    Parents will be None
    """
    
    def __init__(self, op, args = [], parents = None):
        
        """
        Op (operator) is a logical operator such as '&', '|' etc, or string, such
        as 'P' or 'Likes' (the proposition) stored as a string.
        Args are the arguments in the clause, for e.g. in Likes(X, Y) X and Y are
        the arguments.
        Parents are the clauses from which the current clause has been derived.
        This is helpful for showing the proof process. It defaults to None.
        """
        
        self.op = op
        self.parents = parents
        self.args = map(convert_to_clause, args)
        
    def __hash__(self):
        return hash(self.op) ^ hash(tuple(self.args))
        
    def __repr__(self):
        if len(self.args) == 0:
            # simple proposition, just print it out
            return self.op
        elif self.op not in OPERATORS:
            # again simple clause but with arguments like Strong(Superman)
            # again print it out as it is
            args = str(self.args[0])
            for arg in self.args[1:]:
                args = args + ', ' + str(arg)
            return self.op + '(' + args + ')'
        elif self.op == '~':
            if self.args[0].op not in OPERATORS:
                # statement like ~Loves(Batman, Joker)
                # so no need for parens after '~'
                return '~' + str(self.args[0])
            else:
                return '~' + '(' + str(self.args[0]) + ')'
        else:
            # binary operator like '&', '|' or '==>'
            # check if argument clauses have logical operators
            str_repn = ''
            if self.args[0].op in OPERATORS:
                str_repn = '(' + str(self.args[0]) + ')'
            else:
                str_repn = str(self.args[0])
            str_repn += ' ' + self.op + ' '
            if self.args[1].op in OPERATORS:
                str_repn += '(' + str(self.args[1]) + ')'
            else:
                str_repn += str(self.args[1])
            return str_repn
            
    def __eq__(self, other):
        
        return isinstance(other, Clause) and self.op == other.op and \
        self.args == other.args        

#______________________________________________________________________________              
        
def convert_to_clause(item):
    
    """
    Converts item to the type clause.
    Item may already have been a clause, or might be a string or a symbol.
    """
    
    if isinstance(item, Clause):
        # already a clause
        # happens with cases like negate
        return item
        
    # something like the precedence of operators is implicit in the order we process the symbols
    # I say 'something like' because implication is checked for first
    # This is because people tend to say P & Q ==> R by which they mean
    # (P & Q) ==> R rather than P & (Q ==> R)
    # For this to work implication has to be checked for first
    
    # the check for the symbol with the highest precedence comes at the end
    # only then will the nesting take place properly
    # take a moment to wrap your head around this
        
    # check for implication
    if '==>' in item:
        implication_posn = item.index('==>')
        lhs = item[:implication_posn]
        rhs = item[implication_posn + 1:]
        impl_clause = Clause('==>', [lhs, rhs])
        return impl_clause
    # check for or
    elif '|' in item:
        or_posn = item.index('|')
        first_disjunct = item[:or_posn]
        second_disjunct = item[or_posn + 1:]
        or_clause = Clause('|', [first_disjunct, second_disjunct])
        return or_clause
    # check for and
    elif '&' in item:
        and_posn = item.index('&')
        first_conjunct = item[:and_posn]
        second_conjunct = item[and_posn + 1:]
        and_clause = Clause('&', [first_conjunct, second_conjunct])
        return and_clause
    # check for not
    elif '~' in item:
        # get the remaining clause and simply not it
        not_posn = item.index('~')
        not_clause = Clause('~', [item[not_posn + 1:]])
        return not_clause
    elif isinstance(item, str):
        return Clause(item)
    if len(item) == 1:
        # for statements such as ['P']
        # this also helps get rid of unnecessary parens in statements such as
        # ((P & Q))
        return convert_to_clause(item[0])
    # for statements such as ['Loves',['Aashish', 'Chocolate']]
    simple_clause = Clause(item[0], item[1:][0]) # [0] because [1:] produces a [[list]]
    return simple_clause 

#______________________________________________________________________________       

def negate(clause):
    """
    A function that negates the given clause. 'clause' is an object of type
    clause
    """
    if clause.op not in OPERATORS:
        # means a clause like 'P' or 'Has'...
        if clause.args == []:
            # simple clause like 'P'
            return Clause('~', [clause.op])
        else:
            # clause like ['Has', ['Aashish', 'Chocolate']]
            # in that case 'Has' will be the op and rest the arguments
            # of the clause in the '~' "level"
            return Clause('~', [Clause(clause.op, clause.args)])
            
    # otherwise we have four kinds of operations to negate - &, |, ~ and ==>
    # and
    if clause.op == '&':
        # ~(P & Q) becomes ~P | ~Q
        return Clause('|', map(negate, clause.args))
    # or
    elif clause.op == '|':
        # ~(P | Q) becomes ~P & ~Q
        return Clause('&', map(negate, clause.args))
    # implies
    elif clause.op == '==>':
        # ~(P ==> Q) becomes P & ~Q
        return Clause('&', [clause.args[0], negate(clause.args[1])])
    # not
    else:
        # this case is very easy
        # we can just return the argument of the not clause, because THAT'S
        # what is being negated!!
        return clause.args[0]   # there will only be one argument
        
#______________________________________________________________________________
        
def break_nesting(clause):
    
    """
    Breaks the nesting of clauses and converts them into their equivalent
    "no-brackets" representation.
    Helper function to enable us to count the number of positive and negative
    disjuncts for helping with is_definite_clause()
    """
    
    # there is nesting to be broken if the symbol is either
    # an implication, or a not and the operator of the argument's not
    # is a logical symbol
    
    if clause.op == '==>':
        # expand P ==> Q as ~P | Q
        negated_precedent = negate(clause.args[0]) # this is ~P
        # break the nesting of ~P
        broken_negated_precedent = break_nesting(negated_precedent)
        return Clause('|', [broken_negated_precedent, clause.args[1]])
    elif clause.op == '~':
        # only continue breaking nesting if the operator of the not clause's
        # argument is a logical operator
        if clause.args[0].op in OPERATORS:
            # expand
            negated_not_clause = negate(clause.args[0])
            broken_negated_not_clause = break_nesting(negated_not_clause)
            return broken_negated_not_clause
        else:
            # just keep the whole thing as it is
            # we want the ~P etc. to stay as they are so we can count
            # the number of negative and positive literals
            return clause
    elif clause.op in ['&', '|']:
        # break the nesting of their arguments and return them as themselves
        broken_first_arg = break_nesting(clause.args[0])
        broken_second_arg = break_nesting(clause.args[1])
        return Clause(clause.op, [broken_first_arg, broken_second_arg])
    else:
        # simple propositions such as 'P' or 'Loves(Aashish, Chocolate)'
        # send back straight away, nothing to do
        return clause
        
#______________________________________________________________________________
                           
def is_definite_clause(clause):

    """
    Checks if the given clause is a definite clause.
    A definite clause is a disjunction of literals such that exactly one term
    is positive (all the other clauses are negated)
    """
    
    # first break the clause up into simple terms
    broken_clause = break_nesting(clause)
    
    # breaking nesting ensures that the only symbols remaining in the clause
    # are '&', '|' or '~'.
    
    def check_definite_and_count(clause):
        
        """
        Counts the number of positive and negated literals and returns them as
        tuples of (positive, negative) counts.
        Returns False if the clause's operator is 'and' or if the number of positive
        literals exceeds one.
        # TODO: Is this bad engineering?
        """
        
        if clause.op not in OPERATORS:
            # simple propositions such as 'P' or 'Has(...)'
            # return one for positive
            return (1, 0)    
        elif clause.op == '~':
            # there will only be one simple argument such as 'P' or 'Has(...)'
            # so we can simply return one for negative
            return (0, 1)
        elif clause.op == '&':
            # we can simply return False because now there is no way that
            # the clause is a definite clause
            return False        
        # and we're at the hardest case
        # operator is '|'
        # count the number of positive and negative literal for each argument
        first_arg_count = check_definite_and_count(clause.args[0])
        second_arg_count = check_definite_and_count(clause.args[1])
        if type(first_arg_count) == bool or type(second_arg_count) == bool:
            # one of them was False (there's no way this function returns True)
            # so send back False
            return False
        # otherwise add the numbers up and continue
        arg_sum = (first_arg_count[0] + second_arg_count[0], 
                   first_arg_count[1] + second_arg_count[1])
        if arg_sum[0] > 1:
            # more than one positive literal
            return False
        return arg_sum
        
    broken_clause_count = check_definite_and_count(broken_clause)
    if broken_clause_count == False:
        return False
    return broken_clause_count[0] == 1

#______________________________________________________________________________

def is_predicate(clause):
        
        """
        Finds if the clause is a predicate or not
        """
        
        return clause.op not in OPERATORS and clause.op[0].isupper() 
