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

"Total Time Worked: 42hr00min"

# Info for sending E-Mail
sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
password = os.environ.get("SENDER_PASSWORD")

# For calculating run time
start_time = time.perf_counter()

# Time Stamp of when code was ran
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
    # Send E-mail in case of error
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
    # Send E-mail in case of error
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
    # Send E-mail in case of error
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
    # Send E-mail in case of error
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
edb = EventsDB(events, 'events')
try:
    edb.add_events()
except Exception as err:
    errors.append(err)
    print(f"There was an error uploading events to database:\n{err}")
    # Send E-mail in case of error
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        msg = f"Subject: ERROR ADDING EVENT TO DATABASE\n\nError Message:\n{err}"
        connection.starttls()
        connection.login(user=sender_email, password=password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=msg
        )

print("Posting events to WordPress")
wp = CEIWordPress()
try:
    wp.post_events()
except Exception as err:
    errors.append(err)
    print(f"There was an error posting events to wordpress:\n{err}")
    # Send E-mail in case of error
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        msg = f"Subject: ERROR POSTING EVENT TO WORDPRESS\n\nError Message:\n{err}"
        connection.starttls()
        connection.login(user=sender_email, password=password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=msg
        )
        

# Calculaute run time
end_time = time.perf_counter()
minutes = int((end_time - start_time) / 60)
seconds = round((end_time - start_time) % 60, 2)

print(f"\nTotal Run Time: {minutes}m {seconds}s")

# Send final email with status reports
with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
    msg = f"Subject: WEBSCRAPER STATUS REPORT\n\n"

    # Include the date and time the code ran
    msg += f"WebScraper ran on {runtime.date().strftime('%B %d, %Y')} @ {runtime.hour}:{runtime.minute}\n\n"
    # TODO: Include Number events scraped and number of events posted in final

    msg += f"{len(events)} Total events scraped.\n"
    msg += f"{edb.new_events} New events were added to the database.\n\n"



    # Include errors that were presented (if any)
    if len(errors) != 0:
        msg += "The following errors were found:\n\n"
        for error in errors:
            msg += f"{error}\n\n"
    else:
        msg += "No errors were found.\n\n"

    if len(wp.events_posted) != 0:
        msg += "The Following events were posted to the database:\n\n"
        for item in wp.events_posted:
            for key in item.keys():
                msg += f"{key}: {item[key]}\n"

            msg += "\n"

        msg += "\n"

    # Include the events that may possibly not have been posted (if any)
    if len(wp.events_not_posted) != 0:
        msg += "The following events may not have been posted:\n\n"
        for item in wp.events_not_posted:
            for key in item.keys():
                msg += f"{key}: {item[key]}\n"

            msg += "\n"

    elif len(wp.events_posted) != 0:
        msg += "It appears all events were successfully uploaded.\n\n\n"

    msg += f"\n\nTotal Run Time: {minutes}m {seconds}s"

    connection.starttls()
    connection.login(user=sender_email, password=password)
    connection.sendmail(
        from_addr=sender_email,
        to_addrs=receiver_email,
        msg=msg
    )



