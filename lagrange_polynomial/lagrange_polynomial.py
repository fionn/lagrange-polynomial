#!/usr/bin/env python3
"""Lagrange polynomial"""

from functools import partial
from collections.abc import Sequence
from typing import Callable, Union, overload

Polynomial = Callable[[int], int]

# pylint: disable=too-few-public-methods
class LagrangeBasis(Sequence[Polynomial]):
    """Factory class for Lagrange basis polynomials"""

    def __init__(self, x_points: Sequence[int], prime: int) -> None:
        self.xs = x_points
        self.prime = prime

    def __len__(self) -> int:
        return len(self.xs)

    @overload
    def __getitem__(self, key: int) -> Polynomial:
        pass

    @overload
    def __getitem__(self, key: slice) -> list[Polynomial]:
        pass

    def __getitem__(self, key: Union[int, slice]) -> Union[Polynomial,
                                                           list[Polynomial]]:
        if isinstance(key, int):
            return partial(self._basis, key)
        step = key.step or 1
        return [partial(self._basis, j) \
                for j in range(key.start, key.stop, step)]

    def _basis(self, j: int, x: int) -> int:
        """Lagrange basis polynomial l_j(x)"""
        x_j = self.xs[j]
        product = 1
        for x_m in self.xs:
            if x_m != x_j:
                product *= (x - x_m) // (x_j - x_m)
        return product

# pylint: disable=too-few-public-methods
class LagrangePolynomial:
    """Instantiates a Lagrange polynomial function"""

    def __init__(self, x_points: Sequence[int],
                 y_points: Sequence[int], prime: int) -> None:
        self.xs = x_points
        self.ys = y_points
        if len(self.xs) != len(self.ys):
            raise RuntimeError("The number of x- and y-coordinates must be equal")
        self.basis = LagrangeBasis(self.xs, prime)
        self.prime = prime

    def __repr__(self) -> str:
        return f"LagrangePolynomial(xs, ys, {self.prime})"

    def __call__(self, x: int) -> int:
        return self._lagrange_poly(x)

    def _lagrange_poly(self, x: int) -> int:
        """Lagrange polynomial at x"""
        total = 0
        for j, y in enumerate(self.ys):
            total += y * self.basis[j](x)
        return total

def main() -> None:
    """Entry point"""
    xs = range(700)
    ys = [x ** 6 for x in xs]

    lagrange_poly = LagrangePolynomial(xs, ys, prime=2 ** 32 - 1)

    for x in xs[620:]:
        print(x, ys[x], lagrange_poly(x))
        assert ys[x] == lagrange_poly(x)

    print(lagrange_poly(0))

if __name__ == "__main__":
    main()
