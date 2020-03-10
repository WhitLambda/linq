# Linq by Lambda
## Lambda
Lamda is a team of students at Whitworth University. As part of the software engineering capstone class, Team Lambda is working with client Dallas Crockett in order to create the product, Linq. 

### Team Members
- Lauren Barry
- Sam Holzer
- Amon Sthapit
- Allysa Sewell
- Becca Soderberg

## Linq
Today Lamba, of Whitworth University, announced the release of their new product, Linq. Linq is a product where social-media influencers and content creators view comments and interact with their audience in one place. 

Linq aggregates comments from a variety of social media platforms, such as Instagram, YouTube, and Twitch. Comments data is cached, so content creators have multiple views to choose from. Comments are viewable on a per-platform, per-user, per-post, or aggregated (all-together) basis. 

Linq has data processing features that allow content creators to interact with their audience through a single platform. For example, content creators can set trigger phrases/words to search for in their comments. Content creators can then add automatic responses and interactions. This allows users to easily respond to commonly asked questions, or to moderate their chat/comments section efficiently.

## FAQ
### Who can use Linq?
Linq is best for social media influences and other content creators such as Youtubers and Streamers.

### What social media platforms are supported currently?
Currently, Linq supports Instagram, YouTube, and Twitch. Other platforms are not currently available, however they may be considered in the future. 

### How can I view my comments with Linq?
Linq allows you to view all of your comments in one place. You can choose whether you'd like to view your comments: per-platform, per-user, per-post, or aggregated (all-together). 

### How do I interact with comments?
Linq allows influencers to designated phrases and words to watch for, as well as a pool of responses. Linq can be configured to automatically respond, or simply suggest responses to the content creator when they're viewing their comments. 

## Development
### Technologies Used
- Python
- Django
- PostgreSQL

### Dev Environment
Linq is developed using [`venv`](https://docs.python.org/3/library/venv.html) virtual environments. The following scripts can be used to activate the development environment. 

- `source linq-venv/bin/activate`:
Activates the virtual environment. 

- `python3 manage.py runserver` (in `linqbackend` folder): Starts the Django development server.
Open a browser and go to http://localhost:8000 to view.

- `deactivate`:
Deactivates the virtual environment.

### Local PostgreSQL database setup
[ instructions are for windows, might be different for mac ]
- install postgresql binary from official website
- set password for (superuser) postgres   [ save it somewhere ]
- install python
- $ pip install psycopg2

references:
https://courses.cs.washington.edu/courses/csep544/11au/resources/postgresql-instructions.html
https://www.jetbrains.com/help/datagrip/connecting-to-a-database.html#connect-to-postgresql-database

- $ createdb -U postgres <db_name>                 [ create new database as postgres superuser ]
- $ psql -U postgres <db_name>                        [ connect to database ]
[ you need to be connected to the db in a terminal to use it in DataGrip ]

[ I recommend using JetBrains DataGrip for a more visual access to the database ]
- install JetBrains DataGrip (make a student account for free access)

connecting to datagrip:
- make sure psql is connected to the database in a console/terminal
- $ psql -U postgres <db_name>
- open datagrip
- menu > file > new > data source > postgresql
- change [database:] to <db_name>
- test connection
- ok
- database should load into datagrip
