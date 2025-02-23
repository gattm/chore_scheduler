# Chore Scheduler Microservice
This microservice generates a weekly schedule based on user-provided day-of-the-week preference rankings. It uses text files as a communication pipe: request.txt for input and response.txt for output. This README defines the communication contract for interacting with the microservice programmatically.

## Communication Contract
### Overview
Input File: request.txt - Where clients write their ranking data.
Output File: response.txt - Where the microservice writes the generated schedule.
Format: Rankings are provided as comma-separated values (CSV) in request.txt, and the schedule is returned as JSON in response.txt.
Behavior: The microservice monitors request.txt for changes, processes the rankings, writes the schedule to response.txt, and clears request.txt when done.
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
