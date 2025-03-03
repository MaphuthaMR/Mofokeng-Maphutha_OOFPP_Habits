# My Habit Tracker Application
This Habit Tracking App is designed to help users create and manage habits, track progress, and analyze their habit-forming journey. The app is built using Python and utilizes a SQLite database for storing habit data.

## Features
Create and manage daily and weekly habits.
Track habit completion and streaks.
Analyze habits. 
Store and load habit data using a SQLite database 
Command-line interface (CLI) for user interaction.

# Installation and Usage


## Installation
1. Clone the repository: git clone https://github.com/MaphuthaMR/Mofokeng-Maphutha_OOFPP
2. Navigate to the project directory: cd habit-tracking-app
3. Install dependencies: pip install -r requirements.txt

## Usage
1. Run the app: python main.py
2. Follow the interactive menu prompts to create, manage, and analyze habits.
## Code Structure


The code is organized into several functions:

get_habit_id(): Retrieves the habit ID from the user.
get_habit(habit_id): Retrieves the habit object from the database.
main_menu(): Displays the main menu and handles user input.
create_habit(): Creates a new habit.
edit_habit(): Edits an existing habit.
delete_habit(): Deletes a habit.
analyze_habit(): Analyzes a habit and displays its streak.
 
