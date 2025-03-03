import pytest
import sqlite3
from datetime import date, datetime
from habit import Habit, DailyHabit, WeeklyHabit

class TestHabit:
    def setup_method(self):
        self.habit = Habit(name ="Study",description = "Read a chapter in a book")
    def test_single_dates(self):
        self.habit.check(datetime(2025, 1, 18))
        assert self.habit.compute_streak() == 1

    def test_multiple_dates(self):
        self.habit.check(datetime(2025, 1, 18))
        self.habit.check(datetime(2025, 1, 19))
        self.habit.check(datetime(2025, 1, 20))
        assert self.habit.compute_streak() == 3

        # checking non-consecutive dates
        self.habit.check(datetime(2023, 8, 22))
        assert self.habit.compute_streak() == 3  # streak should still be 3

    def test_random_order_dates(self):
            # Checking dates in random order
            self.habit.check(datetime(2025, 1, 19))
            self.habit.check(datetime(2025, 1, 17))
            self.habit.check(datetime(2025, 1, 18))
            assert self.habit.compute_streak() == 3

    def teardown_method(self):
            # Clean up the habit instance
            del self.habit

class TestWeeklyHabit:
    def setup_method(self):
        self.habit = WeeklyHabit(name="Weekly Habit", description="A weekly habit")

    def test_weekly_streak(self):
        # Complete habit every week for 4 weeks
        self.habit.check(date(2025, 2, 3))
        self.habit.check(date(2025, 2, 10))
        self.habit.check(date(2025, 2, 17))
        self.habit.check(date(2025, 2, 24))
        assert self.habit.compute_streak() == 4

    def test_incomplete_weekly_streak(self):
        # Complete habit for 2 weeks, then miss a week
        self.habit.check(date(2025, 2, 3))
        self.habit.check(date(2025, 2, 10))
        assert self.habit.compute_streak() == 2

    def test_discontinuous_weekly_streak(self):
        # Complete habit for 2 weeks, then complete it again 2 weeks later
        self.habit.check(date(2025, 2, 3))
        self.habit.check(date(2025, 2, 10))
        self.habit.check(date(2025, 2, 24))
        assert self.habit.compute_streak() == 2

    def teardown_method(self):
        del self.habit

# Run the tests
pytest.main()


