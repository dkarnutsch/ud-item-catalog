# ud-item-catalog
The item catalog app for the Full Stack Web Developer Nano Degeree. 

## Prerequisites
- python installed
- flask installed `(pip install flask)`
- sqlalchemy installed `(pip install sqlalchemy)`
- oauth2client installed `(pip install oauth2client)`
- httplib2 installed `(pip install httplib2)`
- requests installed `(pip install requests)`

## Running
A sample db is provided (item-catalog.db). However, if you want to create your own db, you can do that with `python database_setup.py`. The sample db also provides sample data items. If you want to create them on your own use `python lotsofitems.py`. To run the actual project use `python project.py`.

HINT: Possibly the easiest way to run it is in the Vagrant VM. Just clone it and run it.

## JSON Endpoint
The JSON Endpoint is available at http://localhost:5000/catalog.json.

## Credits
Most of the code is based on the Restaurant Project from the Full Stack Foundations Course. See https://github.com/udacity/ud330/tree/master/Lesson4/step2. 
