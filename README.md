# CheckeeInfo-Scraper
This is a scraper that scrapes all the cleared visa processing information from [Checkee.info](http://checkee.info/) (anonymous data that available to public)

### Background
[Checkee.info](http://checkee.info/) is a website maintained by [mumuwang](http://www.websitegoodies.com/guestbook.php?a=view&id=169519) which allow people to record their visa application case. Most of the times, people log their information if their visa application got delayed because of **admistrative processing** (like myself).

The website is a great place to have an general view of the current visa application status. Nonetheless, the data has lots of limitations. From what I know, very few people know about this website and even less are willing to record their case and update it. Plus there are lots of other similar websites. In addition, lots of people recorded their cases but never updates it which confuses other people and make it very hard to estimate the overall distribution.

### Scraper
The scraper scrapes [Checkee.info](http://checkee.info/) using urllib and Beautifulsoup4 in Python 3 (3.6.0 64bit). It will go through all the listed cases that are available to the public and scrapes information including:
- Visa Type (e.g. F1)
- Visa Entry (e.g. Renewal)
- City
- Major (optional field)
- Case Status (Pending/Cleared)
- Check Date (when did the case started)
- Complete Date (when case is cleared)
- Waiting Days (days waited until the case is cleared)

Given that there are lots of cases never gets updated with a complete date, I only recorded those cases that are marked as *Complete*. When scraping is done, all the information will be assembled into a .csv file.

### Data Analysis
I tried to do some simple analysis with the data by myself. About 99.9% of the recorded fields in the auto-generated .csv file is good but the rest will have some issues like missing or misaligned field that needs some tweek.

Until 3/4/2017, I have **16297** visa application cases recorded dates back since 01/05/2009.
