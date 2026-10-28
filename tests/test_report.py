import unittest
from datetime import date

from generator import build_csv, last_week_range


class GeneratorTests(unittest.TestCase):
    def test_last_week_range_is_seven_days(self) -> None:
        since, until = last_week_range(date(2026, 10, 28))
        self.assertEqual(since, "2026-10-21")
        self.assertEqual(until, "2026-10-27")

    def test_build_csv_contains_all_sections(self) -> None:
        summary = [
            {"product": "A", "units_sold": 2, "total_revenue": 49.80},
            {"product": "B", "units_sold": 1, "total_revenue": 10.00},
        ]
        daily = [{"day": "2026-10-01", "revenue": 59.80}]
        output = build_csv(summary, daily, "2026-10-01", "2026-10-07")
        self.assertIn("Sales report 2026-10-01 to 2026-10-07", output)
        self.assertIn("Product,Units sold,Revenue", output)
        self.assertIn("A,2,49.80", output)
        self.assertIn("B,1,10.00", output)
        self.assertIn("Day,Revenue", output)
        self.assertIn("2026-10-01,59.80", output)
        self.assertIn("Total,,59.80", output)

    def test_build_csv_with_no_rows(self) -> None:
        output = build_csv([], [], "2026-10-01", "2026-10-07")
        self.assertIn("Total,,0.00", output)


if __name__ == "__main__":
    unittest.main()