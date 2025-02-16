import argparse
import urllib.request
import logging
import datetime
import csv

def downloadData(url):
    """Downloads the data from a url and returns it as a string."""

    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

def processData(csv_content):
    """Takes .CSV file and returns a dictionary. Mapped IDs to (name, birthday)."""

    personData = {}  # Dictionary to store data
    logger = logging.getLogger('assignment2')  # Get logger for error logging. Part V.3 here.

    lines = csv_content.strip().split("\n")  # Split content into lines
    reader = csv.reader(lines)  # Reads the .csv data
    next(reader, None)  # Skips the header row.

    for line_number, row in enumerate(reader, start=2):  # Starts the count from row 2 since the first row is text.
        try:
            person_id = int(row[0])  # First column: ID (couldn't use 'id'. it's a function.)
            name = row[1]  # Second column: Name
            birthday = datetime.datetime.strptime(row[2], "%d/%m/%Y").date()  # Third column: Birthday (converted)

            personData[person_id] = (name, birthday)  # Stores the data
        except (ValueError, IndexError):
            logger.error(f"Error processing line #{line_number} for ID #{row[0] if row else 'UNKNOWN'}")

    return personData

def displayPerson(person_id, personData):
    """Displays the name and birthday of the given person ID."""

    if person_id in personData:
        name, birthday = personData[person_id]
        print(f"Person #{person_id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that ID")

def main(url):
    """Main function to retrieve data and for user interaction."""

    #Setup logging to write errors to 'errors.log'
    logging.basicConfig(filename="errors.log", level=logging.ERROR)

    try:
        csvData = downloadData(url)  #Fetch data
    except Exception as e:
        print(f"Failed to retrieve data: {e}")
        exit(1)

    personData = processData(csvData)  #Process data into dictionary

    #Mobius loop
    while True:
        try:
            person_id = int(input("Enter an ID to lookup (0 or negative to exit): "))
            if person_id <= 0:
                break  #Exit loop
            displayPerson(person_id, personData)
        except ValueError:
            print("Invalid input. Please enter a valid numeric ID.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)