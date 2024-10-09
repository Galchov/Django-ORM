# Python-ORM-2024
Course of SoftUni - Second part of the module Python DB

## 0. ORM Introduction / Project Configuration
### 0.1. Setting up a virtual environment and Django project
<br>

**Step 1: Set up your Python virtual environment**

Make sure you have Python 3.x installed. You can download it from [here](https://www.python.org/)

Verify your Python version.
```bash
python --version
```
Install virtualenv. Virtual environment helps to manage project dependencies.
```bash
pip install virtualenv
```
<br>

**Step 2: Create your project directory**

Create new directory, where your project will be, then navigate to it.
```bash
cd path\to\your\workspace
mkdir my_django_project
cd my_django_project
```
<br>

**Step 3: Set up a virtual environment**

Inside your project directory, create a new virtual environemt that will be used only for this project. Named 'venv' (Optional)
```bash
python -m venv venv
```
The virtual environment must be activated. Activation can be confirmed, once (venv) appears at the very left in you shell prompt.
```bash
venv\Scripts\activate
```
You can see the current packages.
```bash
pip list
```
If you want to install a new package. [More details on packages here](https://packaging.python.org/en/latest/tutorials/installing-packages/)
```bash
pip install <package_name>
```
If you have to install packages from 'requirements.txt' file.
```bash
py -m pip install -r requirements.txt
```
Or if you want, you can also export your packages to 'requirements.txt'. (To be used for other projects)
```bash
pip freeze > requirements.txt
```
<br>

**Step 4: Install Django**

Once the environment is activated, it is time to install Django in it.
```bash
pip install django
```
Verify Django installation and see its version.
```bash
django-admin --version
```
<br>

**Step 5: Create a new Django project and start it**

Create a new Django project.
```bash
django-admin startproject my_project
```
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
