from greenvillechamber import GreenvilleChamber
from spartanburgarea import SpartanburgArea
from scra import SouthCarolinaResearchAuthority
from startgrowupstate import StartGrowUpstate
from eventsdb import EventsDB
from ceiwordpress import CEIWordPress
import time

"Total Time Worked: 32hr40min"

# TODO: Debug SCRA and CEIWordPress

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
    print(f"There was an error scraping {gc.name}:\n{err}")
    gc.driver.quit()

sa = SpartanburgArea()
print(f"\nScraping Spartanburg Area...\nURL: {sa.url}")
try:
    sa.get_events()
    events += sa.events
except Exception as err:
    print(f"There was an error scraping {sa.name}:\n{err}")
    sa.driver.quit()

scra = SouthCarolinaResearchAuthority()
print(f"\nScraping South Carolina Research Authority...\nURL: {scra.url}")
try:
    scra.get_events()
    events += scra.events
except Exception as err:
    print(f"There was an error scraping {scra.name}:\n{err}")
    scra.driver.quit()


sgu = StartGrowUpstate()
print(f"\nScraping Start Grow Upstate...\nURL: {sgu.url}")
try:
    sgu.get_events()
    events += sgu.events
except Exception as err:
    print(f"There was an error scraping {sgu.name}:\n{err}")
    sgu.driver.quit()

print(f"{len(events)} Events scraped")

print("Adding events to the database")
try:
    edb = EventsDB(events)
    edb.add_events()
except Exception as err:
    print(f"There was an error uploading events to database:\n{err}")


end_time = time.perf_counter()
minutes = int((end_time - start_time) / 60)
seconds = round((end_time - start_time) % 60, 2)

print("Posting events to WordPress")
try:
    wp = CEIWordPress()
    wp.post_events()
except Exception as err:
    print(f"There was an error posting events to wordpress:\n{err}")

print(f"\nTotal Run Time: {minutes}m {seconds}s")
