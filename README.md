# Udacity FSND 5th Project: Item Catalogue

This is a project for the course `introduction to full-stack development`. 

Here, users can create, delete, edit and read posts, retrieve data via server-side web API, and login using account from Google and Facebook. 

This project is created for demonstration purposes. It is not open to contribution. However, users are free to clone and explore.

This project utilizes FLASK, SQLAlchemy, SQLite, Python, Jinja2, CSS3, Bootstrap, Javascript and JQuery.

---

## Table of Contents
* Dependences
* Prerequisites
* Installation
* Usage

## Dependencies
- Flask 0.11.0
- SQLAlchemy 1.1.4
- Jinja2 2.8
- httplib2 0.9.2
- oauth2client 4.0.0
- requests 2.2.1
- sqlite3 3.8.2

## Prerequisites
1. [Git](https://www.atlassian.com/git/tutorials/install-git)
2. [Vagrant](https://www.vagrantup.com/downloads.html) ([Virtual Box](https://www.virtualbox.org/) is required)

## Installation
### 1. Download Project Files

1. Navigate to a directory of choice
2. Download git repository
```
git clone https://github.com/hyungmogu/Udacity-Item-Catalogue-App/
```

### 2. Run Vagrant

1. Navigate to where `VagrantFile` is located
```
cd <FOLDER_CONTAINING_CLONED_REPO>/udacity-item-catalogue
```
2. Setup vagrant
```
vagrant up
```
3. Login
```
vagrant ssh
```

### 3. Install Dependencies
```
cd /vagrant/item-catalogue
python setup.py install
```

### 4. Setup OAuth for Login via Google

1. Go inside the project directory
```
cd item-catalogue
```
2. Obtain credential

   a. Go to https://console.developers.com/apis/credential
   
   b. Click `Create a Project`
   
   c. Click `Oauth Consent Screen`
   
   d. Save after entering the following information:

        - Product Name: Item Catalogue
        - Homepage URL: http://localhost:5000

   e. Click `Create Credentials`>`OAuth Client ID`
   
   f. Enter the following information after selecting `Web Application`:
 
        - Name: Item Catalogue
        - Authorized Javascript Origin: http://localhost:5000
        - Authorized Redirect URI: http://localhost:5000/welcome

   g. Click `Create` when done
   
   h. Click `Download JSON` 
   
   i. Save the file in `/vagrant/item_catalogue/item_catalogue` (or `<FOLDER_CONTAINING_CLONED_REPO>/udacity-item-catalogue/item_catalogue` outside vagrant)
   
   j. Change name to `g_credential.json`

3. Navigate to the directory containing `glogin.js`
```
cd static/js
```
4. Open and complete the file using information from step 2

### 5. Setup OAuth for Login via Facebook

1. Obtain credential:

   a. Go to https://developers.facebook.com/apps
   
   b. Click `Add New App`
   
   c. Fill in the inputs; click `Create App ID` when done
   
   d. Click `Dashboard` under the main menu
   
   e. Open `fb_credential.json` in `vagrant/item_catalogue/item_catalogue` 
   
   e. Copy `App ID` and `App Secret`; paste each in `app_id` and `app_secret`, respectively
   
   f. Save and quit
   
3. Navigate to directory containing `fblogin.js`
```
cd static/js
```
4. Open and complete the file using information from step 1

## Usages

### Viewing Demo
1. Navigate to `/vagrant/item_catalogue/item_catalogue`
2. Start Flask server
```
export FLASK_APP=run.py
flask run
```
3. Enter `http://localhost:5000/` in browser

### Accessing Web API
1. Enter `http://localhost:5000/catalogue.json` in browser


### Closing Server

1. Press `Ctrl` + `c` in window where local server is running
