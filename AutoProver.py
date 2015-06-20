# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 23:04:42 2015

@author: aashishsatya
"""

from Parser import *

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
        return item
        
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
        # get the next clause and simply not it
        not_posn = item.index('~')
        not_clause = Clause('~', [item[not_posn + 1:]])
        return not_clause
    elif isinstance(item, str):
        return Clause(item)
    if len(item) == 1:
        # for statements such as ['P']
        return Clause(item[0])
    # for statements such as ['Loves',['Aashish', 'Chocolate']]
    simple_clause = Clause(item[0], item[1:][0]) # [0] because [1:] produces a [[list]]
    return simple_clause        
    
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

print 'Enter statements in first-order logic one by one:'
print 'Enter STOP when done.'

# the knowledge base that stores all the statements
kb = KnowledgeBase()

statement = raw_input()
while statement != 'STOP':    
    # parse the statement    
    parsed_stmnt = parse(statement)
    print parsed_stmnt

    clause = convert_to_clause(parsed_stmnt)   
    
    # add to knowledge base
    
    statement = raw_input()