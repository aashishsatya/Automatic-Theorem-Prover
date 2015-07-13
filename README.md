# Automatic Theorem Prover

This is a program that helps prove (or acknowledge non-provability of) a statement based on a given a set of propositions in first-order logic. The proof process is also displayed. The strategy used is backward chaining with unification. 

The following logical connectives are supported:

& - and
==> - implies
~ (tilde) - not
| (pipe) - or

Only knowledge bases using definite clauses (a disjunction of clauses that have just one positive literal) are allowed. For e.g.

Kid(x) & Loves(Chocolate, x) ==> Awesome(x)

is allowed (as P ==> Q translates to ~P | Q), but not

King(Ashoka) | Just(Ashoka) | ~Evil(Ashoka)

as there are two positive literals in the above statement.

Oh, and this is important: variables are named using small letters and values using words with atleast their first letter capital. For e.g. in 

Spy(x)

x can take on any values like Bond, Hunt or Powers, but

Spy(X)

would mean a spy whose name is X -- X cannot be substituted with Bourne or Tasker.

Also do not use spaces between names.

#####Running the program:

Run the script 'AutoProver.py' by executing

python AutoProver.py

once you're in the directory that has all the scripts included with the program.

Simply enter propositions one by one (press Enter after each). Enter STOP to stop feeding clauses to the knowledge base.
Input your statement to prove and you're done!! Simple as that :-)

#####RECOMMENDED HACK:

Commenting some set of statements and uncommenting some others (see AutoProver.py) lets you use the program as a query based system in first order logic. This is FAR more powerful than a simple theorem prover, and comes highly recommended.

#####Demo run:

Enter statements in first-order logic one by one:
Enter STOP when done.

King(x) ==> Person(x)
King(Charles)
STOP

Enter statement to prove: Person(Charles)

Proof:

We know King(Charles) (given)
which leads to King(Charles) ==> Person(Charles) (Rule of universal instantiation on King(x) ==> Person(x))
which leads to Person(Charles) (Modus Ponens)


All this information is displayed when a help command (HELP) is invocated in the program.

As always feel free to contact me at ankarathaashish@gmail.com if you have any bug reports or suggestions for improvement. Thank you!!


