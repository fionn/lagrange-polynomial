#!/usr/bin/env python3
"""Test Lagrange interpolation"""

import unittest

from lagrange_polynomial import LagrangePolynomial

PRIME = 2 ** 31 - 1


class TestMagic(unittest.TestCase):
    """Test  magic methods"""

    def test_basis_slice(self) -> None:
        """Get a slice of basis functions"""
        xs = range(5)
        ys = [x**2 for x in xs]
        lp = LagrangePolynomial(xs, ys)
        self.assertEqual(len(xs), len(lp.basis))
        self.assertEqual([l(0) for l in lp.basis[:len(xs)]],
                         [l(0) for l in lp.basis])

    def test_different_coordinate_lengths(self) -> None:
        """We must have an equal number of x- and y-coordinates"""
        xs = range(3)
        ys = range(4)
        with self.assertRaises(RuntimeError):
            LagrangePolynomial(xs, ys)

    def test_non_unique_x(self) -> None:
        """We must have unique x-coordinates"""
        xs = [1, 1, 2]
        ys = range(3)
        with self.assertRaises(RuntimeError):
            LagrangePolynomial(xs, ys)


class TestProperties(unittest.TestCase):
    """Test basic features of Lagrange basis functions and polynomials"""

    def test_polynomial_intersection(self) -> None:
        """The polynomial intersects the original points"""
        xs = range(100)
        ys = [x**2 for x in xs]
        lp = LagrangePolynomial(xs, ys)
        for x in xs:
            self.assertEqual(ys[x], lp(x))

    def test_basis_function_is_identity_matrix(self) -> None:
        """The basis function ℓ_i at x_j is δ_ij"""
        xs = range(12)
        ys = [x**2 for x in xs]
        lp = LagrangePolynomial(xs, ys)
        for i, x_i in enumerate(xs):
            for j in range(len(xs)):
                if i != j:
                    self.assertEqual(lp.basis[j](x_i), 0)
                else:
                    self.assertEqual(lp.basis[j](x_i), 1)


class TestXSq(unittest.TestCase):
    """Check that the implementation matches specific functions"""

    def test_basis_x_sq_at_x_0(self) -> None:
        """Basis functions ℓ_j for x -> x^2 match expectation"""
        xs = [1, 2, 3]
        ys = [x**2 for x in xs]

        x = 0
        for p in [3, 17, PRIME]:
            lp = LagrangePolynomial(xs, ys, p)
            self.assertEqual(lp.basis[0](x), 3 % lp.prime)
            self.assertEqual(lp.basis[1](x), -3 % lp.prime)
            self.assertEqual(lp.basis[2](x), 1 % lp.prime)

if __name__ == "__main__":
    unittest.main(verbosity=2, buffer=True)
