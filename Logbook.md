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
- Note: Django will complain without a comma after the app. According to the official documentation, there are two ways of enabling the app:
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


#### Django ORM - creating a model for BlogPosts

A blogpost has a title, a body, a time it has been created at. 
I want to use the time the blogpost gets created at as the primary key. 
This is generally not recommended since there can be issues with 
uniqueness of a timestamp (rare case scenario). But since this is my
own blog and not a site people other than me will use, this won't 
be an issue. 

On second thought, the primary key can just be provided by django. It
seems to much of a huzzle to mimic fefes https://blog.fefe.de/?ts=98e3fee4
permalinks to his blogposts just to mimic it. So a draft of the post model 
looks like this:

```python
class Post(models.Model):
    """A model representing a blog post"""
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-created_at"]
```

The title can be long but not to long. The body can be of arbitrary length. 
The created_at attribute will provide a way to access blogposts in the right 
order. The __str__ method is overwritten for easy and recocnisable representation.
The posts will be orderd by created_at in descending order. The newest entry will always
be on top of the database. The default for created_at was choosen so that mockposts 
can be more conveniently created (as opposed to auto_add=True).

#### Populating the database with mock data

Three blogposts for today, one for yesterday, two for the day before yesterday.
Link to detail views works. The first real problem arises:
How do I query the database so The queryset will always contain the latest three days.
Examples:
Fri, Thu, Wed
Fri, Sun, Fr

See: TODO in fb_blog/views.py


## Tue Apr 16 01:26:59 PM CEST 2024

Right now I am facing several problems. Maybe a descriptin helps.

1. Formatting

When visiting home, every Post has a header, stating the day it was posted.

Tue Apr 16 2024. 
- Post1 

Tue Apr 16 2024
- Post2

Tue Apr 16 2024 
- Post 3

This is not really elegant since some posts will be released on the same day. Desired behaviour: All blogposts for one day have a single headline.

Tue Apr 16 2024
- Post1
- Post2
- Post3

2. Getting the right queryset

The home view should provide the posts for the last three days. The last three days are not necessarily in a row. So if home_view gets called
it should return for example:
Tue Apr 16 2024
- Post1
- Post2
Fri Apr 12 2024
- Post1
- Post3
Wed Apr 10 2024
- Post1

3. Monthly view: 
- Queryset for the whole current month

4. Link to: earlier month -> How to calculate the earlier month? And how to pass the variable to the view?

5. Link to: later month -> Same as above. But also
what to do if it is a month in the future and there are no posts?

6. How do I render the body of the posts? Right now there is no way to format that text in any way. But I want to be able to use HTML tags. 
The obvious solution is to store body and Update
As HTML files in the database. I am fairly sure
this problem arose before and there is a built-in
solution. 

7. Impressum
What do I need to write down there?

8. Updates
The blueprint blog: blog.fefe.de sometimes
has updates on posts. Do I provide a 
Update field to implement that functionality?

Probably I should create a global TODO file for
this project.


## Sun Apr 21 03:42:49 PM CEST 2024

I solved problems 1 and 2. 
Here's the code:

```python
# models.py
class Date(models.Model):
    """A model representing a specific day"""
    created_at_date = models.DateField(default=timezone.now, unique=True)
    
    class Meta:
        ordering = ["-created_at_date"]
    
    def __str__(self):
        return str(self.created_at_date)

# views.py
def get_home_view_queryset():
    queryset = []
    latest_three_days = Date.objects.all()[:3]
    for day in latest_three_days:
        queryset.append(Post.objects.filter(created_at_date=day))
    return queryset


def home_view(request):
    queryset = get_home_view_queryset()
    context = {"queryset":queryset}
    return render(request, "fb_blog/home.html", context)
```
I created a Date model to be able to retrieve the latest 
three days without much of a huzzle. The date is a foreign key to every blogpost and defaults to the day the
post is created. The queryset contains the posts for the latest three days. 

```html
{% for posts in queryset %}

    <h3>{{posts.0.created_at_date.created_at_date|date:"D M d Y" }}</h3>
    
    {% for post in posts %}
        <ul>
        <li><a href="{% url 'detail' post.id %}">[l]</a> {{post.title}}</li>
        <p>{{post.body|safe}}</p>
        {% if post.update %}
            <p><b>Update: </b>{{post.update}}</p>
        {% endif %}
        </ul>

    {% endfor %}

{% endfor %}
```

As I progress, I realize that I started tinkering. 
Back to square 1.

I have to remind myself:

"Give me six hours to chop down a tree and I will spend the first four sharpening the axe."
 
## Planning phase 

Blog will have:

<hr>

### 1. Home view

- Functionality:
    - Links to: 
        - Month view: {% url "month" month_id=latest_post.ts|date:"Ym" %} 
        - Impressum links to: impressum.html
    - Shows: search functionality
    - Every blogpost has a link to its detail view: {% url "detail" post.id %}

- The home view will show all posts of the last three days with blogentries. 

- The URL will look like this: mywebsite/blog/

- Edgecases: 
    
    What is the current month here:

    - Entries for the 1st of May, 30th of April, 28th of April
    - Entries for 2nd of May, 2nd of April, 2nd of February
    
- Question: 
    - How to retrieve posts for the latest three days from the database efficiently? 

<hr>

### 2. Detail view
- Functionality:
    - Links to: Whole month, home, itself, Impressum 
    - Shows: search functionality
- URL will look like: mywebsite/blog/detail/\<int:post_id>

<hr>

### 3. Monthly view

- The month view will show all days with blogentries for a specific month. Identified by
its string representation: Example: 
    - April 2024 = 202404
    - March 2024 = 202403

- Functionality: 
    - Links to: 
        - earlier month {% url "month" month_id=current_month-1 %}
        - homeview {% url "home" %}
        - later month {% url "month" month_id = current_month + 1%}
        {% if not queryset %}
            <p>No entries found</p>
        {% endif %}
    - Shows: search functionality

- URL will look like this: mywebsite/\month=202402

<hr>

### 4. Search functionality

- Backend has to sanitize user input!
- Searches all posts in the database for searchterm. 

<hr>

### 5. Impressum

- Link to html file

<hr>

### 6. A database to store Blogentries

Model of a blogpost:
```python 

class Month(models.Model):
    """A model representing a Month"""
    created_at = models.DateField(default=)

    def __str__(self):
        return str(self.created_at)

class Day(models.Model):
    """A model representing a day"""
    created_at = models.DateField()

class BlogPost(models.Model):
    """A model representing a blog post"""
    title = models.CharField()
    body = models.TextField()
    update = models.TextField()

    created_time = models.TimeField()
    month = models.ForeignKey()
    day = models.ForeignKey()

    class Meta:
        ordering = ["-created_date", "-created_time"]

    def __str__(self):
        return self.title
```

<hr>

### HTML Files

base.html shared by all views

- Title, subtitle
- Impressum
- Search function

home.html, detail.html and month.html
all share code for 

--------------------------------------------

## Wed Apr 24 01:41:20 PM CEST 2024

I finished with the basic functionality today. What really gave me a headache
was the queryset for the homeview. My solution works but is horribly ugly, awkward
and inefficient. In general there is some redundancy in the code:

- templates/fb_blog/: Home view and month view use the same template logic
- fb_blog/views.py: get_previous_month and get_next_month look fairly similar except one uses addition and one subtractions. Both look awefully complicated for what they actually do. 

Questions: 
1. What to do with invalid urls like blog/10/, blog/detail/wrongstring? 


## Working on TODO

DRY:
 - templates/fb_blog/: Home view and month view use the same template logic
 Define a html file that contains the redundant logic. {% include 'path/to.html' %}

Beautify:
- From brute to smooth:
    - get_home_view_queryset():
    Query the database for distinct dates. 

Searchfunctionality:
- Either use django forms or html forms.
-> To use django forms, I would have to change all the views to have a form in the context that gets passed to the base.html (because the search functionality should be visibile in all views except impressum)
Therefore, I use raw html forms in base.html


## Thu Apr 25 03:17:26 PM CEST 2024

Search functionality implemented:

locations:

fb_blog/templates/fb_blog/base.html
    - form tag
fb_blog/templates/fb_blog/search.html

fb_blog/views.py
    - search_view()
    - assemble_posts()

For now, it is a really basic search functionality. It will search for a string
in a blogposts title, its body and its update. It does
the trick for a single word like "Blueberry" and it is also case insensitive meaning "Cheesecake" will return all blogposts with cheesecake cheese. A searchterm like: blueberry cheesecake will return no posts...
