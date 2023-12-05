# CSI3335 !!!

This repository contains the necessary instructions to launch our team's website for the CSI 3335 2023 Final Project.
These instructions assume that the database is already running and that the !!!.sql file has already been run.

## Description

This virtual environment contains essential Python libraries and frameworks required for the project. The `requirements.txt` file lists all the dependencies.

## Instructions


1. **Clone the Repository**:

```bash
git clone https://github.com/DotJARgon/-.git
cd -
```

2. **Create a Virtual Environment**

Make sure you are using python 3.11, 3.12 will not work

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

## Start the !!! Server

Make sure your python virtual environment is running, if it is not, make sure you are in
the project directory, and refer to step 3. of the **Instructions** section
1. **Creating the database**

Log into your mariadb instance and run the following:
```mysql
DROP DATABASE `!!!` IF EXISTS;
```
```mysql
CREATE DATABASE `!!!`;
```
2. Outside of your mariadb instance in the commandline, run the following to import
the database data (make sure to enter your database password when prompted):
```commandline
mysql -u root -p !!! < path/to/!!!.sql
```
## Default Admin Account

There is a default admin account already in the database that will have been loaded
in, however, if this will be deployed, we highly recommend going to the **Setting up a New Admin Account**
section. The user credentials are as follows.

username: Admin

password: csi3335rocks

## Start the !!! Backend!

1. In the directory of the project, run the following:
```bash
python -m flask run
```
Note that the virtual environment must be active.

2. Navigate to http://127.0.0.1:5000, the website should now be running!

## Deactivating the Virtual Environment

Run the following to deactivate the virtual environment

```bash
deactivate
```

## Setting up a New Admin Account
Make sure you are inside of the repository directory before following the instructions
below
1. **Create Admin**
```bash
python -m create_admin.py
```
You will be prompted to enter a username and password, and to repeat this password.
If your repeated password does not match the first password entered, the program will
terminate. If this happens, redo step 1. If both passwords are typed in
correctly, then you will be prompted to enter 'Y' to confirm. Anything else with 
terminate the program and you will have to redo step 1 to create the admin account. 
After entering 'Y',an admin account will be created with the entered username and password.
If you ever need to make a new admin account, simply rerun this section. It will delete
the previous admin and create a new one. Note that this will erase the previous admin's
query count information, so make sure you are positive you wish to recreate the admin
account. 
