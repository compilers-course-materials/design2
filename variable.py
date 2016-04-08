def f(x, *y):
  return y

print(f(1, 2, 3))  # (2, 3) is bound to y

print

print(f(1))   # an empty tuple is bound to y

print

print(f())    # an arity error
