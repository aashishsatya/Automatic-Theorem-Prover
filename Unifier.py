
"""
Python script that implements the unification algorithm.

@author: Aashish Satyajith.
"""

from KBUtil import *

#______________________________________________________________________________

def is_variable(item):
    
    """
    Checks if the item is a variable.
    """
    
    # an item is a variable if it is of type Clause, its operator is a string
    # and starts with a small case letter, and has no args
    
    return isinstance(item, Clause) and item.op.islower() and item.args == []

#______________________________________________________________________________

def unify(x, y, subst = {}):
    
    """
    The function that tries to unify two statements x and y. If such a unification
    exists then the function returns the substitutions that make the unification
    successful.
    x and y can be clauses, lists (because we pass the arguments of a clause
    to the function, or strings (we pass the operators too)
    subst[x] (if x is in subst) stores the clause after 
    """
    
    # AIMA 3rd edition Fig. 9.1, Pg. 328
    
    if subst is None:
        # failure is denoted by None (default is {})
        return None
    elif x == y:
        # happens if both x and y are operators like '&'
        # or same-name variables (we're trying to return the most general unifier)
        return subst
    # the following two cases are the only cases that can cause a binding
    elif is_variable(x):
        return unify_vars(x, y, subst)
    elif is_variable(y):
        return unify_vars(y, x, subst)
    elif isinstance(x, Clause) and isinstance(y, Clause):
        # if we're to merge two clauses we need to ensure that the operands are the same
        # if they are then unify their arguments
        return unify(x.args, y.args, unify(x.op, y.op, subst))
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        # this is the case when we're unifying the arguments of a clause
        # see preceding line
        return unify(x[1:], y[1:], unify(x[0], y[0], subst))
    else:
        # does not match any case, so no substitution
        return None

#______________________________________________________________________________

def unify_vars(var, x, subst):
    
    """
    Helper function that supports the above unify function. Only gets called
    when unify is dealing with variables.
    """
    
    if var in subst:
        # if binding is already in the dict simply return it
        return unify(subst[var], x, subst)
    # occur check is eliminated
    subst_copy = subst.copy()
    subst_copy[var] = x
    return subst_copy
