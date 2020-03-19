# Lagrange Polynomials

Module to generate Lagrange polynomials for 1-dimensional data.
This is generally useful for interpolation.

## Interface

```python
from lagrange_polynomial import LagrangePolynomial

xs = range(0, 100)
ys = [f(x) for x in xs]          # For some function f

lp = LagrangePolynomial(xs, ys)  # Instantiate a polynomial with sequences of
                                 # x- and y-coordinates.

for x in xs:
    assert ys[x] == lp(x)        # Polynomial will intersect original points
    coefficient = lp.basis[0](x) # Get the 0th basis vector at x
```

`LagrangePolynomial` takes two equally-sized sequences on initialisation.
The instance is a Lagrange polynomial _L_: _x_ -> _L_(_x_).

It has a `basis` property, a `LagrangeBasis` object subclassing `Sequence`.
Each element indexed by integers in `range(len(xs))` is a function taking _x_ to its basis vector.
