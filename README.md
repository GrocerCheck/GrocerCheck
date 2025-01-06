# GrocerCheck [deprecated]

# Update Jan 5 2025

grocercheck has been taken offline. Here are some screenshots for posterity

main menu
![image](https://github.com/user-attachments/assets/af364fc3-676c-4465-b40a-4cfe94ba4050)

help
![image](https://github.com/user-attachments/assets/fe99ed34-919f-44b2-a3c2-f5fa7aa37007)

detail view of a grocery store
![image](https://github.com/user-attachments/assets/a3e79e3e-8140-48fd-a630-8b2b7a5a5966)


change between live data only & w/ historical augmentation

![image](https://github.com/user-attachments/assets/d9309be2-6209-438e-ad4e-e2d24b910448)

search filtering results

![image](https://github.com/user-attachments/assets/f874bca7-cc4a-4386-9e82-522993463c4b)

region select

![image](https://github.com/user-attachments/assets/c6b7f1e8-5234-4936-b6ce-795de0e33ea9)


bay area
![image](https://github.com/user-attachments/assets/303b5a05-3b06-41db-aa9f-24e2e1247b07)

seattle
![image](https://github.com/user-attachments/assets/b9d1dc5d-ffb2-4222-82d2-c9695bef0095)

toronto
![image](https://github.com/user-attachments/assets/95886b56-7d48-467d-bcc9-f500c330be60)


Some of the CovidWatch articles
![image](https://github.com/user-attachments/assets/35625bcc-382b-4a41-a4c4-e6a76d3cd0d4)
![image](https://github.com/user-attachments/assets/2946e7cf-5aa1-43b2-95df-821c2fd0fe77)
![image](https://github.com/user-attachments/assets/236d9cd0-2451-40c3-9117-bb4013efb3c0)
![image](https://github.com/user-attachments/assets/03bf65c5-53d5-403f-b921-85e53c3d1307)
![image](https://github.com/user-attachments/assets/d42740ce-a7cc-4a6c-85c7-fb9123ff95d1)
![image](https://github.com/user-attachments/assets/f14816cc-d006-4b04-b9e1-b9df335aef45)


Looking back we had a good amount of press coverage.

CBC: https://www.cbc.ca/news/canada/british-columbia/bc-youth-entrepreneurs-covid19-1.5784637
dailyhive: https://dailyhive.com/vancouver/grocercheck-vancouver
some more linked on Brian's personal page https://chenbrian.ca/posts/projects/

All in all, building this was quite the adventure for our 17/18 year old selves back then, and we hope that it, at the very least, helped someone.


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
