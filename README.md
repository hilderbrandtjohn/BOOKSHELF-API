## BOOKSHELF API

----
Get information about books via a RESTful API

---
#### Pre-requisites
* Have Python3, pip installed on your local machines.

* **Start your virtual environment** 
From the parent folder run
```bash
# Mac users
python3 -m venv venv
source venv/bin/activate
# Windows users
> py -3 -m venv venv
> venv\Scripts\activate
```

* **Install dependencies**<br>
From the parent folder run 
```bash
# All required packages are included in the requirements file. 
pip3 install -r requirements.txt
# In addition, you will need to UNINSTALL the following:
pip3 uninstall flask-socketio -y
```

### Step 1 - Create and Populate the database

1. **Create the database
In your terminal, navigate to the parent directory, and run the following:
```bash
# Connect to the PostgreSQL
psql postgres
#View all databases
\l
# Create the database
\i setup.sql
# Exit the PostgreSQL prompt
\q
```


3. **Create tables**<br>
Once your database is created, you can create tables (`bookshelf`) and apply contraints
```bash
# Mac users
psql -f books.psql -U student -d bookshelf
# Linux users
su - postgres bash -c "psql bookshelf < /path/to/exercise/backend/books.psql"

```
**You can even drop the database and repopulate it, if needed, using the commands above.** 


### Step 2: Start the server
Start the Flask server by running the command below from the parent directory.
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

---

#### Running Tests
Navigate to the parent folder and run: 
```bash

python test_flaskr.py
```