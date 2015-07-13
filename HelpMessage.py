
"""
The script that prints the help message.

@author: aashishsatya
"""

def print_help():

    print '\nThis is a program that helps prove (or acknowledge non-provability of)'
    print 'a statement based on a given a set of propositions in first-order logic.'
    print 'The proof process is also displayed.'
    print 'The strategy used to prove statements is backward chaining with unification.\n'

    print 'The following logical connectives are supported:\n'

    print '& - and'
    print '==> - implies'
    print '~ (tilde) - not'
    print '| (pipe) - or\n'

    print 'Only definite clauses (a disjunction of clauses that have just one positive literal)'
    print 'are allowed (the program actually ensures this). For e.g.'
    print 'Kid(x) & Loves(Chocolate, x) ==> Awesome(x)'
    print 'is allowed (as P ==> Q translates to ~P | Q), but not'
    print 'King(Ashoka) | Just(Ashoka) | ~Evil(Ashoka)'
    print 'as there are two positive literals in the above statement.\n'

    print 'Oh, and this is important: variables are named using small letters and values using words with'
    print 'atleast their first letter capital. For e.g. in'
    print 'Spy(x)'
    print 'x can take on any values like Bond, Hunt or Powers, but'
    print 'Spy(X)'
    print 'would mean a spy whose name is X -- X cannot be substituted with Bourne or Tasker.\n'

    print 'Also do not use spaces between your names.\n'

    print 'Using the program:\n'

    print 'Simply enter propositions one by one (press Enter after each). Enter STOP to stop feeding clauses to the knowledge base.'
    print "Input your statement to prove and you're done!! Simple as that :-)\n"

    print 'RECOMMENDED HACK:\n'
    print 'Commenting some set of statements and uncommenting some others (see AutoProver.py) lets you use the'
    print 'program as a query-based system on first order logic. This is FAR more powerful than a simple theorem prover,'
    print 'and comes highly recommended.\n'

    print 'Demo run:\n'

    print 'Enter statements in first-order logic one by one:'
    print 'Enter STOP when done.\n'

    print 'King(x) ==> Person(x)'
    print 'King(Charles)'
    print 'STOP\n'

    print 'Enter statement to prove: Person(Charles)\n'

    print 'Proof:\n'

    print 'We know King(Charles) (given)'
    print 'which leads to King(Charles) ==> Person(Charles) (Rule of universal instantiation on King(x) ==> Person(x))'
    print 'which leads to Person(Charles) (Modus Ponens)\n'    

    print 'As always feel free to contact me at ankarathaashish@gmail.com if you have any bug reports or suggestions for improvement.'
    print 'Thank you!!\n'
    print 'Enter statements in first-order logic one by one:'
    print 'Enter STOP when done.\n'
