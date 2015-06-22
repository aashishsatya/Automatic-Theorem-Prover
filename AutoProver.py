# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 23:04:42 2015

@author: aashishsatya
"""

from Parser import *

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
            
    def tell(clause):
        if is_definite_clause(clause):
            if clauses.op in self.clauses:
                self.clauses[clause.op].append(clause)
            else:
                # no such key as clause.op
                # so make one
                self.clauses[clause.op] = [clause]
        else:
            print 'Clause not definite, ignored:', clause
            
    def ask(self, query):
        pass
    
    def fetch_rules_for_goal(self):
        return self.clauses

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
        
    
def fol_bc_ask(kb, query):
    """
    A function that uses backward chaining to find whether query is entailed by
    the knowledge base kb.
    Straight from Fig. in AIMA, 3rd edition.
    """
    pass

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
    elif is_variable(x):
        return unify_vars(x, y, subst)
    elif is_variable(y):
        return unify_vars(y, x, subst)
    elif isinstance(x, Clause) and isinstance(y, Clause):
        return unify(x.args, y.args, unify(x.op, y.op, subst))
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        return unify(x[1:], y[1:], unify(x[0], y[0], subst))
    else:
        return None

def unify_vars(var, x, subst):
    
    """
    Helper function that supports the above unify function. Only gets called
    when unify is dealing with variables.
    """
    
    if var in subst.keys():
        return unify(subst[var], x, subst)
    # occur check is eliminated
    subst_copy = subst.copy()
    subst_copy[var] = x
    return subst_copy

#______________________________________________________________________________

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
st1 = parse('Knows(John, x)')
st2 = parse('Knows(y, Mother(y))')  # TODO: Nesting does not work!!
st1_cl = convert_to_clause(st1)
st2_cl = convert_to_clause(st2)
ans = unify(st1_cl, st2_cl, {})
if ans is not None:
    ans_keys = ans.keys()
    for key in ans_keys:
        print key, ': ', ans[key]
else:
    print ans   # None