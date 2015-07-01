# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 23:04:42 2015

@author: aashishsatya
"""

from Parser import *

OPERATORS = ['&', '|', '~', '==>']
# this is to store parents of clauses
parent_clauses = {}

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
        return fol_bc_ask(self, query)
        
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
        predicate = self.retrieve_predicate(goal)
        if predicate in self.clauses:
            return self.clauses[predicate]
        else:
            return []
    
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
            return retrieve_predicate(goal.args[0])

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
        
    def __str__(self):
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

def is_variable(item):
    
    """
    Checks if item is a variable.
    """
    
    # an item is a variable if it is of type Clause, its operator is a string
    # and starts with a small case letter, and has no args
    
    return isinstance(item, Clause) and item.op.islower() and item.args == []

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
        possible_subst = unify(x.args, y.args, unify(x.op, y.op, subst))
#        if possible_subst is not None:
            # means one was the parent of the other
            # the way fol_bc_ask works is with x as rhs and y as goal
            # hence y is the parent
#            parent_clauses[y] = x
        return possible_subst
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        # this is the case when we're unifying the arguments of a clause
        # see preceding line
        return unify(x[1:], y[1:], unify(x[0], y[0], subst))
    else:
        # does not match any case, so no substitution
        return None

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
    # so now x is a parent of var
    # TODO: inefficient because it stores a lot of bindings that are not used?
#    parent_dict[var] = x
    return subst_copy

#______________________________________________________________________________

VARIABLE_COUNTER = 0

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
        else:
            # clause is a simple clause of kind 'Has(X, Y)'
            # so we need to prove just this i.e. there IS no second clause to prove
            # hence make the second clause [] so it is picked up by fol_bc_and
            first_arg = goals
            second_arg = []
        for theta1 in fol_bc_or(kb, substitute(theta, first_arg), theta):
            # the first argument goes to fol_bc_or because only ONE of the literals
            # in that clause need be proved (and hence the clause becomes true)
            for theta2 in fol_bc_and(kb, second_arg, theta1):
                yield theta2

def convert_to_implication(clause):
    
    """
    Converts clause to a form lhs => rhs for further processing by fol_bc_or.
    """
    
    if clause.op == '==>':
        # the idea is that in lhs => rhs, lhs must be returned as a conjunction of literals.
        # only then can fol_bc_and get each of those conjuncts to prove
        # for this we simply break the nesting of the lhs (this should work, right?)
        return break_nesting(clause.args[0]), clause.args[1]
    else:
        return [], clause

def fol_bc_or(kb, goal, theta):
    
    """
    Helper functions that support fol_bc_ask as in AIMA
    """
    
    possible_rules = kb.fetch_rules_for_goal(goal)
    for rule in possible_rules:
        stdized_rule = standardize_vbls(rule)
        lhs, rhs = convert_to_implication(stdized_rule)
        # lhs goes to fol_bc_AND because ALL clauses in the lhs needs to be proved
#        if lhs != []:
#            print 'from', stdized_rule, 'adding'
#            print 'parent_clauses[', rhs, '] =', lhs, '...'
#            parent_clauses[rhs] = lhs
        rhs_unify_try = unify(rhs, goal, theta)
        if rhs_unify_try is not None:
            # some successful unification was obtained
            # so the rule is the parent of the current goal            
            if lhs != []:
                # checking for and declaring parent for '&'
                if lhs.op == '&':
#                    print 'GOAL IS AND'
                    parent_clauses[lhs] = (lhs.args, 'Rule of conjunction')
                parent_clauses[goal] = ([stdized_rule], 'Modus Ponens')
                parent_clauses[stdized_rule] = ([lhs], 'Rule of universal instantiation')
        for theta1 in fol_bc_and(kb, lhs, rhs_unify_try):
            yield theta1
    
def fol_bc_ask(kb, query):
    """
    A function that uses backward chaining to find whether query is entailed by
    the knowledge base kb.
    Straight from Fig. in AIMA, 3rd edition.
    """
    # simple one-liner.
    return fol_bc_or(kb, query, {})

#______________________________________________________________________________

def is_predicate(clause):
        
        """
        Finds if the clause is a predicate or not
        """
        
        return clause.op not in OPERATORS and clause.op[0].isupper() 
        
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

def complete_substitute(theta, clause):
    # TODO: make this efficient!!
    for i in range(0, len(theta.keys())):
        clause = substitute(theta, clause)
    return clause

def print_parent(theta, clause):
    """
    Prints the parents of the clause one by one
    """
    
    if clause not in parent_clauses:
        # last statement, must have already been given in kb
        print 'We know', complete_substitute(theta, clause), '(given)'
#        print 'We know', clause, '(given)'
        return
    parents, rule_used = parent_clauses[clause]
    for parent in parents:
        if parent in parent_clauses:
            print_parent(theta, parent)
    #        if all(vbl in find_variables(query) for vbl in find_variables(clause)):
    #        print 'From', complete_substitute(theta, parent_clauses[clause]), 'we get', complete_substitute(theta, clause)
        else:
            print_parent(theta, substitute(theta, parent))
    print 'which leads to', complete_substitute(theta, clause), '(' + rule_used + ')'
#    print 'From', parent_clauses[clause], 'we get', clause
        

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
#    # convert the statement to clause
#    clause = convert_to_clause(parsed_stmnt)   
#    # add to knowledge base
#    kb.tell(clause)    
#    statement = raw_input()
#    
## input query
#query_input = raw_input('Enter your query: ')
#assert query_input != ''
#query = convert_to_clause(parse(query_input))

# if you just want to see the theorem prover in action
# comment out the code above, uncomment the following code and run

# thanks Mr. Norvig for this

crime_kb = KnowledgeBase(
  map(convert_to_clause, map(parse,
    ['(American(x) & Weapon(y) & Sells(x, y, z) & Hostile(z)) ==> Criminal(x)',
     'Owns(Nono, M1)',
     'Missile(M1)',
     '(Missile(x) & Owns(Nono, x)) ==> Sells(West, x, Nono)',
     'Missile(x) ==> Weapon(x)',
     'Enemy(x, America) ==> Hostile(x)',
     'American(West)',
     'Enemy(Nono, America)'
     ])))

test_kb = KnowledgeBase(
    map(convert_to_clause, map(parse, ['Farmer(Mac)',
               'Rabbit(Pete)',
               'Mother(MrsMac, Mac)',
               'Mother(MrsRabbit, Pete)',
               '(Rabbit(r) & Farmer(f)) ==> Hates(f, r)',
               '(Mother(m, c)) ==> Loves(m, c)',
               '(Mother(m, r) & Rabbit(r)) ==> Rabbit(m)',
               '(Farmer(f)) ==> Human(f)',
               '(Mother(m, h) & Human(h)) ==> Human(m)'
               ])))

simpler_kb = KnowledgeBase(
    map(convert_to_clause, map(parse, ['Malayali(Aashish)',
    'Malayali(y) & Loves(India, y) ==> Indian(y)',
    'Loves(India, Aashish)'
    ])))

simplest_kb = KnowledgeBase(
    map(convert_to_clause, map(parse, ['Malayali(Aashish)',
    'Malayali(x) ==> Indian(x)',
    ])))
    
kb = test_kb
query = convert_to_clause(parse('Hates(x, y)'))

#kb = test_kb
#query = convert_to_clause(parse('Hates(x,y)'))

vbls_in_query = find_variables(query)
for answer in kb.ask(query):
#    print '\nbindings:\n'
##    for variable in vbls_in_query:
##        if variable in answer:
##            print str(variable) + ':', answer[variable]
#    for key in answer.keys():
#        print str(key) + ':', answer[key]
#    print '\nparents:\n'
#    for key in parent_clauses.keys():
#        parents, rule_used = parent_clauses[key]
#        print str(key) + ': [',
#        print parents[0],
#        for parent in parents[1:]:
#            print ',',
#            print parent,
#        print '],', rule_used
    print '\nlogical process:\n'
    print_parent(answer, query)
    print ''
#    break