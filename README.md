# Chore Scheduler Microservice
This microservice generates a weekly schedule based on user-provided day-of-the-week preference rankings. It uses text files as a communication pipe: request.txt for input and response.txt for output. This README defines the communication contract for interacting with the microservice programmatically.
~~                                                                                                                                                                                    ~~
## Communication Contract
### Overview
**Input File**: request.txt - Where clients write their ranking data.

**Output File**: response.txt - Where the microservice writes the generated schedule.

**Format**: Rankings are provided as comma-separated values (CSV) in request.txt, and the schedule is returned as JSON in response.txt.

**Behavior**: The microservice monitors request.txt for changes, processes the rankings, writes the schedule to response.txt, and clears request.txt when done.

### How to Programmatically REQUEST Data
### Instructions

**Prepare Your Rankings:**
Each line in request.txt represents one person's preferences.

**Format**: name,preference_sun,preference_mon,preference_tue,preference_wed,preference_thu,preference_fri,preference_sat
name is a string (no commas allowed).

preference_* is an integer from 1 (most preferred) to 7 (least preferred), with no duplicates per person.

**Example**: Joe,1,2,3,4,5,6,7 means Joe prefers Sunday (1) most and Saturday (7) least.

### Write to request.txt:
Open request.txt in write mode ("w") and write all rankings as lines of comma-separated values.

Ensure the file is fully written before closing it (use proper file handling to avoid partial writes).

The microservice will detect the file change and process it.

### Timing:
After writing, wait briefly (e.g., 0.5 seconds) to allow the microservice to process the request.

## Example Request
```
import time

# Define rankings
rankings = [
    "Joe,1,2,3,4,5,6,7",
    "Matt,2,1,3,4,5,6,7"
]

# Write rankings to request.txt
with open("request.txt", "w") as file:
    file.write("\n".join(rankings))

# Wait for the microservice to process
time.sleep(0.5)
```

### How to Programmatically RECEIVE Data
### Instructions

**Wait for response.txt:**

After writing to request.txt, monitor for the existence of response.txt.

The microservice writes the schedule to response.txt and clears request.txt when processing is complete.

**Read response.txt:**

Open response.txt in read mode ("r") and parse the JSON content.

The JSON object is a dictionary where keys are day names (Sunday, Monday, etc.), and values are lists of assigned names or ["Free Day"] if no one is assigned.

**Handle Timing:**

Poll response.txt until it exists (e.g., with a small delay like 0.1 seconds between checks).

Once read, the schedule is ready for use.

### Example Call (Python)
```
import json
import os
import time

# Wait for response.txt to be generated
while not os.path.exists("response.txt"):
    time.sleep(0.1)

# Read and parse the schedule
with open("response.txt", "r") as file:
    schedule = json.load(file)

# Example usage: print the schedule
for day, people in schedule.items():
    print(f"{day}: {people}")
```

### Expected Output
For the example request above (Joe and Matt), the output in response.txt might look like:

**json**
```
{
    "Sunday": [["Joe"]],
    "Monday": [["Matt"]],
    "Tuesday": ["Free Day"],
    "Wednesday": ["Free Day"],
    "Thursday": ["Free Day"],
    "Friday": ["Free Day"],
    "Saturday": ["Free Day"]
}
```
### Notes
- Error Handling: Ensure your code handles cases where request.txt or response.txt might be temporarily locked or unavailable due to file I/O.

- Running the Microservice: The teammate must ensure scheduler.py is running in the background before making requests.

- File Location: Both request.txt and response.txt should be in the same directory as the microservice script.
