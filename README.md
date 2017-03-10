# Udacity FSND 5th Project: Item Catalogue

---

## Introduction

This is a project for Udacity's "Introduction to Full-stack Development" course. The project utilizes FLASK, SQLAlchemy, SQLite, Python, Jinja2 and CSS3.

## Dependencies
- Flask 0.11.0
- SQLAlchemy 1.1.4
- Jinja2 2.8
- httplib2 0.9.2
- oauth2client 4.0.0
- requests 2.2.1
- sqlite3 3.8.2

## Getting Started
### Setting up

#### Installing Git

1. Follow the instruction provoided [here](https://www.atlassian.com/git/tutorials/install-git)

#### Installing Vagrant

1. Download and install [Virtual Box](https://www.virtualbox.org/)
2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
  - NOTE: Ubuntu is a [Debian-based operating system](https://en.wikipedia.org/wiki/Ubuntu_(operating_system)).
3. Boot into BIOS and enable virtual environment
  - NOTE: This step varies for different motherboard models and versions. Please refer to instruction provided by manufacturer for details.  

#### Downloading Project Files

1. Navigate to a directory of choice
2. Type `git clone https://github.com/hyungmogu/Udacity-Item-Catalogue-App/`; download the repository

#### Running Vagrant

1. Type `cd udacity-item-catalogue`; navigate to where `VagrantFile` is located
2. Type `vagrant up`; let vagrant to setup dependencies
3. Type `vagrant ssh`; login to the virtual machine

#### Installing Dependencies for Python

1. Type the following after loggin in:
```
cd /vagrant/item-catalogue
python setup.py install
```

#### Setting up OAuth for Google and Facebook Login

1. Type `cd item-catalogue`; go inside the project directory
2. Open `client_secret.json` and `fb_client_secret.json` using an editor of choice; follow instructions there
3. Type `cd static/js`; navigate to the directory containing OAuth Javascript SDKs.
4. Open `fblogin.js` and `glogin.js` using an editor of choice; fill in using information obtained from step 2.


### Running Flask Server

1. Type `cd ../../`; Go back to project root directory

2. Type the following:
```
export FLASK_APP=run.py
flask run
```

### Viewing Demo

1. Type `http://localhost:5000/` in browser

### Closing Server

1. Press `Ctrl` + `c` in window where local server is running
