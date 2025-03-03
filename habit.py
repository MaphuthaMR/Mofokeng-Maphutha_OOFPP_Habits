import sqlite3
from datetime import datetime, timedelta, date
class Habit:
    """A base class that defines a habit, its data, and behavior."""
    _DB_NAME = "habits.db"
    def __init__(self, habit_id=None, name=None, description=None):
        self.habit_id = habit_id
        self.name = name
        self.description = description
        self.completed_dates = []  # Initialize as an empty list
        self._initialize_db()

    def save(self):
        """
        Saves a habit to the database. If the habit already exists (based on habit_id), it updates the record.
        Otherwise, it creates a new record and assigns the generated habit_id to the instance.
        """
        try:
            with sqlite3.connect(self._DB_NAME) as conn:
                cursor = conn.cursor()
                # Update existing habit or create a new one
                if self.habit_id:
                    cursor.execute(
                        "UPDATE habit SET name = ?, description = ? WHERE id = ?",
                        (self.name, self.description, self.habit_id),
                    )
                else:
                    cursor.execute(
                        "INSERT INTO habit (name, description) VALUES (?, ?)",
                        (self.name, self.description),
                    )
                    self.habit_id = cursor.lastrowid
                # Fetch existing completed dates
                cursor.execute(
                    "SELECT completed_date FROM tracking WHERE habit_id = ?",
                    (self.habit_id,),
                )
                existing_dates = {row[0] for row in cursor.fetchall()}
                # Insert new completed dates
                for date in [d.isoformat() for d in self.completed_dates if d.isoformat() not in existing_dates]:
                    cursor.execute(
                        "INSERT INTO tracking (habit_id, completed_date) VALUES (?, ?)",
                        (self.habit_id, date),
                    )
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            raise

    def delete(self):
        """Deletes the habit and its associated tracking data from the database."""
        if not self.habit_id:
            raise ValueError("Cannot delete a habit that has not been saved to the database.")
        with sqlite3.connect(self._DB_NAME) as conn:
            cursor = conn.cursor()
            # Delete tracking data associated with this habit
            cursor.execute("DELETE FROM tracking WHERE habit_id = ?", (self.habit_id,))
            # Delete the habit itself
            cursor.execute("DELETE FROM habit WHERE id = ?", (self.habit_id,))
            conn.commit()
            print(f"Habit '{self.name}' and associated data have been deleted.")

    @classmethod
    def get_by_id(cls, habit_id):
        """Retrieve a habit by its ID."""
        with sqlite3.connect(cls._DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, description FROM habit WHERE id = ?",
                (habit_id,),
            )
            result = cursor.fetchone()
            if not result:
                return None
            habit = cls(habit_id=result[0], name=result[1], description=result[2])
            cursor.execute(
                "SELECT completed_date FROM tracking WHERE habit_id = ?",
                (habit_id,),
            )
            habit.completed_dates = [
                datetime.fromisoformat(row[0]).date() for row in cursor.fetchall()
            ]
            return habit
    def check(self, check_date=None):
        """Mark a habit as completed on a specific date."""
        if check_date is None:
            check_date = date.today()
        if check_date not in self.completed_dates:
            self.completed_dates.append(check_date)
    def compute_streak(self):
        """Compute the longest streak of completed dates."""
        if not self.completed_dates:
            return 0
        sorted_dates = sorted(self.completed_dates)
        longest_streak = current_streak = 1
        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] - sorted_dates[i - 1] == timedelta(days=1):
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1
        return longest_streak
    def _initialize_db(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self._DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS habit (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT
                )"""
            )
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS tracking (
                    id INTEGER PRIMARY KEY,
                    habit_id INTEGER,
                    completed_date TEXT,
                    FOREIGN KEY (habit_id) REFERENCES habit (id)
                )"""
            )
            conn.commit()
class DailyHabit(Habit):
    """A subclass for daily habits."""

    def __init__(self, habit_id=None, name=None, description=None):
        super().__init__(habit_id, name, description)

class WeeklyHabit(Habit):
    # A class to compute the longest weekly streak
    def compute_streak(self, current_date=None):
        if current_date is None:
            current_date = date.today()
        if not self.completed_dates:
            return 0

        # Sort completed dates
        self.completed_dates.sort()

        # Calculate streak
        max_streak = 0
        current_streak = 0
        for i in range(len(self.completed_dates)):
            if i == 0 or (self.completed_dates[i] - self.completed_dates[i-1]).days == 7:
                current_streak += 1
            else:
                current_streak = 1
            max_streak = max(max_streak, current_streak)

        return max_streak