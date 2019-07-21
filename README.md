# Gist
### Description
The web application like gist.github.com, that is allowing you to store and share code snippets
### Specification
- Python 3.7
    - Flask 1.1
- JavaScript (ES2015+)
    - highlight.js (https://highlightjs.org/)
- HTML5
    - Jinja2
- CSS
    - SASS
- PostgreSQL 10

### Installation
1. prepare DBMS (Postgres)
   + create a user which can login and create databases
   + or
   + change connection in config.py (variable POSTGRES_DATABASE_URL)
2. clone project to virtual environment with `Python 3.x`
3. run `pip install -r requirements.txt`
4. run `flask run` for start application
5. application running on `http://127.0.0.1:5000/`