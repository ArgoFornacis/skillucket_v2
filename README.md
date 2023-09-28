# Skillucket

### Overwiew
Skillucket is a web application that allows users to gain new skills through exchange. 
Every user can list their skills that they are willing to teach and 
bucket skills that they wish to learn. After the registration and filling out both buckets, users are matched 
together. 

### Installation instruction
Skillucket is a Python Django project. It requires Python, pip and postgres to be installed.

After forking and cloning the project, preferably in VSCode or Pycharm, run the terminal command while being in the skillucket_v2 directory:

```
pip install -r requirements.txt
```

The next necessary step is to create a database using postgreql. For that run the commands:

```postgres
psql -U postgres -h localhost
```
And once in the postgres:
```sql
CREATE DATABASE your_database_name;
\q
```
Next create a file named .env to which copy and fill in the template:
```
export SECRET_KEY='your_secret_key'
export DB_NAME='your_database_name'
export DB_USER='postgres'
export DB_PASSWORD='your_password'
export DB_HOST='localhost'
export DB_PORT='5432'
```
Run in the terminal:
```commandline
source .env
```
Create and run migrations to fill out the database:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
Run the server to check if everything is working correctly: 
```
python3 manage.py runserver
```

### Features

- **Register** - a new user can register to our platform with email, password, username and optionally profile picture and real name.
- **Login** - user is able to login to access full functionaly of our platform.
- **User Skills** - user can make a list of their skills, stating category and name of the skill, proficiency level and experience.
- **Bucket Skills** - user can make a list of skills they wish to learn. They state notes, category and name of the skill.
- **Matches** - after creating a bucket list, user can see users that have the skills and are willing to teach it.
- **Contact** - every user can send a message to the admins of the platform.

### Contributions

Skillucket is a group project. The authors are: Sapir Shamai, Barak Shalom, Michael-Gage Runge, Mariana Dragomir and Róża Wadowska.

### FAQ

- How can users contact each other?
The feature of contact is still in development.

### Changes log

10.10.2023 - We are at the version 0.0.1.