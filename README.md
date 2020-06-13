# GrocerCheck

A website to help people reduce contact at grocery stores and essential services

## How to use GrocerCheck

- **Live data:** Shows only live busyness
- **Live and Historical:** Shows live busyness as well as estimated busyness from past trends
- **All stores:** Show stores even if no live data can be found for them
- **Show closed stores:** Show stores that are currently closed
- **Search:**
    - Search by name - e.g. `"Costco, Superstore, Costco London"`
    - Search by street, location, or neighbourhood - e.g. `"broadway, main, 41st avenue, Vancouver, kerrisdale"`
    - Search by category with keywords - e.g. `"Asian grocery, supermarket, bulk"`
    - Search by proximity with "near me" term (Location **must** be on for this to work)
    - Or a combination of the above!
        - `"asian grocery near me"`
        - `"bulk on kingsway"`
        - `"kerrisdale grocery on broadway"`

## How it works
GrocerCheck is built on the <a href="https://github.com/django/django">Django</a> web framework and <a href="https://github.com/apache">Apache2</a> http web server. To get our data, we make a special google request to get data not available via google maps api. The scraper runs on our <a href="https://github.com/GrocerCheck/LivePopularTimes">LivePopularTimes</a> python module, which is scheduled with celery to aggregate live populartimes for stores with live data every 10 minutes. Requests are routed through <a href="https://luminati.io/?affiliate=ref_5eaf77edc7669177ab3b82b5">Luminati.io</a> data collection networks to ensure reliable retrieval and server security; the last thing we want is our IP blocked! Data is stored in a standard sqlite3 database, from which markers are generated and placed on a map rendered by <a href="https://cloud.google.com/maps-platform/">Google Maps Javascript</a> API.

Blog and content pages are run-of-the-mill css dynamic galleries.
COVID Watch works as a dynamic gallery of links to an article template populated as per their sql id in the url.

## Is GrocerCheck open-source?
#### **You bet it is!**
We would be thrilled to see you contribute!

## How can I support GrocerCheck?
GrocerCheck Foundation is a registered non-profit organization run by high-school and incoming university students. A small donation can go a long way to help us pay for operational costs. Donate to us <a style="font-weight: bold;" href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=CTEMURSS3HR94&source=url">here.</a> All excess funds go towards the Vancouver General Hospital COVID-19 relief fund!

## Let's get in touch.
#### Want to work with us? Want to write for COVID-Watch? Want to help translate GrocerCheck?
- Talk to Brian: brian@grocercheck.ca
#### Want to find out about sponsorship opportunities?
- Talk to Preston: preston@grocercheck.ca
#### Want to help expand GrocerCheck?
- Talk to Andy: andy@grocercheck.ca
#### Want to just say hi? or anything else, really
- Talk to us at info@grocercheck.ca

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
