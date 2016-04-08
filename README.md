# Written 2 – Functions and Memory

This assignment is due by 11:59pm on Monday, April 18.

## When to Garbage Collect

In the Garbage assignment, we trigger collection only when out of memory.  Some
languages, like Java, provide a runtime function that triggers garbage
collection manually:
[System.gc()](https://docs.oracle.com/javase/8/docs/api/java/lang/Runtime.html#gc--).

Are there any benefits to running the garbage collector before the heap is
full, and/or triggered by the user's program?  For simplicity, assume our
mark/compact implementation for the collector.  Why or why not?

## Variable-Arity Functions

Many languages support _variable-arity_ functions.  For example, in Python, an
asterisk before the final argument indicates that it will hold all additional
arguments that are provided.  If too few arguments are provided, it is still an
error.  See `variable.py` for some examples.

Design and describe a calling convention for variable arity functions added to
Egg-Eater (so using global `def` declarations, not closures).  Assume the same
syntax, so a variable-arity function is declared with an asterisk before the
last parameter.  This should evaluate to `(2, 3)`, for instance:

```
def f(x, *y):
  y
f(1, 2, 3)
```

Describe what in the implementation of the compiler you would need to change,
what effects this would have on the rest of the language, and give examples of
the new instructions that would be produced for function calls.

## Heap-allocated Stack Frames and Linked Closures

Consider this alternate stack layout strategy for allocating function call
information:

1. When a closure is _created_, no longer store the count of free variables or
the values of free variables themselves.  Instead, store two other words:

      - One that contains the number of _local variables_ in the function (e.g.
        the result of `count_vars` on the body)
      - Another that contains the address of the current frame object (described
        in the next step)

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

    Then, push onto the stack the address of this frame object, copy the
    arguments to the call into the first `arity` elements.  Then `call` the
    function.


3.  When _called_, a function pushes the current value of `EBP`, and then sets
`EBP` to the address of the frame object it was passed.  All local variable and
argument references are performed by offset from `EBP` into the frame object.
Instead of restoring free variables from the closure onto the stack, free
variables are compiled to use the _previous pointer_ to look up the correct
location.  (This means that for each variable, the compiler will track how many
nested `lambda` expressions above it was bound in, and traverse that many
previous pointers to find it.)

4.  When the main program starts, it allocates a frame object for the main
expression's variables, and puts that address in `EBP`.  This frame pointer has
the special value `0` for its previous pointer.

The net effect of these changes is to put all function call information (other
than return pointers and addresses of frames) on the _heap_.


### Question A:

For each of the following scenarios, discuss the tradeoffs this approach would
have in terms of memory and time needed.  Hint – draw pictures.

- Evaluating a function body that creates 10 closures, each of which refers to
  5 free variables.  For example:

  ```
  let f = (lambda a, b, c, d, e:
    let g0 = (lambda: a + b + c + d + e),
        g1 = (lambda: a + b + c + d + e),
        g2 = (lambda: a + b + c + d + e),
        g3 = (lambda: a + b + c + d + e),
        g4 = (lambda: a + b + c + d + e),
        g5 = (lambda: a + b + c + d + e),
        g6 = (lambda: a + b + c + d + e),
        g7 = (lambda: a + b + c + d + e),
        g8 = (lambda: a + b + c + d + e),
        g9 = (lambda: a + b + c + d + e) in
    (g0, g1, g2, g3, g4, g5, g6, g7, g8, g9) in

  f(1, 2, 3, 4, 5)[0]()
  ```

- Evaluating a function body that was nested 5 functions deep and refers to a
  variable that was an argument to the outermost function repeatedly, for
  example:

  ```
  let f = (lambda x: (lambda: (lambda: (lambda: (lambda: x + x + x + x))))) in
  f(10)()()()()
  ```

### Question B:

Does this layout of function call information and closures afford us any more
flexibility in how we implement variables?  Why or why not?



