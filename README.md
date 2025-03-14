# INTRODUCTION
Course of SoftUni - Second part of the module Python DB

The course covers the basics of mapping between a relational database and an object-oriented model (ORM) with a focus on the Django framework. It begins with an introduction to ORM and its key concepts, before moving on to working with models in Django, including defining models, fields, and methods. The course then delves into advanced topics such as migrations and the Django admin interface, query operations, model relationships, and inheritance. Students will also learn more advanced techniques for working with models and working with ORM queries in Django. The course also covers another popular Python ORM framework, SQLAlchemy, which offers an alternative approach. During the training, exercises will be provided to help them consolidate their knowledge at each step. By the end of this course, participants will have acquired the basic skills to build robust, scalable, and efficient database-driven web applications using Python ORM frameworks.

## Skills you will gain

:heavy_check_mark: Working with a database using an ORM

:heavy_check_mark: Working with models and migrations

:heavy_check_mark: Data retrieval and manipulation

:heavy_check_mark: Using relationships between models

:heavy_check_mark: Model customization and optimization

:heavy_check_mark: More sophisticated techniques when working with ORM queries


## Who is this course suitable for?

The course is suitable for everyone who knows the principles of object-oriented programming and knows the basics of relational databases.
<br/>
<br/>

## 0. ORM Introduction / Project Configuration
### 0.1. Setting up a virtual environment and Django project (For Ubuntu Linux)
<br>

- **Step 1: Make sure Pyton is installed**

    Ubuntu comes with Python installed by default.

    Check Python version.
    ```bash
    python3 --version
    ```
    Update the system.
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
    <br>

- **Step 2: Create your project directory**

    Create new directory, where your project will be, then navigate to it.
    ```bash
    cd path\to\your\workspace
    mkdir my_django_project
    cd my_django_project
    ```
    <br>

- **Step 3: Set up a virtual environment**

    Inside your project directory, create a new virtual environemt that will be used only for this project. Named 'venv' (Optional)
    ```bash
    python3 -m venv venv
    ```
    The virtual environment must be activated. Activation can be confirmed, once (venv) appears at the very left in you shell prompt.
    ```bash
    source venv\bin\activate
    ```
    You can see the current packages.
    ```bash
    pip list
    ```
    To install a new package. For more details on packages click [here](https://packaging.python.org/en/latest/tutorials/installing-packages/)
    ```bash
    pip install <package_name>
    ```
    To install packages/dependencies from 'requirements.txt' file.
    ```bash
    python3 -m pip install -r requirements.txt
    ```
    Or simply run.
    ```bash
    pip install -r requirements.txt
    ```
    To export already installed packages to 'requirements.txt'. (To be used for other projects, for example)
    ```bash
    pip freeze > requirements.txt
    ```
    (In case 'pip' is not correctly linked to Python 3, use 'pip3' instead. But this is unlikely to happen)
  
    <br>

- **Step 4: Install Django**

    Once the environment is activated, it is time to install Django in it.
    ```bash
    pip install django
    ```
    Verify Django installation and see its version.
    ```bash
    django-admin --version
    ```
    <br>

- **Step 5: Create a new Django project and start it**

    Create a new Django project.
    ```bash
    django-admin startproject my_project .
    ```
    (The dot is for creating the project directly inside the directoty, without an extra folder)
  
    Verify the project structure. It should look like this.
    ```markdown
    my_django_project/
        manage.py
        my_project/
            __init__.py
            settings.py
            urls.py
            asgi.py
            wsgi.py
    ```
    Start the Django development server to make sure everything works.
    ```bash
    python manage.py runserver
    ```
    <br>

- **Step 6: Setup your database (Optional)**

    Django is using SQLite by default, but for this course we will be using PostgreSQL.
    
    Let's assume we all have PostgreSQL installed from the previous course. Now install Psycopg2 by running the command below for any OS - This is the adapter that connects the database to Django.
    ```bash
    pip install psycopg2
    ```
    Access PostgreSQL shell.
    ```bash
    psql -U postgres
    ```
    Create new database.
    ```SQL
    CREATE DATABASE your_database_name;
    ```
    Create a user for the database.
    ```SQL
    CREATE USER your_username WITH PASSWORD 'your_password';
    ```
    Grant the user access to the database.
    ```SQL
    GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;
    ```
    Exit PostgreSQL shell.
    ```SQL
    \q
    ```
    Now, open 'settings.py' file in your project and find the DATABASES settings. Replace the default SQLite settings with the PosgreSQL, so it looks like this.
    ```Python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_username',
            'PASSWORD': 'your_password',
            'HOST': 'localhost',                        # Or the IP address of your PostgreSQL server
            'PORT': '5432',                             # Default PostgreSQL port
        }
    }
    ```
    Once all the settings are updated, you have to apply migrations to set up your database schema.
    
    Run the following command:
    ```bash
    python manage.py migrate
    ```
    <br>
