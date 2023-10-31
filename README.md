# bluebike-routing-app

#### Application that allows a user to route from one Bluebike station to one close to their destination. Built with Python (Flask back-end) and JavaScript/HTML/CSS (Jinja2 front-end). Mapping/Routing information is retrieved from the Google Maps API. Map is also interactive, so can be zoomed in/out as needed. 

#### The station data is based on the csv file retrieved from https://www.bluebikes.com/system-data (station location data). 

#### The route tracked is based on a user's current coordinates (retrieved via geocoder library in python). The route in the attached picture is from a sample starting location, not my actual location (so don't try to find me there pls). 


#### Use Case
##### For example, if I'm by the Boston Common BlueBike station and want to bike to is Harvard University, what is the closest station to Harvard that I can dock my bike to minimize my travel? This application displays the location and the directions/routing to get that closest station via GoogleMaps API. 

#### Sample Screenshots
<img width="1403" alt="Screenshot 2023-10-31 at 7 08 57 PM" src="https://github.com/ariangokhale/bluebike-routing-app/assets/55399896/4d69b67a-2892-43aa-8ae1-d78bf3691319">


#### sample input "Harvard University"
<img width="1414" alt="Screenshot 2023-10-31 at 7 13 51 PM" src="https://github.com/ariangokhale/bluebike-routing-app/assets/55399896/d4406a79-0f5e-4166-8ee2-c46816dc9c61">
