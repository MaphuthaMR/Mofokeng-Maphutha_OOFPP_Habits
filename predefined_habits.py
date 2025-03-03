import sqlite3
from datetime import datetime, timedelta
from habit import Habit, DailyHabit, WeeklyHabit  # Import from your habit module
# Define predefined habits
predefined_habits = [
    DailyHabit(name="Pray", description="Pray at least 3 times a day."),
    DailyHabit(name="Exercise", description="Do 1 hour of exercise."),
    DailyHabit(name="Read", description="Read at least 10 pages of a book."),
    WeeklyHabit(name="Clean Room", description="Do a deep cleaning of the room every Sunday."),
    WeeklyHabit(name="Call Family", description="Call family members at least once a week."),
]
# Insert habits into the database
def insert_predefined_habits():
    for habit in predefined_habits:
        habit.save()
        print(f"Predefined Habit Added: {habit.name}")

if __name__ == "__main__":
    insert_predefined_habits()
