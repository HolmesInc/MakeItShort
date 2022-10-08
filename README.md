# Test Project
## Goal
Create short link based on provided full link. Store amount of clicks for created short link
## Local installation
1) Pull Git repo
2) Perform migration: `./manage.py migrate`. Local DB db.sqlite3 with all required tables will be created.
3) Export Env variables:
```
export DJANGO_SETTINGS_MODULE=short_link.settings
export SECRET_KEY='<some super secret key>'
```
4) Run server:
```
./manage.py runserver 5050
```