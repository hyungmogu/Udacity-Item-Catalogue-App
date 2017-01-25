# Udacity-Item-Catalogue-App

---

## Introduction

This is a project for Udacity's "Introduction to Full-stack Development" course. The project utilizes FLASK, SQLAlchemy, SQLite, Python, Jinja2 and CSS3.

## Step-by-step Instruction

### 1. Downloading File

#### Windows

1. Install [git bash](https://git-scm.com/downloads) 
2. Open git bash
3. Navigate to a directory of choice
4. Type `git clone https://github.com/hyungmogu/Udacity-Item-Catalogue-App/`; clone the repository

#### Linux/MacOS

1. Open terminal
2. Navigate to a directory of choice
3. Type `git clone https://github.com/hyungmogu/Udacity-Item-Catalogue-App/`; clone the repository

### 2. Installing Vagrant

#### Windows, Linux and Mac OS

1. Download and install [Virtual Box](https://www.virtualbox.org/)
2. Download and install [Vagrant](https://www.vagrantup.com/downloads.html)
  - NOTE: Ubuntu is a [Debian-based operating system](https://en.wikipedia.org/wiki/Ubuntu_(operating_system)).
3. Boot into BIOS and enable virtual environment
  - NOTE: This step varies for different motherboard models and versions. Please refer to instruction provided by manufacturer for details.  

### 3. Running Vagrant

#### Windows

1. 

#### Linux, Mac OS

### 4. Running Flask Server (In Vagrant)

1. Type `cd /vagrant/Item\ Catalogue` after logging in
2. Type `export FLASK_APP=web_server.py` once inside
3. Type `flask run`

### 5. Viewing Content
1. Type `http://localhost:5000/` in browser

### 6. Closing Server

#### Windows
1. Press `Ctrl` + `c` in virtual machine where local server is running

#### Linux, Mac OS
1. Press `Ctrl` + `c` in terminal where local server is running
