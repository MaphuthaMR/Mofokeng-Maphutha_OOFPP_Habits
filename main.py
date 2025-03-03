import questionary
from habit import Habit, WeeklyHabit
def get_habit_id():
    """Get the habit ID from the user."""
    while True:
        try:
            habit_id = int(questionary.text("Enter the ID of the habit:").ask())
            return habit_id
        except ValueError:
            print("Invalid habit ID. Please enter a valid integer.")

def get_habit(habit_id):
    """Get the habit object from the database."""
    habit = Habit.get_by_id(habit_id)
    if not habit:
        print("Habit not found!")
        return None
    return habit

def main_menu():
    """Display the main menu."""
    choice = questionary.select(
        "Choose an action:",
        choices=[
            "Create Habit",
            "Edit Habit",
            "Delete Habit",
            "Analyze Habit",
            "Exit"
        ]
    ).ask()
    if choice == "Create Habit":
        create_habit()
    elif choice == "Edit Habit":
        edit_habit()
    elif choice == "Delete Habit":
        delete_habit()
    elif choice == "Analyze Habit":
        analyze_habit()
    elif choice == "Exit":
        exit()

def create_habit():
    """Create a new habit."""
    name = questionary.text("Enter the habit name:").ask()
    description = questionary.text("Enter the habit description:").ask()
    habit = Habit(name=name, description=description)
    habit.save()
    print("Habit saved successfully!")
    main_menu()

def edit_habit():
    """Edit an existing habit."""
    habit_id = get_habit_id()
    habit = get_habit(habit_id)
    if not habit:
        return
    name = questionary.text(f"Enter the new name (current: {habit.name}):").ask()
    description = questionary.text(f"Enter the new description (current: {habit.description}):").ask()
    habit.name = name
    habit.description = description
    habit.save()
    print("Habit updated successfully!")
    main_menu()

def delete_habit():
    """Delete a habit."""
    habit_id = get_habit_id()
    habit = get_habit(habit_id)
    if not habit:
        return
    confirmation = questionary.confirm(f"Are you sure you want to delete the habit '{habit.name}'?").ask()
    if confirmation:
        habit.delete()
        print("Habit deleted successfully!")
    main_menu()

def analyze_habit():
    """Analyze a habit."""
    habit_id = get_habit_id()
    habit = get_habit(habit_id)
    if not habit:
        return

    print(f"Habit: {habit.name}")
    print(f"Description: {habit.description}")

    # Check if the habit is a weekly habit and use the correct method
    if isinstance(habit, WeeklyHabit):
        weekly_streak = habit.compute_streak()
        print(f"Current weekly streak: {weekly_streak} weeks")
    else:  # Default to daily habit
        daily_streak = habit.compute_streak()
        print(f"Current daily streak: {daily_streak} days")

    main_menu()

if __name__ == "__main__":
    main_menu()

