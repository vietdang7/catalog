# Catalog  Project
The project is created for Udacity Full Stack Nanodegree Programme.
![Catalog Example](https://github.com/vietdang7/catalog/blob/master/static/catalog.gif)


## Code Example
Here are some lines of example code:
1. catalog.py:
```python
# Import flask and sqlalchemy library
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import asc desc
from sqlalchemy import asc, desc


# Import for anti forgery state token
from flask import session as login_session
import random
import string


# Import for gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


# Import from database_setup.py
from database_setup import Base, User, Category, CatalogItem


# Create CLIENT_ID
CLIENT_ID = json.loads(open('client_secrets'
                            '.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Item App"


app = Flask(__name__)

# Create database connection
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Making anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)



```

## Why I create this project?
This is one of projects of Full Stack Udacity Nanodegree. Main reason is to evaluate the skills I have learnt (CRUD, API Endpoint, OAuth...).

## Functions of Catalog Application
After login with you Google Account, you can create/edit/delete your own category, item. Without login, you will be able to check the catalog items in the front page.

## Getting Started
### Prerequisites
1. You need to have code editor like `Atom` to modify the code 
2. [Vagrant](https://www.vagrantup.com/downloads.html)
3. [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
4. You need to have Google Account to setup OAuth 2.0 

### Installation
1. Clone this project (Using `https://github.com/vietdang7/catalog.git` or through your GitDesktop application)
2. Install VirtualBox
3. Install Vagrant
4. Download this [FSND-Virtual-Machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip) from Udacity (this will install all needed OS, software in your VirtualBox)
5. Unzip the file, change to this directory in your terminal - `cd` command.


## Testing
1. Move cloned folder `catalog` to `vagrant` folder
2. Run Vagrant by type `vagrant up`, and `vagrant ssh`to log in
3. Move to catalog folder in vagrant by entering `cd /vagrant/catalog`
4. Run application by entering: `python catalog.py`
5. Open `http://locahost:5000` in your browser to test application

## Built With
- Python3
- Flask
- SQLalchemy
- SQLite
- HTML
- CSS
- Bootstrap

## Contribution
If you want to make contribution for this project, feel free to `fork` this project and make `pull request`

## License

- Copyright of FSND-Virtual-Machine.zip are belong to [Udacity](https://github.com/udacity/).
- This project is licensed under the MIT license
