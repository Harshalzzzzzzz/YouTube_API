# YouTube_API

Django based project to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## Features Implemented 

- Cronjob setup that calls the API every 5 mins.
- GET API that shows the entries in a paginated form
- Dockerized the application
- Interface to search and filter the responses/ db entries.
- Multiple API keys to automatically use the next available key.
- Admin dashboard to view cron logs and stored API responses in Video model.

## Setup 
- Clone the repository `git clone https://github.com/Harshalzzzzzzz/YouTube_API.git`
- To install dependencies run : `pip3 install -r requirements.txt`
- Add your YouTube API Keys to `API_KEYS` in `settings.py`
- In order to create and apply migration run :
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
- To run the server `$ python3 manage.py runserver` and go to `http://127.0.0.1:8000/` or `http://localhost:8000/` on your browser.
- In order to access the admin interface go to `http://127.0.0.1:8000/admin` and login. 
  (*Superuser* - Username : *harshal* Password : *12345678*) 
- To run cronjob using the console : `$ python manage.py runcrons`

## References

- [Django-cron](https://django-cron.readthedocs.io/en/latest/installation.html) lets you run Django/Python code on a recurring basis proving basic plumbing to track and execute tasks.
- [Django REST framework](https://www.django-rest-framework.org/tutorial/3-class-based-views/#using-generic-class-based-views) for the interface.
- [Docker Compose](https://docs.docker.com/samples/django/) to set up and run a simple Django app.
- [Django Filter](https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html#quickstart)  
- [Youtube API Key](https://console.developers.google.com/apis/enabled) 
- [Youtube API Documentation](https://developers.google.com/youtube/v3/docs/search/list)

