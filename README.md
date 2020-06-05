# blog-platform
Blog platform python3 and django.

## Requirements
- Python3
- Django3
- python virtual enviornment

## Install for testing
1) Activate Virtual Enviornment
   - source venv/bin/activate
2) Install requirements
   - pip install -r requirements.txt
3) migrade models 
   - python manage.py makemigrations blog
   - python manage.py sqlmigrate blog 0001
   - python manage.py migrate
4) run server
   - python manage.py runserver


 

This project was to help learn python3 and django better. 
