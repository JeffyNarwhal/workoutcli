import os, cmd, datetime
import pandas as pd
import shlex
import tkinter as tk
from tkinter import filedialog

pd.set_option('display.max_rows', 900)

class FileManagerCLI(cmd.Cmd):
    prompt = "WorkoutCli/data>> "
    intro = 'Welcome to WorkoutCLI. Type "help" for available commands.'
    filename = "./csv/data.csv"

    def __init__(self):
        super().__init__()
        self.current_directory = os.path.dirname(os.path.realpath(__file__)) # Sets directory to file directory so creating the csv works
        if not os.path.exists(self.filename):
            try:
                # Create an empty DataFrame with the desired columns
                df = pd.DataFrame(columns=["Exercise", "Reps", "Weight", "Date"])
                # Save to CSV without index
                df.to_csv(self.filename, index=False)
                print(f"Created new CSV file: {self.filename}")
            except Exception as e:
                print(f"Error creating CSV file: {e}")

    def do_add(self, line):
        """Adds a workout
        Format: add "Exercise Name" Reps Weight [Date (YYYY-MM-DD)]
        Example: add "Bench Press" 8 135 2025-05-19
                 add "Squat" 5 225 (uses today's date)"""
        try:
            args = shlex.split(line)
            if len(args) < 3 or len(args) > 4:
                print("Error: Expected format: add \"Exercise Name\" Reps Weight [Date]")
                return
            exercise = args[0]
            try:
                reps = int(args[1])
                weight = float(args[2])
            except ValueError:
                print("Error: Reps and Weight must be numbers.")
                return
            if len(args) == 4:
                try:
                    date = pd.to_datetime(args[3]).date()
                except ValueError:
                    print("Error: Invalid date format. Use YYYY-MM-DD.")
                    return
            else:
                date = datetime.date.today()
            new_row = pd.DataFrame({
                'Exercise': [exercise],
                'Reps': [reps],
                'Weight': [weight],
                'Date': [date]
            })
            if os.path.exists(self.filename):
                df = pd.read_csv(self.filename)
                if df.empty:
                    # If the CSV is empty (only headers), use new_row directly
                    df = new_row
                else:
                    # Concatenate if the CSV has data
                    df = pd.concat([df, new_row], ignore_index=True)
            else:
                # If file doesn't exist, use new_row (shouldn't happen due to __init__)
                df = new_row
            df.to_csv(self.filename, index=False)
            print(f"Added: {exercise}, {reps} reps, {weight} lbs, {date}")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def do_view(self, line):
        """View workouts with optional filters
        Format: view [Column:Value] [Column:Value] ...
        Example: view Exercise:"Bench Press"
                 view Exercise:"Bench Press" Reps:8
                 view (shows all workouts)"""
        try:
            if not os.path.exists(self.filename):
                print(f"Error: File '{self.filename}' not found.")
                return
            df = pd.read_csv(self.filename)
            if not line.strip():
                # No filters: mimic print(pd.read_csv(self.filename))
                print(df)
                return
            # Apply filters
            try:
                args = shlex.split(line)
            except ValueError:
                print("Error: Invalid input format. Use quotes for multi-word values (e.g., Exercise:\"Bench Press\").")
                return
            filters = {}
            for arg in args:
                if ':' not in arg:
                    print(f"Error: Invalid filter format in '{arg}'. Use Column:Value.")
                    return
                column, value = arg.split(':', 1)
                if column not in df.columns:
                    print(f"Error: Column '{column}' not found in CSV.")
                    return
                filters[column] = value
            filtered_df = df.copy()
            for column, value in filters.items():
                if column in ['Reps', 'Weight']:
                    try:
                        value = float(value)
                        filtered_df = filtered_df[filtered_df[column] == value]
                    except ValueError:
                        print(f"Error: Value '{value}' for '{column}' must be a number.")
                        return
                elif column == 'Date':
                    try:
                        value = pd.to_datetime(value).date()
                        filtered_df = filtered_df[filtered_df[column] == str(value)]
                    except ValueError:
                        print(f"Error: Invalid date format for '{column}'. Use YYYY-MM-DD.")
                        return
                else:
                    filtered_df = filtered_df[filtered_df[column] == value]
            if filtered_df.empty:
                print("No workouts match the specified filters.")
            else:
                # Reset index to start from 0 for filtered results
                filtered_df = filtered_df.reset_index(drop=True)
                print(filtered_df)
        except Exception as e:
            print(f"Error: {e}")
    
    def do_sort(self, line):
        """Sorts"""
        try:
            csvData = pd.read_csv(self.filename)
            csvData.sort_values(line, 
                                axis=0,
                                ascending=False, 
                                inplace=True)
            csvData.to_csv(self.filename, index=0)
        except Exception as e:
            print(f"Error: {e}")

    def do_clear(self, line):
        """Clear the terminal screen."""
        os.system('cls')

    def do_merge(self, line):
        """Merges CSV file"""
        try:
            pd.concat([pd.read_csv(self.filename), pd.read_csv(line)]).to_csv(self.filename, index=0)
        except Exception as e:
            print(f"Error: {e}")

    def do_export(self, line):
        """Export CSV file"""
        try:
            csvData = pd.read_csv(self.filename)
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            file_path = filedialog.asksaveasself.filename(defaultextension="csv")
            csvData.to_csv(file_path, index=0)
        except Exception as e:
            print(f"Error: {e}")
    
    def do_files(self, line):
        """List csv files"""
        try:
            items = os.listdir("csv/")
            for item in items:
                print(item[0:-4])
        except Exception as e:
            print(f"Error: {e}")

    def do_open(self, line):
        """Opens a select csv file"""
        try:
            items = os.listdir("csv/")
            for item in items:
                if (item[0:-4] == line):
                    self.filename = "./csv/" + line + ".csv"
                    self.prompt = "WorkoutCli/" + line + ">> "
                    break
        except Exception as e:
            print(f"Error: {e}")

    def do_quit(self, line):
        """Exit the CLI."""
        return True

if __name__ == '__main__':
    FileManagerCLI().cmdloop()