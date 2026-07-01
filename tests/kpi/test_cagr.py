import unittest

from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr
)


class TestCAGR(unittest.TestCase):

    # Test 1
    def test_normal_cagr(self):
        value, flag = calculate_cagr(
            100,
            200,
            5
        )

        self.assertEqual(flag, "NORMAL")
        self.assertIsNotNone(value)

    # Test 2
    def test_zero_base(self):
        value, flag = calculate_cagr(
            0,
            200,
            5
        )

        self.assertIsNone(value)
        self.assertEqual(flag, "ZERO_BASE")

    # Test 3
    def test_decline_to_loss(self):
        value, flag = calculate_cagr(
            100,
            -50,
            5
        )

        self.assertIsNone(value)
        self.assertEqual(
            flag,
            "DECLINE_TO_LOSS"
        )

    # Test 4
    def test_turnaround(self):
        value, flag = calculate_cagr(
            -100,
            50,
            5
        )

        self.assertIsNone(value)
        self.assertEqual(
            flag,
            "TURNAROUND"
        )

    # Test 5
    def test_both_negative(self):
        value, flag = calculate_cagr(
            -100,
            -50,
            5
        )

        self.assertIsNone(value)
        self.assertEqual(
            flag,
            "BOTH_NEGATIVE"
        )

    # Test 6
    def test_insufficient_years(self):
        value, flag = calculate_cagr(
            100,
            200,
            2
        )

        self.assertIsNone(value)
        self.assertEqual(
            flag,
            "INSUFFICIENT"
        )

    # Test 7
    def test_invalid_period(self):
        value, flag = calculate_cagr(
            100,
            200,
            0
        )

        self.assertIsNone(value)
        self.assertEqual(
            flag,
            "INVALID_PERIOD"
        )

    # Test 8
    def test_revenue_cagr(self):
        value, flag = revenue_cagr(
            100,
            200,
            5
        )

        self.assertEqual(flag, "NORMAL")
        self.assertIsNotNone(value)

    # Test 9
    def test_pat_cagr(self):
        value, flag = pat_cagr(
            100,
            200,
            5
        )

        self.assertEqual(flag, "NORMAL")
        self.assertIsNotNone(value)

    # Test 10
    def test_eps_cagr(self):
        value, flag = eps_cagr(
            10,
            20,
            5
        )

        self.assertEqual(flag, "NORMAL")
        self.assertIsNotNone(value)


if __name__ == "__main__":
    unittest.main()