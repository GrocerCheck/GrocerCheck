# GrocerCheck

A website to help people reduce contact at grocery stores and essential services

## How to use GrocerCheck

- **Live data:** Shows only live busyness
- **Live and Historical:** Shows live busyness as well as estimated busyness from past trends
- **All stores:** Show stores even if no live data can be found for them
- **Show closed stores:** Show stores that are currently closed
- # **Search:**
    - Search by name - e.g. `"Costco, Superstore, Costco London"`
    - Search by street, location, or neighbourhood - e.g. `"broadway, main, 41st avenue, Vancouver, kerrisdale"`
    - Search by category with keywords - e.g. `"Asian grocery, supermarket, bulk"`
    - Search by proximity with "near me" term (Location **must** be on for this to work)
    - Or a combination!
        - `"asian grocery near me"`
        - `"bulk on kingsway"`
        - `"kerrisdale grocery on broadway"`
        
## How it works
GrocerCheck is built on the <a href="https://github.com/django/django">Django</a> web framework and <a href="https://github.com/apache">Apache2</a> http web server. The scraper runs on our <a href="https://github.com/GrocerCheck/LivePopularTimes">LivePopularTimes</a> python module, which is scheduled with celery to aggregate live populartimes for stores with live data every 10 minutes. Requests are routed through <a href="https://luminati.io/?affiliate=ref_5eaf77edc7669177ab3b82b5">Luminati.io</a> data collection networks to ensure reliable retrieval and server security; the last thing we want is our IP blocked! 

## divider
## Screenshots
- ### Help Screenshot
    - <img src="https://raw.githubusercontent.com/GrocerCheck/GrocerCheck/master/grocercheck/map/static/images/tutorial.png">

- ### Live data only
    - <img src="https://raw.githubusercontent.com/GrocerCheck/GrocerCheck/master/content/liveonly.png">

- ### All data
    - <img src ="https://raw.githubusercontent.com/GrocerCheck/GrocerCheck/master/content/all.png">

- ### Live and Historical
    - <img src = "https://raw.githubusercontent.com/GrocerCheck/GrocerCheck/master/content/liveandhistorical.png">

- ### With Infowindow
    - <img src = "https://raw.githubusercontent.com/GrocerCheck/GrocerCheck/master/content/livewithinfowindow.png">

## About Us

GrocerCheck Foundation is a registered non-profit organization run by high-school and incoming university students. 

L
