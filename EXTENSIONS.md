# Extensions

1. Amended interface to the NearEarthObject constructor to take a collection of zipped items which map data field to column name so that it can be parsed effectively and more importantly, can be tested in a more targeted fashion.

2. Added a `constants.py` file to map data field names to more readable constants names for use in extracy.py

3. Opted to subclass AttributeFilter to create a number of specialised filters which extract the relevant data value in question from CloseApproach objects and associated NEOs.


