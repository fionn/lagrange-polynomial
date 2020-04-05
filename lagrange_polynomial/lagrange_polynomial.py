#!/usr/bin/env python3
"""Lagrange polynomial"""

from functools import partial
from typing import List, Sequence, Callable, Union, overload

Polynomial = Callable[[float], float]

# pylint: disable=too-few-public-methods
class LagrangeBasis(Sequence[Polynomial]):
    """Factory class for Lagrange basis polynomials"""

    def __init__(self, x_points: Sequence[float]) -> None:
        self.xs = x_points

    def __len__(self) -> int:
        return len(self.xs)

    @overload
    def __getitem__(self, key: int) -> Polynomial:
        pass

    @overload
    def __getitem__(self, key: slice) -> List[Polynomial]:
        pass

    def __getitem__(self, key: Union[int, slice]) -> Union[Polynomial,
                                                           List[Polynomial]]:
        if isinstance(key, int):
            return partial(self._basis, key)
        step = key.step or 1
        return [partial(self._basis, j) \
                for j in range(key.start, key.stop, step)]

    def _basis(self, j: int, x: float) -> float:
        """Lagrange basis polynomial l_j(x)"""
        x_j = self.xs[j]
        product = 1.0
        for x_m in self.xs:
            if x_m != x_j:
                product *= (x - x_m) / (x_j - x_m)
        return product

# pylint: disable=too-few-public-methods
class LagrangePolynomial:
    """Instantiates a Lagrange polynomial function"""

    def __init__(self, x_points: Sequence[float],
                 y_points: Sequence[float]) -> None:
        self.xs = x_points
        self.ys = y_points
        if len(self.xs) != len(self.ys):
            raise RuntimeError("The number of x- and y-coordinates must be equal")
        self.basis = LagrangeBasis(self.xs)

    def __call__(self, x: float) -> float:
        return self._lagrange_poly(x)

    def _lagrange_poly(self, x: float) -> float:
        """Lagrange polynomial at x"""
        total = 0.0
        for j in range(len(self.ys)):
            total += self.ys[j] * self.basis[j](x)
        return total

def main() -> None:
    """Entry point"""
    xs = range(0, 100)
    ys = [x ** 5 for x in xs]

    lagrange_poly = LagrangePolynomial(xs, ys)

    for x in xs:
        print(x, ys[x], lagrange_poly(x))
        assert ys[x] == lagrange_poly(x)

if __name__ == "__main__":
    main()
