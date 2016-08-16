# django-league
Django app which makes easy to create sports team website

## Requirements
Django == 1.9.7

Python >= 3

## Installation
Download app to your project and enable it in INSTALLED_APPS

Then include urls in urls.py

```url(r'^league/', include('league.urls', namespace='league')),```
