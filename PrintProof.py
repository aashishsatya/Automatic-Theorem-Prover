
"""
The script that prints out proof of the queried statement (if one exists).

@author: Aashish Satyajith.

"""

from FolBC import *

#______________________________________________________________________________

def complete_substitute(theta, clause):

    """
    Keeps substituting for variables in clause until there
    are no variables to substitute for or all variables in
    theta have been substituted.
    This is needed for displaying the proof.
    """
    
    for i in range(0, len(theta.keys())):
        clause = substitute(theta, clause)
    return clause

#______________________________________________________________________________

def print_parent(theta, clause):
    
    """
    Prints the parents of the clause one by one
    """
    
    if clause not in parent_clauses:
        # last statement, must have already been given in kb
        print 'We know', complete_substitute(theta, clause), '(given)'
        return
    parents, law_used, clause_used = parent_clauses[clause]
    for parent in parents:
        print_parent(theta, parent)
    print 'which leads to', complete_substitute(theta, clause),
    if clause_used is not None:
        # clause was of the implication form
        print '(' + law_used, 'on', str(clause_used) + ')'
    else:
        print '(' + law_used + ')'
        
