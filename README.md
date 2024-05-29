---
title: aspireit-flask-backend
author: Shantanu Badmanji
email: shantanubadmanji1912@gmail.com
phone: "+91 8080546956"
linkedin: https://www.linkedin.com/in/shantanu-badmanji/
github: https://github.com/ShantanuBadmanji/
---

# Aspireit-Flask-Backend

## Project Overview

This project is a Flask-based backend application that implements a RESTful API and integrates with MongoDB for data storage. It also incorporates a machine learning model for sentiment analysis and a React-based frontend for user interaction.

## Features

1. **API Endpoints**:

- `/register` (POST): Register a new user.
- `/login` (POST): User login.
- `/profile` (GET, PUT): Retrieve and update the user profile.
- `/uploads/` (POST): Store files on the server's "/uploads/" folder.
- `/uploads/:filename` (GET): Retrieve files from the server's "/uploads/" folder.
- `/uploads-mongodb/` (POST, GET): Upload a file and retrieve the uploaded file list of the authenticated user from the MongoDB database.
- `/uploads-mongodb/:filename` (GET): Retrieve a specified file of the authenticated user from the MongoDB database.
- `/analyze` (POST): Send text data for sentiment analysis using a pre-trained model from HuggingFace.

2. **Database Integration**:

- MongoDB is used as the database, and Pymongo is utilized for communication.
- The application can store various types of buffer objects, such as audio, video, PDFs, PPTs, etc., with a maximum size of 16MB.

3. **User Authentication and Authorization**:

- JSON Web Tokens (JWT) are implemented for user authentication.
- Secured endpoints ensure that only authenticated users can access them.

4. **Machine Learning Integration**:

- A pre-trained sentiment analysis model from HuggingFace is integrated into the application using joblib.

5. **Security Measures**:

- Input validation is implemented using Marshmallow.
- Password hashing is implemented using bcrypt.
- Protection against common web vulnerabilities (e.g., SQL injection, XSS) is implemented.

6. **Frontend Presentation**:

- A React.js-based frontend application is developed using Bootstrap.
- User interfaces are provided for user registration, login, profile management, text analysis, and file management for logged-in users.
- The frontend can successfully communicate with the backend API, displaying data and results appropriately.

## Installation

1. Fork this repository to your GitHub account.
2. Clone the forked repository and follow the steps below:

### Backend Setup

- The dir size increases to 6Gb due to the dependencies to huggingface model.

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python run.py
```

### Setup Evironment Variables

- Refer ".env.sample" file

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

### ML Model setup

```bash
source env/bin/activate
python download_model.py
```

this will dump the model in ml-model/ dir (~350MB)

### Start the Backend server and frontend server

#### flask server

```bash
source env/bin/activate
python run.py
```

#### client server

```bash
cd client
npm run dev
```

## MY Info

**Name:** Shantanu Badmanji  
**Phone:** +91 8080546956  
**Email:** [shantanubadmanji1912@gmail.com](mailto:shantanubadmanji1912@gmail.com)  
**LinkedIn:** [linkedin.com/in/shantanu-badmanji/](https://www.linkedin.com/in/shantanu-badmanji/)  
**GitHub:** [github.com/ShantanuBadmanji/](https://github.com/ShantanuBadmanji/)
