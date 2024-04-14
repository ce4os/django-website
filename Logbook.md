# Motto of the project:
## Give me six hours to chop down a tree and I will spend the first four sharpening the axe.

## Sun Apr 14 06:41:43 PM CEST 2024 - Server up and running

### Step 1 - minimalistic app - or not
After starting development, the first question that arises is,
which preinstalled apps in settings.py do I actually need?
For now I will go with the admin site (for easy management and 
testing) and static files (as I want to have a single location 
to store static files). The only application so far is a blog so I don't need
authenticication, there won't be complicated models anytime soon 
so the contenttypes framework seems a bit like overkill (although
I have to deepdive at some point), the blog itself will be stateless
so sessions and messages won't be necessary.

BUT! "Computer says no" 
Server does not run and throws an error:
It turns out the admin site relies on: 
"django.contrib.admin",
"django.contrib.auth",
"django.contrib.contenttypes",
"django.contrib.messages",

Leaving out the admin application also throws an error:
LookupError: No installed app with label 'admin'.

Seems like I need to deepdive to disable all the apps I don't want.
So, I will go with all preinstalled apps to make sure everythin runs 
for now. 

### Step 2 - Database
The second question that arises is the database question. Do I use
the default sqlite3 database or another one? Since blogposts mainly consist
of rather uncomplicated datatypes (strings) and there are, so far, no
other planned features and since sqlite3 is simple and easy to use, 
I will go for sqlite3 for now. 

SIDENOTE: The search functionality and website performance with thousands
of blogposts seem to be a good argument for a non relational database
like mongodb.

### Step 3 - Hello world from fb_blog

Enabling the app fb_blog in settings.py [x] <br>
- Note: Django will complain without a comma after the app. According to the official documentation, there are two ways doing so:
Each string should be a dotted Python path to:
    - an application configuration class (preferred), or
    - a package containing an application.

Adding paths to mywebsite/urls.py (and a RedirectView for convenient redirecting) [x] <br>
Creating fb_blog/urls.py [x] <br>
Creating a basic HttpResponse in fb_blog/views.py [x] <br>

Everything works as expected. Now let's get serious!

### Step 4 - Planning 

#### Blog homepage – displays the latest few entries.

Home view should show the entries for the last 3 days including today. 
Home will look like this  

Fri Apr 12 2024
- [[l]]() Topic <br>
content
- [[l]]() Topic 

Thu Apr 11 2024
Wed Apr 10 2024
...

Note: What happens if there are no entries for 
Fri? Should go to Thu, Wed, Tue -> Latest three
days in the database 

Home view has a 
[whole month]()
element

Route could look like this:
https://myblog.de/

<hr>

#### Entry “detail” page – permalink page for a single entry.
A detail view will look like this:

Fri Apr 12 2024
- [[l]]() Topic <br>
content

Note: What is the primary key for each entry in the database? Fefe does not use a database but
he identifies each blogentry by its timestamp

<hr>

#### Month-based archive page – displays all days with entries in the given month.

Same as above but all entries for the current month

whole month has a 
[earlier]() tag that leads to the month before
[later]() tag that leads to the next month (if the month is not found it leads to: No entries found)
[now]() tag that leads back to the home view

route could look like this:
https://myblog.de/?mon=202404

<hr>

#### Day-based archive page – displays all entries in the given day.

Is this really necessary?

<hr>

#### Search functionality

Parses each entry in the database for the given keyword. Right now I think of it like this:
```sql
SELECT * FROM "blogentries" WHERE "entry" LIKE 
"%searchterm%"
```
Django uses an ORM however. 

<hr>

#### Questions:

How do I make the best use of djangos template 
engine?

base.html: 
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
    
<header>
    <h1>Title of my blog</h1>
     <a href="https://myblog/searchfunction/">Searchfunctionality</a> 
</header>
<body>
    {% block content %}

    {% endblock %}
</body>
<footer>
    <p>proudly made with django!!!</p>
    <a href="https://myblog/permaroute/">Some link</a>  
</footer>
</html>
```
In the end this will look different but this is the main idea. 

How do I store Blogentries in the database? Markdown? How do I make sure they get rendered the way I want them
to be rendered? Bold letters, links, citing, 
bullet points etc. pp.. 
Whats the primary key? 
Looking forward to work with dates again...
