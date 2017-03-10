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

### 1. Installing Git

- Follow the instruction provoided [here](https://www.atlassian.com/git/tutorials/install-git)

### 2. Installing Vagrant

1. Download and install [Virtual Box](https://www.virtualbox.org/)
2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
  - NOTE: Ubuntu is a [Debian-based operating system](https://en.wikipedia.org/wiki/Ubuntu_(operating_system)).
3. Boot into BIOS and enable virtual environment
  - NOTE: This step varies for different motherboard models and versions. Please refer to instruction provided by manufacturer for details.  

### 3. Downloading Project Files

1. Navigate to a directory of choice
2. Type `git clone https://github.com/hyungmogu/Udacity-Item-Catalogue-App/`; download the repository

### 4. Running Vagrant

1. Type `cd udacity-item-catalogue`; navigate to where `VagrantFile` is located
2. Type `vagrant up`; let vagrant to setup dependencies
3. Type `vagrant ssh` when step 4 is finished; login to the virtual machine

### 5. Installing Dependencies for Python
- Type the following commands after loggin in:
```
cd /vagrant/item-catalogue
python setup.py install
```

### 5. Running Flask Server
- Type the following after installing dependencies:
```
cd item-catalogue
export FLASK_APP=run.py
flask run
```

### 6. Viewing Content

1. Type `http://localhost:5000/` in browser

### 7. Closing Server

1. Press `Ctrl` + `c` in window where local server is running
