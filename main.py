from greenvillechamber import GreenvilleChamber
from spartanburgarea import SpartanburgArea
from scra import SouthCarolinaResearchAuthority
import pprint

# Instantiate classes
gc = GreenvilleChamber()
sa = SpartanburgArea()
scra = SouthCarolinaResearchAuthority()

# Scrape websites for events
print("Scraping Greenville Chambers...")
try:
    gc.get_events()
except Exception as err:
    print(f"There was an error:\n{err}")

print("\nScraping Spartanburg Area...")
try:
    sa.get_events()
except Exception as err:
    print(f"There was an error:\n{err}")

print("\nScraping South Carolina Research Authority...")
try:
    scra.get_events()
except Exception as err:
    print(f"There was an error:\n{err}")


events = gc.events
events.append(sa.events)
events.append(scra.events)