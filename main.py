import csv, os, cmd, datetime
import pandas as pd
import shlex

filename = "data.csv"
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

    def do_view(self, line):
        """View workouts with optional filters
        Format: view [Column=Value] [Column=Value] ...
        Example: view Exercise="Bench Press"
                 view Exercise="Bench Press" Reps=8
                 view (shows all workouts)"""
        try:
            # Check if file exists
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' not found.")
                return

            # Read the CSV
            df = pd.read_csv(filename)

            # If no filters provided, show all rows
            if not line.strip():
                print(df.to_string(index=False))
                return

            # Parse filters using shlex to handle quoted strings
            try:
                args = shlex.split(line)
            except ValueError:
                print("Error: Invalid input format. Use quotes for multi-word values (e.g., Exercise=\"Bench Press\").")
                return

            # Validate and extract filters
            filters = {}
            for arg in args:
                if '=' not in arg:
                    print(f"Error: Invalid filter format in '{arg}'. Use Column=Value.")
                    return
                column, value = arg.split('=', 1)  # Split on first '=' only
                if column not in df.columns:
                    print(f"Error: Column '{column}' not found in CSV.")
                    return
                filters[column] = value

            # Apply filters
            filtered_df = df.copy()
            for column, value in filters.items():
                # Convert value to appropriate type based on column
                if column in ['Reps', 'Weight']:
                    try:
                        value = float(value)  # Allow integers or floats
                        filtered_df = filtered_df[filtered_df[column] == value]
                    except ValueError:
                        print(f"Error: Value '{value}' for '{column}' must be a number.")
                        return
                elif column == 'Date':
                    try:
                        value = pd.to_datetime(value).date()  # Convert to date
                        filtered_df = filtered_df[filtered_df[column] == str(value)]
                    except ValueError:
                        print(f"Error: Invalid date format for '{column}'. Use YYYY-MM-DD.")
                        return
                else:  # Exercise or other string columns
                    filtered_df = filtered_df[filtered_df[column] == value]

            # Display results
            if filtered_df.empty:
                print("No workouts match the specified filters.")
            else:
                print(filtered_df.to_string(index=False))

        except Exception as e:
            print(f"Error: {e}")
    
    def do_sort(sort, line):
        """Sorts"""
        try:
            csvData = pd.read_csv(filename)
            csvData.sort_values(line, 
                                axis=0,
                                ascending=False, 
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