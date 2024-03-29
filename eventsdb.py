import sqlite3
from sqlite3 import Error


class EventsDB:
    """This class is in charged of uploading the events to a database."""

    def __init__(self, events, table_name):
        self.db_name = '/Users/manny/Documents/Freelancing/USCUCEI/events.db'
        self.table_name = table_name
        self.events = events
        self.table_header = "(Title VARCHAR(100), Date VARCHAR(100), Time VARCHAR(100), Link VARCHAR(100), " \
                            "Description VARCHAR(2000), Posted BOOL, id INT NOT NULL, PRIMARY KEY (id)) "
        self.connection = None
        self.cursor = None
        self.new_events = 0

    def connect(self):
        """This method establishes a connection with a database"""

        try:
            self.connection = sqlite3.connect(self.db_name)
        except Error as err:
            print(f"There was an error connecting:\n{err}")

    def create_cursor(self):
        """This method creates a cursor for the database"""

        # Make sure a connection is already established
        if self.connection is None:
            self.connect()
        try:
            self.cursor = self.connection.cursor()
        except Error as err:
            print(f"There was an error creating cursor:\n{err}")

    def create_table(self):
        """This method is in charged of creating a table within the database"""

        if self.cursor is None:
            self.create_cursor()

        try:
            self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}
                                {self.table_header}''')
            self.connection.commit()
        except Error as err:
            print(f"There was an error creating table: {err}")

    def add_events(self):
        """This is the main method in charged of adding events to the database."""
        if self.cursor is None:
            self.create_table()

        # Start looping through events and creating the right syntax
        for item in self.events:
            new_event = "("

            # Go through of the keys in an event
            for key in item.keys():

                event = str(item[key])
                # Replace special keys
                event = event.replace("'", "&&&")
                event = event.replace("\n", "&&n")

                # Surround entry in single quotes
                new_event += "'"
                new_event += event
                new_event += "'"

                # Add commas for all entries except for the last one
                if key != list(item.keys())[-1]:
                    new_event += ", "

            # Loop through events in the database and check to see whether or not the event has already been uploaded
            repeated_event = False
            self.cursor.execute(f"SELECT Title, Date, Time, Link, Description FROM {self.table_name}")
            records = self.cursor.fetchall()
            if records:
                data_id = len(records) + 2  # I deleted two events
                for record in records:
                    # Only compare event details (L79) not the id or whether or not it has been posted posted
                    if str(record) == new_event + ")":
                        repeated_event = True
                        print("There is a repeated event")
            else:
                data_id = 0

            # If it is not a repeated event, then upload to database
            if not repeated_event:
                try:
                    # This Posted column indicated whether or not event has already been posted to WordPress
                    new_event += f", '0', '{data_id}')"
                    self.cursor.execute(f"INSERT INTO {self.table_name} VALUES {new_event}")
                    self.connection.commit()
                    self.new_events += 1

                except Error as err:
                    print(f"There was an error adding event: {err}")

        # Print how many events were added
        if self.new_events == 0:
            print("No new events were added to database...")
        else:
            print(f"{self.new_events} Total events added to database")

        self.end_connection()

    def end_connection(self):
        """This method is in charged of closing the connection to the database."""

        if self.connection is None:
            pass
        else:
            self.connection.close()
            print("Connection Closed")


if __name__ == "__main__":
    events = [{'Title': 'Ribbon Cutting: Upstate Hearing and Balance', 'Date': 'February 22, 2022',
               'Time': '4:00 pm - 4:30 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/02/22/business-celebration/ribbon-cutting-upstate-hearing-and-balance/',
               'Description': 'Join us to celebrate the opening of Upstate Hearing and Balance.\nSocial distancing and masks are encouraged.'},
              {'Title': 'Ribbon Cutting: Double Dogs', 'Date': 'February 23, 2022', 'Time': '10:30 am - 11:00 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/02/23/business-celebration/ribbon-cutting-double-dogs/',
               'Description': 'Join us to celebrate the newly opened Double Dogs restaurant!'},
              {'Title': 'Links Group #2', 'Date': 'February 23, 2022', 'Time': '11:30 am - 1:00 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/02/23/business-growth/links-group-2/',
               'Description': 'This non-compete leads group offers business networking and referral marketing.\nTo learn more about joining this group contact Andrew Van.'},
              {'Title': 'Ribbon Cutting: Overture Apartments', 'Date': 'February 24, 2022', 'Time': '4:00 pm - 4:30 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/02/24/business-celebration/ribbon-cutting-overture-apartments/',
               'Description': 'Join us to celebrate the opening of the Overture Apartments!\nSocial distancing and masks are encouraged.'},
              {'Title': 'Women in Advocacy – Inaugural Event', 'Date': 'February 25, 2022', 'Time': '8:00 am - 9:30 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/02/25/business-advocacy/women-in-advocacy-inaugural-event/',
               'Description': 'Presented by Greenville Federal Credit Union\nThe women in advocacy program is designed to connect women in all sectors of the advocacy community – from those who are in the trenches to those who want to be better informed to help their businesses and community. These events bring our members up close and personal with elected officials, government affairs professionals, lobbyists and more.\n  Featuring Barbara Melvin, COO, South Carolina Ports\nThe Greenville Chamber is taking every safety precaution recommended by the CDC and state and local officials for our event, including limiting capacity and implementing social distancing during this event. Attendees are encouraged to wear masks – whether you are vaccinated or not. We will continue to follow the latest CDC, state and local guidelines and will communicate any changes to our plan. If you feel sick, stay home! You will be refunded or credited 100% of registration fees paid if you are ill due to COVID-19.'},
              {'Title': 'Ribbon Cutting: Harness Health Partners', 'Date': 'March 2, 2022',
               'Time': '11:30 am - 12:00 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/02/business-celebration/ribbon-cutting-harness-health-partners/',
               'Description': "Join us for an exclusive ribbon cutting for the opening of Harness Health Partner's new location!\nMasks and social distancing are encouraged."},
              {'Title': 'Links Group #1', 'Date': 'March 3, 2022', 'Time': '8:45 am - 10:00 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/03/business-growth/links-group-1/',
               'Description': 'This non-compete leads group offers business networking and referral marketing.\nTo learn more about joining this group contact Andrew Van.'},
              {'Title': 'Business After Hours', 'Date': 'March 3, 2022', 'Time': '5:30 pm - 7:30 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/03/business-growth/business-after-hours/',
               'Description': 'Mix and mingle with Chamber Investors at one of our premier networking events. Professionals utilize this opportunity to discuss and share ideas in a relaxed, social atmosphere while learning about other Investor businesses.\nThe Greenville Chamber is taking every safety precaution recommended by the CDC and state and local officials for our event, including limiting capacity and implementing social distancing during this event. Attendees are encouraged to wear masks – whether you are vaccinated or not. We will continue to follow the latest CDC, state and local guidelines and will communicate any changes to our plan. If you feel sick, stay home! You will be refunded or credited 100% of registration fees paid if you are ill due to COVID-19.'},
              {'Title': 'Ribbon Cutting: Mosquito Shield', 'Date': 'March 8, 2022', 'Time': '12:00 pm - 12:30 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/08/business-celebration/ribbon-cutting-mosquito-shield/',
               'Description': "Join us for the launch of Mosquito Shield's new mobile unit at the Commons!\nMasks and social distancing are encouraged."},
              {'Title': 'Greenville Chamber Young Professionals Connect Events (for 2022 GCYP Members Only)',
               'Date': 'March 9, 2022', 'Time': '5:00 pm - 7:00 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/09/leadership-development/greenville-chamber-young-professionals-connect-events-for-2022-gcyp-members-only/',
               'Description': 'The Greenville Chamber is taking every safety precaution recommended by the CDC and state and local officials for our event, including limiting capacity and implementing social distancing during this event.  Attendees are encouraged to wear masks – whether you are vaccinated or not. We will continue to follow the latest CDC, state and local guidelines and will communicate any changes to our plan. If you feel sick, stay home!  You will be refunded or credited 100% of registration fees paid if you are ill due to COVID-19.'},
              {'Title': 'Links Industrial', 'Date': 'March 10, 2022', 'Time': '8:30 am - 9:45 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/10/business-growth/links-industrial/',
               'Description': 'This non-compete leads group offers business networking and referral marketing in industrial industries.\nTo learn more about joining this group contact Andrew Van.'},
              {'Title': 'Ribbon Cutting: Pointe Grand Apartments', 'Date': 'March 10, 2022',
               'Time': '4:00 pm - 4:30 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/10/business-celebration/ribbon-cutting-pointe-grand-apartments/',
               'Description': 'Join us to celebrate the opening of the Pointe Grand Apartments in Simpsonville!\nSocial distancing and masks are encouraged.'},
              {'Title': '2022 Human Resources Law Update', 'Date': 'March 11, 2022', 'Time': '8:00 am - 3:00 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/11/economic-competitiveness/2022-human-resources-law-update/',
               'Description': "More than 200 Upstate South Carolina human resources professionals are expected to attend (virtual and in-person) the 2022 Human Resources Law Update.  \nRegistration fee is $309 per person. Advance payment is required.\nFor agenda, speaker bios and other information, go to www.hrlugreenville.com. \nThis annual Update is regarded as the premier educational and networking event for human resources managers, generalists, and assistants. The concentrated agenda also appeals to office managers, plant managers, and other business executives who wish to gain current information in a short amount of time.\nSince the Update's beginning  27 years ago, the Ogletree Deakins Law Firm has helped organize the update. This year's Update faculty includes attorneys who will present timely information on HR topics.  In addition, many suppliers of human resources services will be on hand with displays full of information and ideas.\nThe Update is an annual partnership event planned and hosted by the Employers Network and the Greenville Chamber.  \nPAYMENT/CANCELLATION POLICIES\nAll registrations must be paid no later than the event date (March 11 2022). \nYou are responsible for submitting payment by the payment deadline (if paying by check). Failure to do so may result in cancellation of your reservation.\nPlease note:\n• Registration fee is $309 per person\n• Cancellations made on or before Feb 11 will receive a full refund.\n• Cancellations made after Feb 11 and on or before Feb 18 will receive a refund minus a $95 cancellation fee\n• No refunds will be issued after Feb 18. No refunds or credits will be given for “no-shows” at the Update\n• If you cannot attend and wish to send a substitute, please call 864-585-1007 with the substitute's name\n• Reservations by phone that are not paid by Feb 25 may be cancelled \nThe Greenville Chamber is taking every safety precaution recommended by the CDC and state and local officials for our event, including limiting capacity and implementing social distancing during this event.  Attendees are encouraged to wear masks – whether you are vaccinated or not. We will continue to follow the latest CDC, state and local guidelines and will communicate any changes to our plan. If you feel sick, stay home!  You will be refunded or credited 100% of registration fees paid if you are ill due to COVID-19."},
              {'Title': 'Business Advocacy Committee', 'Date': 'March 11, 2022', 'Time': '8:30 am - 9:30 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/11/business-advocacy/business-advocacy-committee/',
               'Description': 'The Greenville Chamber is taking every safety precaution recommended by the CDC and state and local officials for our event, including limiting capacity and implementing social distancing during this event.  Attendees are encouraged to wear masks – whether you are vaccinated or not. We will continue to follow the latest CDC, state and local guidelines and will communicate any changes to our plan. If you feel sick, stay home!  You will be refunded or credited 100% of registration fees paid if you are ill due to COVID-19.'},
              {'Title': 'Links Group #3', 'Date': 'March 15, 2022', 'Time': '8:30 am - 10:00 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/15/business-growth/links-group-3/',
               'Description': 'This non-compete leads group offers business networking and referral marketing.\nTo learn more about joining this group contact Andrew Van.'},
              {'Title': 'Ribbon Cutting: Ink Properties, LLC', 'Date': 'March 15, 2022', 'Time': '12:00 pm - 12:30 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/15/business-celebration/ribbon-cutting-ink-properties-llc/',
               'Description': 'Join us for the celebration of the opening of Ink Properties, LLC!\nMasks and social distancing are encouraged.'},
              {'Title': 'Links Group #4', 'Date': 'March 16, 2022', 'Time': '11:30 am - 1:00 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/16/business-growth/links-group-4/',
               'Description': 'This non-compete leads group offers business networking and referral marketing.\nTo learn more about joining this group contact Andrew Van.'},
              {'Title': 'Ribbon Cutting: Holy Molli', 'Date': 'March 17, 2022', 'Time': '10:30 am - 11:00 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/17/business-celebration/ribbon-cutting-holy-molli/',
               'Description': "Join us to celebrate Holy Molli's new location on Main St. in downtown Greenville!\nMasks and social distancing are encouraged."},
              {'Title': 'Growth & Infrastructure Committee', 'Date': 'March 18, 2022', 'Time': '8:30 am - 9:30 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/18/business-advocacy/growth-infrastructure-committee/',
               'Description': 'The Growth & Infrastructure Committee meets the select meeting months beginning at 8:30 am. This committee is open to any Chamber Investor interested in issues related to transportation and infrastructure. This committee often hosts guest presentations on important issues such as road projects, rail, air service, public transportation, and our ports. If you are interested in such topics, we encourage you to attend a meeting soon. \nThe Greenville Chamber is taking every safety precaution recommended by the CDC and state and local officials for our event, including limiting capacity and implementing social distancing during this event.  Attendees are encouraged to wear masks – whether you are vaccinated or not. We will continue to follow the latest CDC, state and local guidelines and will communicate any changes to our plan. If you feel sick, stay home!  You will be refunded or credited 100% of registration fees paid if you are ill due to COVID-19.'},
              {'Title': 'Links Group #2', 'Date': 'March 23, 2022', 'Time': '11:30 am - 1:00 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/23/business-growth/links-group-2/',
               'Description': 'This non-compete leads group offers business networking and referral marketing.\nTo learn more about joining this group contact Andrew Van.'},
              {'Title': 'Energy & Environmental Compliance Committee', 'Date': 'March 29, 2022',
               'Time': '8:30 am - 9:30 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/03/29/business-advocacy/energy-environmental-compliance-committee/',
               'Description': 'This committee is open to all Chamber Investors interested in environmental issues and how such issues can impact your business. The committee often hosts speakers from SCDHEC and other groups to talk about water and air quality, sustainability, energy, and other environmental initiatives in the community.  \nThe Greenville Chamber is taking every safety precaution recommended by the CDC and state and local officials for our event, including limiting capacity and implementing social distancing during this event.  Attendees are encouraged to wear masks – whether you are vaccinated or not. We will continue to follow the latest CDC, state and local guidelines and will communicate any changes to our plan. If you feel sick, stay home!  You will be refunded or credited 100% of registration fees paid if you are ill due to COVID-19.'},
              {'Title': 'Links Group #1', 'Date': 'April 7, 2022', 'Time': '8:45 am - 10:00 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/04/07/business-growth/links-group-1/',
               'Description': 'This non-compete leads group offers business networking and referral marketing.\nTo learn more about joining this group contact Andrew Van.'},
              {'Title': 'Business Advocacy Committee', 'Date': 'April 8, 2022', 'Time': '8:30 am - 9:30 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/04/08/business-advocacy/business-advocacy-committee/',
               'Description': 'The Greenville Chamber is taking every safety precaution recommended by the CDC and state and local officials for our event, including limiting capacity and implementing social distancing during this event.  Attendees are encouraged to wear masks – whether you are vaccinated or not. We will continue to follow the latest CDC, state and local guidelines and will communicate any changes to our plan. If you feel sick, stay home!  You will be refunded or credited 100% of registration fees paid if you are ill due to COVID-19.'},
              {'Title': 'Links Group #3', 'Date': 'April 12, 2022', 'Time': '8:30 am - 10:00 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/04/12/business-growth/links-group-3/',
               'Description': 'This non-compete leads group offers business networking and referral marketing.\nTo learn more about joining this group contact Andrew Van.'},
              {'Title': 'Greenville Chamber Young Professionals Biz & Coffee (for 2022 GCYP Members Only)',
               'Date': 'April 13, 2022', 'Time': '7:30 am - 9:00 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/04/13/leadership-development/greenville-chamber-young-professionals-biz-coffee-for-2022-gcyp-members-only/',
               'Description': 'The Greenville Chamber is taking every safety precaution recommended by the CDC and state and local officials for our event, including limiting capacity and implementing social distancing during this event.  Attendees are encouraged to wear masks – whether you are vaccinated or not. We will continue to follow the latest CDC, state and local guidelines and will communicate any changes to our plan. If you feel sick, stay home!  You will be refunded or credited 100% of registration fees paid if you are ill due to COVID-19.'},
              {'Title': 'Links Industrial', 'Date': 'April 14, 2022', 'Time': '8:30 am - 9:45 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/04/14/business-growth/links-industrial/',
               'Description': 'This non-compete leads group offers business networking and referral marketing in industrial industries.\nTo learn more about joining this group contact Andrew Van.'},
              {'Title': 'Coffee & Connections', 'Date': 'April 20, 2022', 'Time': '8:30 am - 9:45 am',
               'Link': 'https://www.greenvillechamber.org/events/2022/04/20/business-growth/coffee-connections/',
               'Description': 'Meet fellow investors and learn how to maximize face-to-face opportunities at this structured networking event hosted by Centre Stage. \nThe Greenville Chamber is taking every safety precaution recommended by the CDC and state and local officials for our event, including limiting capacity and implementing social distancing during this event.  Attendees are encouraged to wear masks – whether you are vaccinated or not. We will continue to follow the latest CDC, state and local guidelines and will communicate any changes to our plan. If you feel sick, stay home!  You will be refunded or credited 100% of registration fees paid if you are ill due to COVID-19.'},
              {'Title': 'Greenville Chamber Young Professionals Leadership Luncheon (for 2022 GCYP Members Only)',
               'Date': 'April 20, 2022', 'Time': '11:30 am - 1:00 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/04/20/leadership-development/greenville-chamber-young-professionals-leadership-luncheon-for-2022-gcyp-members-only/',
               'Description': 'The Greenville Chamber is taking every safety precaution recommended by the CDC and state and local officials for our event, including limiting capacity and implementing social distancing during this event.  Attendees are encouraged to wear masks – whether you are vaccinated or not. We will continue to follow the latest CDC, state and local guidelines and will communicate any changes to our plan. If you feel sick, stay home!  You will be refunded or credited 100% of registration fees paid if you are ill due to COVID-19.'},
              {'Title': 'Links Group #4', 'Date': 'April 20, 2022', 'Time': '11:30 am - 1:00 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/04/20/business-growth/links-group-4/',
               'Description': 'This non-compete leads group offers business networking and referral marketing.\nTo learn more about joining this group contact Andrew Van.'},
              {'Title': 'Ladies Classic Golf Tournament', 'Date': 'April 25, 2022', 'Time': 'N/A',
               'Link': 'https://www.greenvillechamber.org/events/2022/04/25/all-chamber/ladies-classic-golf-tournament/',
               'Description': 'Calling all women of the Greenville Chamber! Join us for a day of fun and networking – on the links. Whether you’re a seasoned golfer or have never picked up a club, we invite you to come play and enjoy the sites, tastes and sounds of Greenville while socializing amongst our city’s most prominent businesswomen.\nThe day will begin with a shotgun start at 10:00am, followed by a Captain’s Choice round featuring 12 holes at the Upstate’s favorite Par-3 course, 3’s Greenville Golf and Grill. Participants will also have the opportunity to compete in individual contests throughout the day, including a putting contest, closest to the pin and a final shootout following the round.\nParticipants are invited to join the Ladies Classic Par3 Party immediately following their round.\nFill out the form below to sponsor or register for the event.\nPARTICIPATION LEVELS\n '},
              {'Title': 'Links Group #2', 'Date': 'April 27, 2022', 'Time': '11:30 am - 1:00 pm',
               'Link': 'https://www.greenvillechamber.org/events/2022/04/27/business-growth/links-group-2/',
               'Description': 'This non-compete leads group offers business networking and referral marketing.\nTo learn more about joining this group contact Andrew Van.'},
              {'Title': 'CRYPTO: DECRYPTED 101', 'Date': 'February 22, 2022', 'Time': '12:00 PM - 2:00 PM',
               'Link': 'https://www.litchainu.com/crypto-decrypted',
               'Description': 'LITCHAIN is hosting a three part webinar entitled CRYPTO:DECRYPTED 101 from 12pm-2pm on Feb 8, 15, and 22. This course explains the basic fundamentals of crypto with fun, live interaction. Folks will learn from experts about currency types, trading basics, portfolio management tips, and more. CRYPTO: DECRYPTED 101 makes crypto make sense, so individuals will go from #CryptoConfused to #CryptoConfident. LITCHAIN, located in upstate, SC is an unbiased, trusted source for everything crypto.For details and to register visit www.litchainu.com/crypto-decrypted '},
              {'Title': 'TAKE CHARGE OF YOUR HEART HEALTH - WEBINAR', 'Date': 'March 01, 2022',
               'Time': '12:00 PM - 1:00 PM',
               'Link': 'https://www.spartanburgregional.com/events/take-charge-your-heart-health',
               'Description': 'While little can be done about the risk factors of age, gender and family history in preventing cardiovascular disease, there are many others you can control by adopting healthy lifestyle habits. The beauty of tackling the risk factors under your influence is that they are all interrelated. Begin by managing one risk factor and work to control them all.Mitchell Devlin, DO with Medical Group of the Carolinas – Medical Affiliates – North Grove, will share what you need to know about the risks for cardiovascular disease and how to handle the ones influenced by your lifestyle.\n\nVisit SpartanburgRegional.com/Events to register.'},
              {'Title': 'HOLLYWOOD HEART ATTACK - WEBINAR', 'Date': 'March 15, 2022', 'Time': '12:00 PM - 1:00 PM',
               'Link': 'https://www.spartanburgregional.com/',
               'Description': 'When Hollywood characters have heart attacks in movies, they usually clutch their chests dramatically, break out in a cold sweat and drop to the floor. In real life, some people experience heart attacks this way, but it is also possible to experience nonspecific symptoms such as fatigue, indigestion or a feeling of a strained muscle in the back or chest to indicate that someone is having a heart attack. It’s important to know all the signs – including subtle ones – to ensure that you get the emergency care that you need.Mitchell Devlin, DO, a real-life cardiologist with Medical Group of the Carolinas – Medical Affiliates – North Grove, will share the signs and symptoms of a heart attack and how to seek lifesaving medical attention.\n\nVisit SpartanburgRegional.com/Events to register.'},
              {'Title': 'SCC IMPACT', 'Date': 'March 17, 2022', 'Time': '5:30 PM - 8:00 PM',
               'Link': 'https://www.sccsc.edu/foundation/',
               'Description': 'Join us as Spartanburg Community College celebrates the impact that the college has on Students, Careers, and the Communities of Spartanburg, Union, and Cherokee counties. Hear from our President, Dr. Michael Mikota, and Gordy Johnson of Johnson Development and meet the NEW SCC mascot!'}]

    edb = EventsDB(events, 'test')
    edb.add_events()
