from greenvillechamber import GreenvilleChamber
from spartanburgarea import SpartanburgArea
from scra import SouthCarolinaResearchAuthority

# Instantiate classes
gc = GreenvilleChamber()
sa = SpartanburgArea()
scra = SouthCarolinaResearchAuthority()

# Scrape websites for events
gc.get_events()
sa.get_events()
scra.get_events()
