from greenvillechamber import GreenvilleChamber
from spartanburgarea import SpartanburgArea
from scra import SouthCarolinaResearchAuthority
from startgrowupstate import StartGrowUpstate
from eventsdb import EventsDB
import time

"Total Time Worked: 21hr50min"

# TODO: Add event data to wordpress

# For calculating run time
start_time = time.perf_counter()

events = []

# Scrape websites for events
gc = GreenvilleChamber()
print(f"Scraping Greenville Chambers...\nURL: {gc.url}")
try:
    gc.get_events()
    events += gc.events
except Exception as err:
    print(f"There was an error:\n{err}")

sa = SpartanburgArea()
print(f"\nScraping Spartanburg Area...\nURL: {sa.url}")
try:
    sa.get_events()
    events += sa.events
except Exception as err:
    print(f"There was an error:\n{err}")

scra = SouthCarolinaResearchAuthority()
print(f"\nScraping South Carolina Research Authority...\nURL: {scra.url}")
try:
    scra.get_events()
    events += scra.events
except Exception as err:
    print(f"There was an error:\n{err}")


sgu = StartGrowUpstate()
print(f"\nScraping Start Grow Upstate...\nURL: {sgu.url}")
try:
    sgu.get_events()
    events += sgu.events
except Exception as err:
    print(f"There was an error:\n{err}\n")

print(f"{len(events)} Events scraped")

edb = EventsDB(events)
edb.add_events()


end_time = time.perf_counter()
minutes = int((end_time - start_time) / 60)
seconds = round((end_time - start_time) % 60, 2)

print(f"\nTotal Run Time: {minutes}m {seconds}s")
