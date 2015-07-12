
"""
The script that implements the actual algorithm for backward chaining along
with several other utilities.

@author: Aashish Satyajith.

"""

from Unifier import *

VARIABLE_COUNTER = 0

# this is to store parents of clauses
parent_clauses = {}

#______________________________________________________________________________

def standardize_vbls(clause, already_stdized = None):
    
    """
    Returns the given clause after standardizing the given variables.
    'clause' is an object of type Clause
    'already_stdized' stands for already standardized variables. It is this dict
    that the program will check first to ensure that a (new) binding has already been
    given to the variable. This is needed for statements such as 'F(x) & G(x)' --
    we need them to be standardized as 'F(v_0) & G(v_0)' and not as 'F(v_0) & G(v_1)'
    """
    
    global VARIABLE_COUNTER
    
    if already_stdized is None:
        already_stdized = {}
        
    if not isinstance(clause, Clause):
        return clause
    
    if is_variable(clause):
        # check if variable has already been standardized
        if clause in already_stdized:
            return already_stdized[clause]
        else:
            new_vbl = Clause('v_' + str(VARIABLE_COUNTER))
            VARIABLE_COUNTER += 1
            # add new binding to the dict
            already_stdized[clause] = new_vbl
            return new_vbl
    else:
        # simply create a new clause mapping the same function to all the args
        return Clause(clause.op, (standardize_vbls(arg, already_stdized) for arg in clause.args))    
    
#______________________________________________________________________________

def substitute(theta, clause):
    
    """
    Substitutes variables in clause with their (new) bindings in theta.
    theta is a dict while clause is as usual an object of type Clause.
    """
    
    assert isinstance(clause, Clause)
    
    if is_variable(clause):
        # check if the variable already has a binding
        if clause in theta:
            return theta[clause]
        else:
            return clause
    else:
        # compound clause with operators such as '&'
        # check if any of the arguments are bound, and substitute
        return Clause(clause.op, (substitute(theta, arg) for arg in clause.args))

#______________________________________________________________________________

def convert_to_implication(clause):
    
    """
    Converts clause to a form lhs => rhs for further processing by fol_bc_or.
    """
    
    if clause.op == '==>':
        # the idea is that in lhs => rhs, lhs must be returned as a conjunction of literals.
        # only then can fol_bc_and get each of those conjuncts to prove
        # for this we simply break the nesting of the lhs
        return break_nesting(clause.args[0]), clause.args[1]
    else:
        return [], clause

#______________________________________________________________________________

def fol_bc_and(kb, goals, theta):
    
    """
    Helper functions that support fol_bc_ask as in AIMA
    goals is a clause that will be a conjunction of all literals to prove.
    """

    if theta is None:
        pass
    elif isinstance(goals, list) and len(goals) == 0:
        # this happens when lhs ==> rhs is [] ==> rhs
        yield theta
    else:
        if goals.op == '&':
            # operator can only be '&' because the clause is definite (we've broken the nesting)
            first_arg = goals.args[0]
            second_arg = goals.args[1]
            if first_arg.op == '&':
                # il problemo!
                # fol_bc_or can only prove definite clauses, a conjunction of two literals alone is not one
                # so we strip each second conjunct off, club it with the second arg until the first_arg is a literal
                while not is_predicate(first_arg):
                    second_arg = Clause('&', [first_arg.args[1], second_arg])
                    first_arg = first_arg.args[0]
        else:
            # clause is a simple clause of kind 'Has(X, Y)'
            # so we need to prove just this i.e. there IS no second clause to prove
            # hence make the second clause [] so it is picked up by fol_bc_and
            first_arg = goals
            second_arg = []
        for theta1 in fol_bc_or(kb, substitute(theta, first_arg), theta):
            # notice that it is substitute(theta, first_arg) that will get a parent and not first_arg
            # second_arg will also get substituted by the theta (i.e. theta1) obtained on running fol_bc_or on the first arg
            # hence it is substitute(thetaONE, second_arg) that will get a parent, not substitute(theta, second_arg) or
            # just second arg
            if isinstance(second_arg, Clause):
                parent_clauses[substitute(theta, goals)] = ([substitute(theta, first_arg), substitute(theta1, second_arg)], 'Rule of conjunction', None)
            # the first argument goes to fol_bc_or because only ONE of the literals
            # in that clause need be proved (and hence the clause becomes true)
            for theta2 in fol_bc_and(kb, second_arg, theta1):
                yield theta2

#______________________________________________________________________________

def fol_bc_or(kb, goal, theta):
    
    """
    Helper functions that support fol_bc_ask as in AIMA
    """

    possible_rules = kb.fetch_rules_for_goal(goal)
    for rule in possible_rules:
        stdized_rule = standardize_vbls(rule)
        lhs, rhs = convert_to_implication(stdized_rule)
        rhs_unify_try = unify(rhs, goal, theta)
        if rhs_unify_try is not None:
            # some successful unification was obtained
            if lhs != []:
                # checking for and declaring parent for '&'
                if lhs.op == '&':
                    substituted_lhs_args = [substitute(rhs_unify_try, arg) for arg in lhs.args]
                    parent_clauses[substitute(rhs_unify_try, lhs)] = (substituted_lhs_args, 'Rule of conjunction', None)
                # actually we're supposed to substitute for the rhs
                # but this will anyway be the goal, so we can go with goal as the child
                # instead of substitute(rhs, rhs_unify_try)
                parent_clauses[goal] = ([substitute(rhs_unify_try, stdized_rule)], 'Modus Ponens', None)
                parent_clauses[substitute(rhs_unify_try, stdized_rule)] = ([substitute(rhs_unify_try, lhs)], 'Rule of universal instantiation', rule)
        # lhs goes to fol_bc_AND because ALL clauses in the lhs needs to be proved
        for theta1 in fol_bc_and(kb, lhs, rhs_unify_try):
            yield theta1

#______________________________________________________________________________
    
def fol_bc_ask(kb, query):
    """
    A function that uses backward chaining to find whether query is entailed by
    the knowledge base kb.
    Straight from Fig. in AIMA, 3rd edition.
    """
    # simple one-liner.
    return fol_bc_or(kb, query, {})
