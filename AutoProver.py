# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 23:04:42 2015

@author: aashishsatya
"""

class KnowledgeBase:
    """
    Implements the knowledge base for the program.
    """
    pass

class Term:
    """
    A class that holds each term.
    A term may be
        - an atomic term, such as Likes(Aashish, Ice Cream)
        - [~]term (and / or) [~]term where [~] denotes an optional negation sign
    """
    
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

statement = raw_input()
kb = KnowledgeBase()

while statement != 'STOP':
    
    # parse the statement
    
    # check for implication
    try:
        antecedent, precedent = statement.split('==>')
    except ValueError:
        # ok, no implication, we just need to split the '&'s and add
        # the statement to the KB   
    # add to knowledge base
    statement = raw_input()