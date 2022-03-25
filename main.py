#!/Users/manny/Documents/Freelancing/USCUCEI/venv/bin/python3
import datetime
import time
import smtplib
from ceiwordpress import CEIWordPress
from eventsdb import EventsDB
from greenvillechamber import GreenvilleChamber
from scra import SouthCarolinaResearchAuthority
from spartanburgarea import SpartanburgArea
from startgrowupstate import StartGrowUpstate
from dotenv import load_dotenv
import os

load_dotenv()

"Total Time Worked: 40hr00min"

# For E-Mail
sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
password = os.environ.get("SENDER_PASSWORD")

# For calculating run time
start_time = time.perf_counter()
runtime = datetime.datetime.now()

events = []
errors = []
# Scrape websites for events
gc = GreenvilleChamber()
print(f"Scraping Greenville Chambers...\nURL: {gc.url}")
try:
    gc.get_events()
    events += gc.events
except Exception as err:
    errors.append(err)
    print(f"There was an error scraping {gc.name}:\n{err}")
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        msg = f"Subject: ERROR SCRAPING {gc.name.upper()}\n\nError Message:\n{err}"
        connection.starttls()
        connection.login(user=sender_email, password=password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=msg
        )
    gc.driver.quit()

sa = SpartanburgArea()
print(f"\nScraping Spartanburg Area...\nURL: {sa.url}")
try:
    sa.get_events()
    events += sa.events
except Exception as err:
    errors.append(err)
    print(f"There was an error scraping {sa.name}:\n{err}")
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        msg = f"Subject: ERROR SCRAPING {sa.name.upper()}\n\nError Message:\n{err}"
        connection.starttls()
        connection.login(user=sender_email, password=password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=msg
        )
    sa.driver.quit()

scra = SouthCarolinaResearchAuthority()
print(f"\nScraping South Carolina Research Authority...\nURL: {scra.url}")
try:
    scra.get_events()
    events += scra.events
except Exception as err:
    errors.append(err)
    print(f"There was an error scraping {scra.name}:\n{err}")
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        msg = f"Subject: ERROR SCRAPING {scra.name.upper()}\n\nError Message:\n{err}"
        connection.starttls()
        connection.login(user=sender_email, password=password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=msg
        )
    scra.driver.quit()

sgu = StartGrowUpstate()
print(f"\nScraping Start Grow Upstate...\nURL: {sgu.url}")
try:
    sgu.get_events()
    events += sgu.events
except Exception as err:
    errors.append(err)
    print(f"There was an error scraping {sgu.name}:\n{err}")
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        msg = f"Subject: ERROR SCRAPING {sgu.name.upper()}\n\nError Message:\n{err}"
        connection.starttls()
        connection.login(user=sender_email, password=password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=msg
        )
    sgu.driver.quit()

print(f"{len(events)} Events scraped")

print("Adding events to the database")
try:
    edb = EventsDB(events)
    edb.add_events()
except Exception as err:
    errors.append(err)
    print(f"There was an error uploading events to database:\n{err}")
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        msg = f"Subject: ERROR ADDING EVENT TO DATABASE\n\nError Message:\n{err}"
        connection.starttls()
        connection.login(user=sender_email, password=password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=msg
        )


end_time = time.perf_counter()
minutes = int((end_time - start_time) / 60)
seconds = round((end_time - start_time) % 60, 2)

print("Posting events to WordPress")
wp = CEIWordPress()
try:
    wp.post_events()
except Exception as err:
    errors.append(err)
    print(f"There was an error posting events to wordpress:\n{err}")
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        msg = f"Subject: ERROR POSTING EVENT TO WORDPRESS\n\nError Message:\n{err}"
        connection.starttls()
        connection.login(user=sender_email, password=password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=msg
        )

print(f"\nTotal Run Time: {minutes}m {seconds}s")

with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
    msg = f"Subject: WEBSCRAPER STATUS\n\nWebScraper ran on {runtime.date()} {runtime.hour}:{runtime.minute}\n"
    if len(errors) != 0:
        msg += "\n\nThe following errors were found:"
        for error in errors:
            msg += f"\n\n{error}"
    else:
        msg += "\n\nNo errors were found."

    if len(wp.events_not_posted) != 0:
        msg += "\n\nThe following events may not have been posted:\n"
        for event in wp.events_not_posted:
            msg += f"{event["title"]} on {event["date"]} @ {event["time"]}\n"
    else:
        msg += "\n\nIt appears all events were successfully uploaded."

    msg += f"\n\nTotal Run Time: {minutes}m {seconds}s"

    connection.starttls()
    connection.login(user=sender_email, password=password)
    connection.sendmail(
        from_addr=sender_email,
        to_addrs=receiver_email,
        msg=msg
    )



