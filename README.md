# Hackfolio
One stop place for uploading and getting to know about hackathon opportunities
Any authorized user can create, update and delete hackathons on the site. 
Guest users can only view all the listed hackathons
## Local Setup
- `git clone https://github.com/dhananjaypai08/Hackfolio.git`
- `cd Hackfolio`
- `python3 -m venv env`
- `pip3 install -r requirements.txt`
- `cd hacksite`
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`
- `python3 manage.py createsuperuser`
  Create super user with your credentials
- `python3 manage.py runserver`

- Head over to <a href="http://127.0.0.1:8000/">http://127.0.0.1:8000/</a>

## Built with
- Django, Django rest Framework
- Jinja1, HTML, Css, JavaScript
- SQLite, serializers

Cheers!
