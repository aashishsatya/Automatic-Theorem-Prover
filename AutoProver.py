# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 23:04:42 2015

@author: aashishsatya
"""

from Parser import *

OPERATORS = ['&', '|', '~', '==>']

class KnowledgeBase:
    
    """
    Implements the knowledge base for the program.
    """
    
    def __init__(self, clauses = []):
        self.clauses = clauses

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
        
def convert_to_clause(item):
    
    """
    Converts item to the type clause.
    Item may already have been a clause, or might be a string or a symbol.
    """
    
    if isinstance(item, Clause):
        # already a clause
        # happens with cases like negate
        return item
        
    # something like the precedence of operators is implicit in the order
    # we process the symbols
    # I say 'something like' because implication is checked for first
    # This is because people tend to say P & Q ==> R by which they mean
    # (P & Q) ==> R
    # For this to work implication has to be checked for first
    
    # the check for the symbol with the highest precedence comes at the end
    # only then will the nesting take place properly
    # take a moment to wrap your head around this
        
    # check for implication
    if '==>' in item:
        implication_posn = item.index('==>')
        precedent = item[:implication_posn]
        antecedent = item[implication_posn + 1:]
        impl_clause = Clause('==>', [precedent, antecedent])
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
#        print 'not args =', [item[not_posn + 1:]]
        not_clause = Clause('~', [item[not_posn + 1:]])
        return not_clause
    elif isinstance(item, str):
        return Clause(item)
    if len(item) == 1:
        # for statements such as ['P']
        return convert_to_clause(item[0])
    # for statements such as ['Loves',['Aashish', 'Chocolate']]
    simple_clause = Clause(item[0], item[1:][0]) # [0] because [1:] produces a [[list]]
    return simple_clause        

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
            # one of them was False (there's no way this fn returns True)
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
        
    
def fol_bc_ask(kb, query):
    """
    A function that uses backward chaining to find whether query is entailed by
    the knowledge base kb.
    Straight from Fig. in AIMA, 3rd edition.
    """
    pass

def unify(x, y, subst = {}):
    """
    The function that tries to unify two statements x and y. If the function is
    successful it returns the binding that makes the unification successful
    (stored in subst)
    """
    pass

def unify_vars(x, y, subst):
    """
    Helper function that supports the above unify function
    """
    pass

def fol_bc_and():
    """
    Helper functions that support fol_bc_ask as in AIMA
    """
    pass

def fol_bc_or():
    """
    Helper functions that support fol_bc_ask as in AIMA
    """
    pass

#print 'Enter statements in first-order logic one by one:'
#print 'Enter STOP when done.'
#
## the knowledge base that stores all the statements
#kb = KnowledgeBase()
#
#statement = raw_input()
#while statement != 'STOP':    
#    # parse the statement    
#    parsed_stmnt = parse(statement)
#    print parsed_stmnt
#
#    clause = convert_to_clause(parsed_stmnt)   
#    
#    # add to knowledge base
#    
#    statement = raw_input()

# testing, will be removed later
st = parse('~P|~Q|~S | ~(~P&Q)')
st_cl = convert_to_clause(st)
idc = is_definite_clause
print idc(st_cl)