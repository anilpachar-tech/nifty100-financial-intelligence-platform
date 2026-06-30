import unittest

from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover
)


class TestLeverageRatios(unittest.TestCase):

    # Test 1
    def test_debt_to_equity_normal(self):
        self.assertEqual(
            debt_to_equity(
                500,
                200,
                300
            ),
            1.0
        )

    # Test 2
    def test_debt_to_equity_debt_free(self):
        self.assertEqual(
            debt_to_equity(
                0,
                200,
                300
            ),
            0.0
        )

    # Test 3
    def test_interest_coverage_normal(self):
        self.assertEqual(
            interest_coverage_ratio(
                100,
                20,
                10
            ),
            12.0
        )

    # Test 4
    def test_interest_zero(self):
        self.assertIsNone(
            interest_coverage_ratio(
                100,
                20,
                0
            )
        )

    # Test 5
    def test_icr_label(self):
        self.assertEqual(
            icr_label(0),
            "Debt Free"
        )

    # Test 6
    def test_high_leverage_flag(self):
        self.assertTrue(
            high_leverage_flag(
                6.0,
                "Industrials"
            )
        )

    # Test 7
    def test_net_debt(self):
        self.assertEqual(
            net_debt(
                500,
                100
            ),
            400
        )

    # Test 8
    def test_asset_turnover(self):
        self.assertEqual(
            asset_turnover(
                1000,
                500
            ),
            2.0
        )


if __name__ == "__main__":
    unittest.main()