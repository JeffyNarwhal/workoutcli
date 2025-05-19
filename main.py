import csv, os, cmd, datetime
from rich.console import Console
from rich.table import Table
import pandas as pd

filename = "data.csv"
console = Console()
pd.set_option('display.max_rows', 900)

class FileManagerCLI(cmd.Cmd):
    prompt = "WorkoutCli>> "
    intro = 'Welcome to WorkoutCLI. Type "help" for available commands.'

    def __init__(self):
        super().__init__()
        self.current_directory = os.path.dirname(os.path.realpath(__file__)) # Sets directory to file directory so creating the csv works
        try:
            with open(filename, 'x') as file:
                with open(filename, 'w', newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Exercise", "Reps", "Weight", "Date"])
        except FileExistsError:
            pass
        except Exception as e:
            print(f"Error: {e}")

    def do_add(self, line):
        """Adds a workout
        Format: add "Exercise Name" Reps Weight [Date (YYYY-MM-DD)]
        Example: add "Bench Press" 8 135 2025-05-19
                 add "Squat" 5 225 (uses today's date)"""
        # Split input while respecting quoted strings
        try:
            # Use shlex to handle quoted strings (e.g., "Bench Press")
            import shlex
            args = shlex.split(line)
        except ValueError:
            print("Error: Invalid input format. Use quotes for multi-word exercises.")
            return

        # Validate number of arguments
        if len(args) < 3 or len(args) > 4:
            print("Error: Expected format: add \"Exercise Name\" Reps Weight [Date]")
            return

        # Extract arguments
        exercise = args[0]
        try:
            reps = int(args[1])  # Ensure reps is an integer
            weight = float(args[2])  # Ensure weight is a number
        except ValueError:
            print("Error: Reps and Weight must be numbers.")
            return

        # Handle date (default to today if not provided)
        if len(args) == 4:
            try:
                date = pd.to_datetime(args[3]).date()  # Validate and convert to date
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD.")
                return
        else:
            date = datetime.date.today()

        # Create a new row as a DataFrame
        new_row = pd.DataFrame({
            'Exercise': [exercise],
            'Reps': [reps],
            'Weight': [weight],
            'Date': [date]
        })

        try:
            # Check if file exists
            if os.path.exists(filename):
                # Read existing CSV
                df = pd.read_csv(filename)
                # Append new row
                df = pd.concat([df, new_row], ignore_index=True)
            else:
                # If file doesn't exist, use new_row as the DataFrame
                df = new_row

            # Write back to CSV
            df.to_csv(filename, index=False)
            print(f"Added: {exercise}, {reps} reps, {weight} lbs, {date}")
        except Exception as e:
            print(f"Error writing to file: {e}")
    
    def do_exercises(self, line):
        """Prints Exercises"""
        exercises = set()
        try:
            with open(filename, "r") as file:
                for row in file:
                    x = row.split(",")
                    if (x[0] == "Exercise"):
                        continue
                    exercises.add(x[0])
            exercises = sorted(exercises)
            for exercise in exercises:
                print(exercise)
        except Exception as e:
            print(f"Error: {e}")

    def do_view(self, line):
        """Prints workouts"""
        print(pd.read_csv(filename))
    
    def do_sort(sort, line):
        """Sorts"""
        try:
            csvData = pd.read_csv(filename)
            csvData.sort_values([line], 
                                axis=0,
                                ascending=[True], 
                                inplace=True)
            csvData.to_csv(filename, index=0)
        except Exception as e:
            print(f"Error: {e}")

    def do_clear(self, arg):
        """Clear the terminal screen."""
        os.system('cls')

    def do_quit(self, line):
        """Exit the CLI."""
        return True

if __name__ == '__main__':
    FileManagerCLI().cmdloop()