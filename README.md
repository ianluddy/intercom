# Intercom

We have some customer records in a text file (customers.txt) -- one customer per line, JSON lines formatted. We want to invite any customer within 100km of our Dublin office for some food and drinks on us. Write a program that will read the full list of customers and output the names and user ids of matching customers (within 100km), sorted by User ID (ascending).

You can use the first formula from this Wikipedia article to calculate distance. Don't forget, you'll need to convert degrees to radians.
The GPS coordinates for our Dublin office are 53.339428, -6.257664.
You can find the Customer list here:
https://s3.amazonaws.com/intercom-take-home-test/customers.txt#


##### Solution

Written in Python2.7

##### To Run

`python intercom.py`


##### To Run Tests

`python -m unittest discover`
