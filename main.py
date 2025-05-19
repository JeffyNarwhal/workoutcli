import csv, os, cmd, datetime
from rich.console import Console
from rich.table import Table
import pandas as pandasForSortingCSV

filename = "data.csv"
console = Console()

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
        """Adds a workout\nFormat: Exercise (If its named like "Bench Press", seperate with a -) Reps Weight Date (YYYY-MM-DD)"""
        line = line.split(" ")
        line[0] = line[0].replace("-", " ")
        try:
            line[3]
        except:
            line.append(datetime.date.today())
        try:
            with open (filename, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([line[0], line[1], line[2], line[3]])
                print(f"Added {line[0], line[1], line[2], line[3]}")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error: {e}")
    
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

    def do_workouts(self, line):
        """Prints workouts"""
        print(pandasForSortingCSV.read_csv("data.csv"))
    
    def do_sort(sort, line):
        """Sorts"""
        try:
            csvData = pandasForSortingCSV.read_csv("data.csv")
            csvData.sort_values(["Exercise"], 
                                axis=0,
                                ascending=[True], 
                                inplace=True)
            csvData.to_csv(filename, index=0)
        except Exception as e:
            print(f"Error: {e}")
    
    def do_prs(self, line):
        """Lists 1 rep prs of the exercise, starting with the highest. Inludes date"""

    def do_quit(self, line):
        """Exit the CLI."""
        return True

if __name__ == '__main__':
    FileManagerCLI().cmdloop()