
# Social Network

## Features

- Register/Login/Logout as a user.
- Search Friends based on email or username.
- Send/Accept/Reject Friend Request.
- List of Friends and Pending Friend Request.


Follow these steps to get the project up and running on your local machine:

## Installation
1. Clone or download this repository and open it in your editor of choice: 
```bash
git clone https://github.com/sachin-khatrani/social-network.git
```
2. Navigate to the project directory:
```bash
 cd social-network
 ``` 
3. To begin setting up this project, ensure that you have Python 3.10 installed on your computer. It's recommended to create a virtual environment to store your projects dependencies separately. You can install virtualenv by running the following command.
```bash
sudo apt install python3-venv
```
4. Create your new virtual environment as per python version:
```bash
python -m venv my-project-env
or
python3 -m venv my-project-env
```
The command above creates a directory with env package, which contains a copy of the Python binary, the Pip package manager, the standard Python library and other supporting files.

5. Activate the virtual environment:
```bash
source project-env/bin/activate.

for Windows
.\my-project-env\Scripts\activate
```
Once activated, the virtual environment’s bin directory will be added at the beginning of the $PATH variable. Also your shell’s prompt will change and it will show the name of the virtual environment you’re currently using. In our case that is
```bash 
(my-project-env) $
```
Now that the virtual environment is activated, we can start installing, upgrading, and removing packages using pip.

6. The first step is to install the module,using the Python package manager, pip:
```bash
pip -r install requirements.txt
```
Modify `social-network/config/setting.py` with database settings if you want to connect database other than default sqlite db.


7. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
8. Create a superuser :
```bash
python manage.py createsuperuser
```
9. To get start runserver localy by:
```bash
python manage.py runserver
```
Open up a browser and visit: http://127.0.0.1:8000/admin , then you will see the admin panel.
