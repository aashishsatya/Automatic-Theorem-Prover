"""
Created on Fri Feb 13 12:01:46 2015

@author: aashishsatya

Description: Python script that handles the parsing of Scheme expressions.
Modeled after Peter Norvig's implementation of the same.

"""

# we'll need functions that perform basic housekeeping
# (removing all the parens for processing etc.)

def tokenize(string):
    
    # a token is the smallest individual unit of a program
    
    """
    Converts the input string into a list of tokens.
    """
    
    # a string is generally of the form P ==> Q
    # we need the list as ['P' ==> 'Q'] for which the string should be wrapped
    # in another pair of parens, like (P ==> Q)
    
    string = '(' + string + ')'
    
    # add a space to parens so that they can be split easily
    string = string.replace('(', ' ( ')
    string = string.replace(')', ' ) ')
    # commas are also troublesome
    string = string.replace(',', ' ')
    
    # add a space to logical operatives so that they are also split
    string = string.replace('|', ' | ')
    string = string.replace('&', ' & ')
    string = string.replace('~', ' ~ ')
    string = string.replace('==>', ' ==> ')
    
    
    return string.split()
    
# we will model things exactly as with the scheme implementation
# of the metacircular evaluator
# (define a 10) becomes ['define', 'a', '10']
# To make the concept more clear, think of a list in Scheme as a 
# list in Python!!
# this lets the classifier do its work (see Classifier.py)

# Thanks Peter Norvig for making this part easy

def parse(program):
    
    """
    Calls tokenize and read_from_tokens, cleans up the program for processing 
    as mentioned above.
    """
    
    return read_from_tokens(tokenize(program))
    
def read_from_tokens(token_list):    
    
    """
    Identifies individual expressions from a list of tokens and packages
    them as a list
    """
    
    # this is implemented as a separate function for the recursion to work properly
    
    first_token = token_list.pop(0)
    
    if first_token == '(':
        # new expression in place
        # so initialize new list to package it
        new_expression = []
        while token_list[0] != ')':
            # keep appending values to the new expression list
            new_expression.append(read_from_tokens(token_list))
        # remove  the ')'
        token_list.pop(0)
        return new_expression
    else:
        # code is here means token is not the start of a new expression
        # i.e. it is already in its simplest form
        # so try to find the matching data type, and return
#        return find_best_data_type(first_token)
        return first_token
        
#def find_best_data_type(data_obj):
#    
#    """
#    Finds the best possible data type for an object
#    Input: a string
#    Output: an int, float or a string depending on the input string
#    """
#    
#    try:
#        return int(data_obj)
#    except ValueError:
#        try:
#            return float(data_obj)
#        except ValueError:
#            # string
#            return data_obj
