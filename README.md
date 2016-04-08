# Written 2 – Functions and Memory

## Linked Stacks

Consider this alternate stack layout strategy for allocating function call
information:

1. When a closure is _created_, no longer store the count of free variables or
the values of free variables themselves.  Instead, store two other words:

      - One that contains the number of _local variables_ in the function
      - Another that contains the address of the current frame object (described
        momentarily)

    ```
    ---------------------------------------------------------
    | 101 |  0  |  frame ptr  | #locals | arity  | code ptr |
    ---------------------------------------------------------
    ```


2.  When _calling_ a function, the caller allocates a _frame object_ on the
heap, with tag `011`, GC word `0`, a size counter equal to `arity` + `#locals`,
a _previous pointer_ that is set to the _closure's_ frame pointer, and space
for `arity` + `#locals` elements:

    ```
    --------------------------------------------------------------------
    | 011 |  0  |  size  |  prev ptr | element1  | ... | maybe padding |
    --------------------------------------------------------------------
    ```

    Then, push onto the stack the address of this frame object, copy the arguments
    to the call into the first _n_ elements (where _n_ is the number of arguments,
    and may be smaller than _N_).  Then `call` the function.


3.  When _called_, a function pushes the current value of `EBP`, and then sets
`EBP` to the address of the frame object it was passed.  All local variable and
argument references are performed by offset from `EBP` into the frame object.
Instead of restoring free variables from the closure onto the stack, free
variables are compiled to use the _previous pointer_ to look up the right
location.



```
|---------------|
| old frame ptr |
|---------------|
|   return ptr  |
|---------------|
|   frame ptr   |
|---------------|
| old frame ptr |
|---------------|
|   return ptr  |
|---------------|
|   frame ptr   |
|---------------|
|      ...      |
|---------------|
```



## Variable-Arity Functions

Many languages support _variable-arity_ functions.  For example, in Python, an
asterisk before the final argument indicates that it will hold all additional
arguments that are provided.  If too few arguments are provided, it is still an
error.  See `variable.py` for some examples.

Design and describe a calling convention for variable arity functions added to
Egg-Eater.  You're free to consider the linked stack implementation above, or
the implementation we've been using in 


