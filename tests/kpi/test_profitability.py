import unittest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    opm_cross_check,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets
)


class TestProfitabilityRatios(unittest.TestCase):

    # Test 1
    def test_net_profit_margin_normal(self):
        self.assertEqual(
            net_profit_margin(20, 100),
            20.00
        )

    # Test 2
    def test_net_profit_margin_zero_sales(self):
        self.assertIsNone(
            net_profit_margin(50, 0)
        )

    # Test 3
    def test_operating_profit_margin_normal(self):
        self.assertEqual(
            operating_profit_margin(25, 100),
            25.00
        )

    # Test 4
    def test_opm_cross_check_pass(self):
        self.assertTrue(
            opm_cross_check(25.0, 25.5)
        )

    # Test 5
    def test_opm_cross_check_fail(self):
        self.assertFalse(
            opm_cross_check(20.0, 22.5)
        )

    # Test 6
    def test_return_on_equity_normal(self):
        self.assertEqual(
            return_on_equity(
                100,
                400,
                100
            ),
            20.00
        )

    # Test 7
    def test_return_on_equity_negative_equity(self):
        self.assertIsNone(
            return_on_equity(
                100,
                -500,
                100
            )
        )

    # Test 8
    def test_return_on_assets_zero_assets(self):
        self.assertIsNone(
            return_on_assets(
                100,
                0
            )
        )


if __name__ == "__main__":
    unittest.main()