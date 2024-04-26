My django website
=================

My django website is a side project of mine to deepen my 
knowledge in Django and in general webdeveloment, to understand how 
to deploy from development to production, how to secure my
website, to explore the differences between function and class based approaches and
so on.  **But first and foremost to have fun developing a project!**


Expected features
-----------------

### A blog build with django

For this application I will use [Fefes Blog](https://blog.fefe.de) as a blueprint and his talk about [writing secure software](https://media.ccc.de/v/37c3-11811-writing_secure_software) at the [37C3](https://media.ccc.de/b/congress/2023) as a guide for security measurements. 
In general, the blog will have:

- Blog homepage – displays the latest few entries.
- Entry “detail” page – permalink page for a single entry.
- Month-based archive page – displays all days with entries in the given month.
- Search functionality 

After developing the basic blog, I plan on customizing the whole project. 

Installation
------------

Installation under the assumption that you:
- are working on a Linux machine
- have Python installed (usually goes hand in hand with first requirement)
- have the python package venv installed to isolate the project


you can install this project 
by cloning this repo and then running:

```sh
# Creating a virtual environment
python3 -m venv .venv

# Activating the virtual environment
source .venv/bin/activate

# Installing required software
pip install -r requirements.txt

# run development server
python3 manage.py runserver
```


In the browser of your choice, go to:
localhost:8000. Now you should be able to 
explore the functionality.

License
-------

This project is licensed under the Creative Commons Zero v1.0 Universal License


