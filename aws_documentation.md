# AWS Django Deployment with PostgreSQL

## 1. Set up an AWS EC2 instance:

- **Initialize**: Create a new EC2 instance.
- **OS**: Use an Ubuntu Server as the operating system.
- **Access**: Download the private key (`*.pem`) to SSH into the server.

## 2. Installing necessary packages:
Here we used the supervisor approach and choose to install postgres on our instance itself.

On your instance make sure to update, upgrade and install necessary packages:

- sudo apt-get update
- sudo apt-get upgrade
- sudo apt-get install python3-dev
- sudo apt-get install python3-pip
- sudo apt-get install python3-virtualenv
- sudo apt install python3.10-venv
- sudo apt-get install supervisor
- sudo apt-get install -y nginx
- sudo apt install postgresql
- sudo apt install postgresql-contrib
- sudo apt install libpq-dev


## 3. Setting up PostgreSQL:

- **Start**: Start the PostgreSQL server: sudo service postgresql start
- **Access**: Switch to the PostgreSQL user: sudo -u postgres psql

- **Configuration**: Create a database and a user for your Django project. Remember to replace `'dbname'`, `'your_username'`, and `'your_password'` with your actual details:

```sql
CREATE DATABASE dbname;
CREATE USER your_username WITH PASSWORD 'your_password';
ALTER ROLE your_username SET client_encoding TO 'utf8';
ALTER ROLE your_username SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE dbname TO your_username;  
```
- **Exit**: Exit PostgreSQL: \q

## 4.  Permissions in PostgreSQL:

- User Roles: By default, the 'root' user cannot interact with PostgreSQL. Therefore, use the 'ubuntu' or 'postgres' user for PostgreSQL-related tasks.
- Specific Roles: If necessary, you can grant specific roles or permissions using the PostgreSQL 'GRANT' command.

## 5. Clone The Project And Setup The Environment:

- On the instance start a new dir that will store the django project and the venv. (example: mkdir projects)
- Create and activate your virtual environment. (python3 -m venv venv) (python3 venv/bin/activate)
- Clone the project from GitHub. (git clone you_project_link_from_github)
- In 'project_v2' dir create .env file that contains all the secret credentials. (change the place of this file according to your project)
- Fill in the file according to the db credentials you just create on the instance (sudo nano .env)
```
export SECRET_KEY='sssssss33333333'  change
export DB_NAME='your db name'        change
export DB_USER='postgres'            change
export DB_PASSWORD='12345'           change
export DB_HOST='localhost'
export DB_PORT='5432'
```
- Run the requirements.txt file to install all the necessary libraries for the project (pip install -r requirements.txt)
- Ensure your Django settings.py is correctly configured with the ALLOWED_HOSTS and DATABASES settings

## 6. Setup Gunicorn And Nginx:
set up Gunicorn

- cd into /etc/supervisor/conf.d/
- sudo nano gunicorn.conf and update accordingly:
    ```
  [program:gunicorn]
  directory=/home/ubuntu/path_to_your_django_project
  environment=SECRET_KEY="djangoinsecuretke92vmf0wznpbqnoxd1wv9hqxnm7siyxi", DEBUG_SETTINGS=true
  command=/home/ubuntu/path_to_your_env/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/path_to_your_django_project/app.sock your_project_name.wsgi:application  
  autostart=true
  autorestart=true
  stderr_logfile=/var/log/gunicorn/gunicorn.err.log
  stdout_logfile=/var/log/gunicorn/gunicorn.out.log
    
  [group:guni]
  programs:gunicorn
  ```
- create a log dir (sudo mkdir /var/log/gunicorn)
- to read logs, sudo nano /var/log/gunicorn/gunicorn.err.log 

run the following commands to update supervisor # Done

- sudo supervisorctl reread
(if you have secret key errors, edit yours so it has only alphanumeric characters)
- sudo supervisorctl update
- sudo supervisorctl status ( check health)

set up Nginx by 

- cd into /etc/nginx/
- use who (or w) command to check the user 
- sudo nano nginx.conf and update user to (user from the second step for example: ubuntu)
- cd into /etc/nginx/sites-available/
- sudo nano nginx_app_name.conf and update:
```
    server{

	listen 80;
	server_name change_here_public_ip_address_from_aws;

	
	location / {

		include proxy_params;
		proxy_pass http://unix:/home/ubuntu/path_to_your_project/app.sock;

	}

}
```
- sudo nginx -t
- sudo ln nginx_app_name.conf /etc/nginx/sites-enabled (to link both entities)

run the following commands to update and restart nginx

- sudo service nginx restart
- sudo service nginx status

to check logs

- sudo tail -f /var/log/nginx/error.log
- sudo systemctl status nginx

## Congratulations 
now you're ready to visit your IP address and view your project:)

## Restart EC2
And one last extra thing if you don't have permanent IP address and you need to stop and restart your AWS instance, you will have to update few things(because you will get new IP address), so here is a list of steps to make sure you're not forgetting anything:

- Activate Virtual Environment. (source venv/bin/activate)
- Make the credentials file in you project visible. (source .env)
- Restart Gunicorn
```
sudo systemctl restart gunicorn
```
- sometimes you need to go to 'sudo nano /etc/supervisor/conf.d/gunicorn.conf' and change one char in the secretkey to make a change in the file
```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
```
- Update Nginx  configuration file: sudo nano nginx_app_name.conf (change to the new IP address)
```
sudo systemctl restart nginx
```
