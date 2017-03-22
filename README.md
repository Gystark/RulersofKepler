# RulersofKepler
Web Application Development 2 team project.

## Running the project

* Clone it from Github: `git clone https://github.com/Gystark/RulersofKepler`
* Install its requirements (optionally in a virtual environment): `pip install -r requirements.txt`
* Make migrations with `python manage.py makemigrations`
* Migrate, creating the SQLite database: `python manage.py migrate`
* Populate the database: `python populate_rok.py`
* Run the project with `python manage.py runserver`

### The login details for the default superuser are:

username: TestUser
password: testusrpwd