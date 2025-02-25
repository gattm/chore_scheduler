import json
import time
import os
import random


# rankings = list of nested lists containing a name and day of the week preference rankings. Indices 1-6 represent Sun-Sat, and should contain a value 1-7, nonrepeating.
# Ex: [[Joe, 1, 3, 4, 2, 6, 5, 7]]
def scheduler(rankings):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    schedule = {day: [] for day in days}

    total_people = len(rankings)
    min_per_day = total_people // 7
    extra_slots = total_people % 7

# 1: Assign each person to their most preferred day
    for rank_set in rankings:
        name = rank_set[0]
        day_index = rank_set[1:].index("1")  # Find the most preferred day (1)
        day = days[day_index]
        schedule[day].append([name])

# 2: If the number of people assigned to a day exceeds the maximum allowed, randomly choose the appropriate amount.
    reassign = []
    for day in days:
        names = schedule[day]
        allowed_per_day = min_per_day + (1 if extra_slots > 0 else 0)
        if len(names) > allowed_per_day:
            random.shuffle(names)
            schedule[day] = names[:allowed_per_day]
            reassign.extend(names[allowed_per_day:])
            extra_slots = max(extra_slots - 1, 0)

    empty_days = [day for day in days if not schedule[day]]
    for day in empty_days:
        if reassign:
            schedule[day].append(reassign.pop(0))

    day_index = 0
    while reassign:
        day = days[day_index % 7]
        if len(schedule[day]) < min_per_day + 1:
            schedule[day].append(reassign.pop(0))
        day_index += 1

    for day in days:
        if not schedule[day]:
            schedule[day] = ["Free Day"]

    return schedule


# Reads and formats content from request.txt
def process_file():
    rankings = []
    with open("request.txt", "r") as infile:
        content = infile.read().strip()
        if not content:
            return  # Skip if file is empty
        for line in content.splitlines():
            rankings.append([num.strip() for num in line.split(",")])

    schedule = scheduler(rankings)
    file_output(schedule)
    open("request.txt", "w").close()


# Continously loops checking request.txt for modifications/requests
def file_monitor():
    last_modified = 0
    while True:
        if os.path.exists("request.txt"):
            current_modified = os.path.getmtime("request.txt")
            if current_modified != last_modified:  # File has been modified
                time.sleep(0.1)  # Brief delay to ensure writing is complete
                process_file()
                last_modified = current_modified
        time.sleep(0.5)  # Check every half second


# Writes completed schedule to response.txt
def file_output(schedule):
    schedule_str = json.dumps(schedule)
    with open("response.txt", "w") as file:
        file.write(schedule_str)

# Main
if __name__ == "__main__":
    open("request.txt", "w").close()  # Ensure file exists initially
    file_monitor()
