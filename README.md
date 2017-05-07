# Udacity FSND 5th Project: Item Catalogue

This is a project for the course `introduction to full-stack development`.

Here, users can create, delete, edit and read posts, retrieve data via server-side web API, and login using account from Google and Facebook.

This project is for demonstration purposes. It is not open to contribution. However, users are free to clone and explore.

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
git clone https://github.com/hyungmogu/udacity-item-catalogue/
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
cd /vagrant/item_catalogue
sudo python setup.py install
```

### 4. Setup Google OAuth

1. Download credential

   a. Go to https://console.developers.google.com/apis/credentials

   b. Click `Create a Project`

   c. Click `Credentials`>`Oauth Consent Screen`

   d. Save after entering the following:

        - Product Name: Item Catalogue
        - Homepage URL: http://localhost:5000

   e. Click `Create Credentials`>`OAuth Client ID`

   f. Enter the following after selecting `Web Application`:

        - Name: Item Catalogue
        - Authorized Javascript Origins: http://localhost:5000
        - Authorized Redirect URIs: http://localhost:5000/welcome

   g. Click `Create` when done

   h. Click `Item Catalogue`

   i. Click `Download JSON`

   j. Save the file in `/vagrant/item_catalogue/item_catalogue` (or `<FOLDER_CONTAINING_CLONED_REPO>/udacity-item_catalogue/item_catalogue` outside vagrant)

   k. Change name to `g_credential.json`

3. Navigate to `glogin.js`
```
cd /vagrant/item_catalogue/item_catalogue/static/js
```
4. Open and fill in missing information using the file from step 1

### 5. Setup Facebook OAuth

1. Obtain credential:

   a. Open `fb_credential.json` in `vagrant/item_catalogue/item_catalogue`

   b. Go to https://developers.facebook.com/apps

   c. Click `Add New App`

   d. Fill in the form, and click `Create App ID` when done

   e. Click `Dashboard` under the main menu

   f. Copy `App ID` and `App Secret`; paste each to `app_id` and `app_secret` in `fb_credential.json`, respectively

   g. Save and quit

2. Navigate to `fblogin.js`
```
cd /vagrant/item_catalogue/item_catalogue/static/js
```
3. Open and fill in missing information using the file from step 1

### 6. Setup Secret Key

1. Navigate to `run.py`
```
cd /vagrant/item_catalogue/item_catalogue
```

2. Open file, and replace the value in `app.secret_key` with lengthy and random combinations of characters

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
1. Enter `http://localhost:5000/catalog.json` to view all items
2. Enter `http://localhost:5000/catalog.json/<category_slug>` to view all items in the selected category
3. Enter `http://localhost:5000/catalog.json/<category_slug>/<item_slug>` to view the selected item

### Closing Server

1. Press `Ctrl` + `c` in window where local server is running
