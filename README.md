This repository is dedicated to the web scraper used by [USC Upstate's Center for Entrepreneurship and Innovation](https://uscupstatecei.org/) (CEI).

It works by scraping four different websites, namely:

[Greenville Chambers](https://www.greenvillechamber.org/index.php?src=events&srctype=glance&submenu=_newsevents),
[South Carolina Research Authority](https://www.scra.org/calendar/list/),
[Spartanburg Area](http://spartanburgareasc.chambermaster.com/events/), and
[StartGrowUpstate](https://www.startgrowupstate.com/explore-events).

The scraper looks for event title, date, time, link, and description and then publishes these events to the CEI's [Event Page](https://uscupstatecei.org/events).

To scrape the websites, I use Selenium. The program runs at 07:00 AM Eastern Time on Monday's, Wednesday's and Friday's and is schedule to run on my local machine using [CRON](https://crontab.guru/).

For more information, email me at [canasmh@yahoo.com](mailto:canasmh@yahoo.com)
