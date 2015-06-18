# Automatic Theorem Prover

WARNING: Program in early stages of development, even this README might be incorrect!!

This is a program that helps prove (or acknowledge non-provability of) a given query based on a given a set of propositions in first-order logic by logical inferences. The strategy used is backward chaining with unification. 

Only the following logical connectives are supported as of now:

& - and
==> - implies

NOT SUPPORTED YET:

~ (tilde) - not
| (pipe) - or

For the time being, only very small knowledge bases using definite clauses (a disjunction of clauses that have just one positive literal - all the others are negated) are assumed. For e.g.

Kid(x) & Loves(Ice cream, x) ==> Awesome(x)

is allowed (as P ==> Q translates to ~P | Q), but not

King(Ashoka) | Just(Ashoka) | ~Evil(Ashoka)

as there are two positive literals in the above statement.

Nested clauses, such as ~(King(Charles) & Prince(Charles)) | Person(Charles) which are technically definite clauses are also not yet supported.

Oh, and this is important: variables are named using small letters and values using words with atleast their first letter capital. For e.g. in 

Spy(x)

x can take on any values like Bond, Johnny English or Kim, but

Spy(X)

would mean a spy whose name is X -- X cannot be substituted with Joe or Bond.

All the above information will be displayed when a help command is invocated in the program (not implemented yet).

As always feel free to contact me at ankarathaashish@gmail.com if you have any bug reports or suggestions for improvement. Thank you!!


