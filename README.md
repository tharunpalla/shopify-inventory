# shopify-inventory - Shopify Backend Developer Intern Challenge - Summer 2022

Logistic Inventory CRUD application that meets the following requirements listed below.

### Requirements:
Basic CRUD Functionality.
1. Create inventory items
2. Edit Them
3. Delete Them
4. View a list of them
5. (Additional) Push a button export product data to a CSV

#### The application is deployed on heroku. You can access it using : https://shopify-inventory-crud.herokuapp.com/


### How To Run

The application requries python 3.6 or higher to run. You can download and install python from : https://www.python.org/downloads/release/python-3615/

1. Install `virtualenv`:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ virtualenv env
```

3. Then run the command to activate the virtualenv:
```
$ source env/bin/activate or .\env\Scripts\activate
```

4. Then install the dependencies:
```
$ pip install -r requirements.txt
```

5. Finally start the web server:
```
$ python app.py
```

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
    
Open http://localhost:5000/ on your browser to access the application
```
