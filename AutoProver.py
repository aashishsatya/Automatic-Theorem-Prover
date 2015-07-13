
"""
The wrapper script that brings it all together, plus some utility functions.

Created on Wed Jun 17 23:04:42 2015

@author: aashishsatya
"""

from Parser import *
from FolBC import *
from PrintProof import *
from HelpMessage import *

#______________________________________________________________________________

def find_variables(clause):
    
    """
    Finds the variables in a clause.
    """
    
    if is_variable(clause):
        return [clause]
    elif is_predicate(clause):
        return clause.args
    elif clause.op == '~':
        return find_variables(clause.args[0])
    else:
        first_arg_vbls = find_variables(clause.args[0])
        second_arg_vbls = find_variables(clause.args[1])
        return first_arg_vbls + second_arg_vbls
        
#______________________________________________________________________________

# x_count will be used to number the variables
# if x_count is 0 then the generated variable will be x_0, if it is 1 then x_1
# and so on (like standardize variables)

x_count = 0

def replace_with_variables(clause, theta = {}):

    """
    Replaces constants in clause with variables and return the substitutions
    that on substitution will yield the statement to prove.
    """

    global x_count

    assert isinstance(clause, Clause)
    if is_predicate(clause):
        # replace arguments of the clause with a variable
        theta_copy = theta.copy()
        new_args = []
        for arg in clause.args:
            if not is_variable(arg):
                new_arg_clause = Clause('x_' + str(x_count))
                theta_copy[new_arg_clause] = arg
                new_args.append(new_arg_clause)
                x_count += 1
        return Clause(clause.op, new_args), theta_copy

#______________________________________________________________________________

print '\nAutomatic Theorem Prover for First Order Logic, implemented by Aashish Satyajith.\n'
print 'Enter HELP for help.\n'
print 'Enter statements in first-order logic one by one:'
print 'Enter STOP when done.\n'

# the knowledge base that stores all the statements
kb = KnowledgeBase()

statement = raw_input()
while statement != 'STOP':
    if statement == 'HELP':
        print_help()
    # parse the statement    
    parsed_stmnt = parse(statement)
    # convert the statement to clause
    clause = convert_to_clause(parsed_stmnt)   
    # add to knowledge base
    kb.tell(clause)    
    statement = raw_input()
    
# input query
query_input = raw_input('\nEnter statement to prove: ')
assert query_input != ''

# replace the constants in the query with variables
query_to_prove = convert_to_clause(parse(query_input))
query, reqd_theta = replace_with_variables(convert_to_clause(parse(query_input)))

# if you just want to see the theorem prover in action,
# comment out the code above, uncomment the following code and run
# NOTE: there's also some formatting to be done towards the end of the script!!

# thanks Mr. Norvig for this

##crime_kb = KnowledgeBase(
##  map(convert_to_clause, map(parse,
##    ['(American(x) & Weapon(y) & Hostile(z) & Sells(x, y, z)) ==> Criminal(x)',
##     'Owns(Nono, M1)',
##     'Missile(M1)',
##     'Missile(x) & Owns(Nono, x) ==> Sells(West, x, Nono)',
##     'Missile(x) ==> Weapon(x)',
##     'Enemy(x, America) ==> Hostile(x)',
##     'American(West)',
##     'Enemy(Nono, America)'
##     ])))
##
##farm_kb = KnowledgeBase(
##    map(convert_to_clause, map(parse, ['Farmer(Mac)',
##               'Rabbit(Pete)',
##               'Mother(MrsMac, Mac)',
##               'Mother(MrsRabbit, Pete)',
##               '(Rabbit(r) & Farmer(f)) ==> Hates(f, r)',
##               '(Mother(m, c)) ==> Loves(m, c)',
##               '(Mother(m, r) & Rabbit(r)) ==> Rabbit(m)',
##               '(Farmer(f)) ==> Human(f)',
##               '(Mother(m, h) & Human(h)) ==> Human(m)'
##               ])))
##
##simpler_kb = KnowledgeBase(
##    map(convert_to_clause, map(parse, ['Malayali(Aashish)',
##    'Malayali(y) & Loves(India, y) ==> Indian(y)',
##    'Loves(India, Aashish)'
##    ])))
##
##simplest_kb = KnowledgeBase(
##    map(convert_to_clause, map(parse, ['Malayali(Aashish)',
##    'Malayali(x) ==> Indian(x)',
##    ])))
##
##simple_kb = KnowledgeBase(
##    map(convert_to_clause, map(parse, ['Malayali(Aashish)',
##    '(Malayali(y) & Loves(India, y)) & Boy(y) ==> Indian(y)',
##    'Loves(India, Aashish)',
##    'Boy(Aashish)'
##    ])))
##
##other_kb = KnowledgeBase(
##    map(convert_to_clause, map(parse, ['P ==> Q',
##    'Q ==> R',
##    'P',
##    ])))
##    
##kb = farm_kb
##query = convert_to_clause(parse('Hates(x, y)'))

# to check if the statement has been proved
proof_flag = False

vbls_in_query = find_variables(query)
for answer in kb.ask(query):
    # comment the below part out if you're using the program as a query-based system    
    if all(reqd_theta[key] == answer[key] for key in reqd_theta.keys()):
        # all keys match        
        print '\nProof:\n'
        print_parent(answer, query)
        proof_flag = True
        break
    # uncomment this and run to see all proofs obtained by the query-based system
##    print '\nProof:\n'
##    print_parent(answer, query)

if not proof_flag:
    print '\nSorry, your statement could not be proved.\n'
else:
    print ''
