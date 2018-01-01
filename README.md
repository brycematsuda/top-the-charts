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
7. Run `python manage.py loaddata ddr` to initially populate database with the provided JSON file dump containing the latest song data (as of 12/31/17) and current list of chart videos.
8. Create superuser with `python manage.py createsuperuser` to access admin module.
9. Run server with `python manage.py runserver`
 
Project Scope
------------
### Current Assumptions
* All songs unlockable for normal play via events are filed under the folders they are placed in after they are unlocked.
* All remaining songs that can only be played via the Extra Stage system and not at any point during normal play are filed under the latest version's folder.

### Current Limitations

Data or features in this project thare are not included or will not be pursued at this time for various reasons (space, time, liability, not worth the effort, etc.) include, but are not limited to:

* Picture banners
* Songs that are not available for play at any point as of the latest DanceDanceRevolution version
* Old 1-10 scale ratings
* Song English translations/transliterations
* Minimum/maximum BPM 
* Step count
* Song trivia
* Any type of file hosting
* Score tracking
* User accounts (aside from admin module)

Contributing Data
------------
You can edit the JSON manually, or add data via the admin module and dump it using the following command:  
`python manage.py dumpdata ddr.folder ddr.song --indent 2 > ddr/fixtures/ddr.json`

Video Quality Guidelines
------------
1. User should be able to clearly see the whole chart and follow along to the music.
2. No chart mods besides speed mods that don't take away from #1.
3. No note mods aside from default/note.

StepMania/line out videos are generally preferred over external camera recordings for this matter, but camera recordings are fine for a song chart if a StepMania/line out video doesn't exist and it follows the aforementioned guidelines. 

Temporary Roadmap/To-Do
------------
* Finish adding as much video data possible for all songs.
* Add views for other sort options (Song title, genre, BEMANI game)
* Add wiki/readme pages explaining models
* Look into adding other games (Sound Voltex, beatmania IIDX, CHUNITHM, etc.)