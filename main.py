import time
import smtplib, ssl
from ceiwordpress import CEIWordPress
from eventsdb import EventsDB
from greenvillechamber import GreenvilleChamber
from scra import SouthCarolinaResearchAuthority
from spartanburgarea import SpartanburgArea
from startgrowupstate import StartGrowUpstate
from dotenv import load_dotenv
import os

load_dotenv()

"Total Time Worked: 36hr30min"

# TODO: Automate script: https://towardsdatascience.com/how-to-easily-automate-your-python-scripts-on-mac-and-windows-459388c9cc94


# For E-Mail

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
password = os.environ.get("SENDER_PASSWORD")
context = ssl.create_default_context()

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
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        message = f"Subject: ERROR SCRAPING {gc.name.upper()}\n\nError Message:\n{err}"
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    gc.driver.quit()

sa = SpartanburgArea()
print(f"\nScraping Spartanburg Area...\nURL: {sa.url}")
try:
    sa.get_events()
    events += sa.events
except Exception as err:
    print(f"There was an error scraping {sa.name}:\n{err}")
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        message = f"Subject: ERROR SCRAPING {sa.name.upper()}\n\nError Message:\n{err}"
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    sa.driver.quit()

scra = SouthCarolinaResearchAuthority()
print(f"\nScraping South Carolina Research Authority...\nURL: {scra.url}")
try:
    scra.get_events()
    events += scra.events
except Exception as err:
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        message = f"Subject: ERROR SCRAPING {scra.name.upper()}\n\nError Message:\n{err}"
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    print(f"There was an error scraping {scra.name}:\n{err}")
    scra.driver.quit()


sgu = StartGrowUpstate()
print(f"\nScraping Start Grow Upstate...\nURL: {sgu.url}")
try:
    sgu.get_events()
    events += sgu.events
except Exception as err:
    print(f"There was an error scraping {sgu.name}:\n{err}")
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        message = f"Subject: ERROR SCRAPING {sgu.name.upper()}\n\nError Message:\n{err}"
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    sgu.driver.quit()

print(f"{len(events)} Events scraped")

print("Adding events to the database")
try:
    edb = EventsDB(events)
    edb.add_events()
except Exception as err:
    print(f"There was an error uploading events to database:\n{err}")
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        message = f"Subject: ERROR SCRAPING ADDING EVENT TO DATABASE\n\nError Message:\n{err}"
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


end_time = time.perf_counter()
minutes = int((end_time - start_time) / 60)
seconds = round((end_time - start_time) % 60, 2)

print("Posting events to WordPress")
try:
    wp = CEIWordPress()
    wp.post_events()
except Exception as err:
    print(f"There was an error posting events to wordpress:\n{err}")
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        message = f"Subject: ERROR POSTING EVENT TO WORDPRESS\n\nError Message:\n{err}"
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

print(f"\nTotal Run Time: {minutes}m {seconds}s")
