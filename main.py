import csv

filename = "data.csv"

def create():
    try:
        with open(filename, 'x') as file:
            with open(filename, 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Exercise", "Reps", "Weight"])
    except FileExistsError:
        pass
        
if __name__ == "__main__":
    create()