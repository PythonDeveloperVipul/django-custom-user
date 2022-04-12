# backend

# Setup Project using virtualenv

create folder and change folder
```sh
mkdir folder_name
cd folder_name
```

The first thing to do is to clone the repository:

```sh
git clone https://github.com/PythonDeveloperVipul/django_custom_user.git
cd django_custom_user
```

Create a virtual environment to install dependencies in and activate it:

```sh
python -m venv env
source env/bin/activate
```

Then install the dependencies:

```sh
pip install -r requirements.txt
```

Then migrate database 

```sh
python manage.py migrate
```

Then runserver

```sh
python manage.py runserver
```