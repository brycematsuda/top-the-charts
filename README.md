Top The Charts
==================
Top The Charts is a webapp for DanceDanceRevolution players to quickly lookup song information and chart videos for the latest version of DanceDanceRevolution using a modern, responsive UI and RESTful urls.

Pre-Requisites
------------
* Python 3.X
* PostgreSQL
* [Firefox Geckodriver](https://github.com/mozilla/geckodriver/releases) (for Selenium testing)

Setup Instructions
------------
1. Install the pre-requisites.
2. Fork and clone the repo.
3. Move into root directory and run `pip install -r requirements.txt`
4. Generate a new Django secret key and place it in a new file `secrets.py` in the project folder (the same folder as `settings.py` and `urls.py`). This should not be checked into source control. An example file is included.
5. Create a PostgreSQL database and user with database access privileges using the details provided in the DATABASE variable in `settings.py`
6. Run migrations to create database with `python manage.py migrate`
7. Run `python manage.py loaddata ddr` to initially populate database with the provided JSON file dump containing the latest song data (as of 12/29/17) and current list of chart videos.
8. Create superuser with `python manage.py createsuperuser` to access admin module.
9. Run server with `python manage.py runserver`