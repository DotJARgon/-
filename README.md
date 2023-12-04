# CSI3335 !!!

This repository contains the necessary instructions to launch our team's website for the CSI 3335 2023 Final Project.
These instructions assume that the database is already running and that the !!!.sql file has already been run.
## Description

This virtual environment contains essential Python libraries and frameworks required for the project. The `requirements.txt` file lists all the dependencies.

## Instructions


1. **Clone the Repository**:

```bash
git clone https://github.com/DotJARgon/-.git
cd '-'
```

2. **Create a Virtual Environment**

**For Windows**
```bash
python -m venv venv
```
**For Linux/MacOs**
```bash
python3 -m venv venv

```
3. **Activate the Virtual Environment**

**For Windows**
```bash
.\venv\Scripts\activate
```
**For Linux/MacOs**
```bash
source venv/bin/activate
```

4. **Install the dependencies**
```bash
pip install -r requirements.txt
```

## Setup Admin Account
Make sure you are inside of the repository directory before following the instructions
below
1. **Create Admin**
```bash
python -m create_admin.py
```
You will be prompted to enter a username and password, and to repeat this password.
If your repeated password does not match the first password entered, the program will
terminate, rerun step 1. to create the admin account. If both passwords are typed in
correctly, then you will be prompted to enter 'Y' to confirm, anything else with 
terminate the program, rerun step 1. to create the admin account. After entering 'Y',
an admin account will be created with the entered username and password. If you
ever need to make a new admin account, then simply rerun this section, it will delete
the previous admin and create a new one. Note that this will erase the previous admin's
query count information, so make sure you are positive you wish to recreate the admin
account. 

## Start the !!! Server

Make sure your python virtual environment is running, if it is not, make sure you are in
the project directory, and refer to step 3. of the **Instructions** section. Now run 
the following:
```bash
python -m flask run
```
Now navigate to http://127.0.0.1:5000 , the website should now be running!

## Deactivating the Virtual Environment

Run the following to deactivate the virtual environment

```bash
deactivate
```
