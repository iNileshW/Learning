import gazpacho
import json
import io

class EventCountError(Exception):
    """Raised if the excepted world record data is not complete/correct."""
    pass

URL = "https://en.wikipedia.org/wiki/List_of_world_records_in_swimming"

## RECORDS = (0, 2, 4, 5)   # The original table numbers from the printed book.
RECORDS = (0, 1, 3, 4)   # Update these values as required (these are valid as of Wednesday 28, 2026).
COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")

WHERE = "/home/nileshw2/webapp/"
## WHERE = ""
JSONDATA = "records.json"

html = gazpacho.get(URL)
soup = gazpacho.Soup(html)
tables = soup.find("table")
records = {}
for table, course in zip(RECORDS, COURSES):
    records[course] = {}
    for row in tables[table].find("tr")[1:]:
        columns = row.find("td")
        event = columns[0].text
        time = columns[1].text
        if "relay" not in event:
            records[course][event] = time
            
# Check to make sure there's all the expected data in the records dictionary.
for course in COURSES:
    if not records[course]:
        raise EventCountError("Please check the values in the RECORDS tuple (data missing).")
                    
with open(WHERE + JSONDATA, "w") as jf:
    json.dump(records, jf)