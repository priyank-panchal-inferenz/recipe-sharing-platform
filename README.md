# Recipe Sharing Platform
## Description

This project is a Recipe Sharing Platform where users can create, share, and discover recipes. It provides REST APIs for managing recipes, user authentication, and various features to enhance the user experience.

## Features

1. **User Authentication**: User authentication and authorization are implemented to allow users to sign up, log in, and manage their recipes securely.

2. **Search and Filter**: Functionality is provided to search and filter recipes based on various criteria such as category, ingredients, and cooking time.

3. **Rating and Reviews**: Users can rate and review recipes, and average ratings are displayed for each recipe.

4. **CRUD Operations**: Users can perform CRUD operations (Create, Read, Update, Delete) on recipes they own.

## Installation

Follow these steps to set up the Recipe Sharing Platform:

1. **Clone the repository:**

2. **Install dependencies:**
    1. create virtual env for install lib
    - python -m venv env 
    2. install all dependecies 
    - pip install -r requirements.txt

3. **Set up the database:**
- The platform uses SQLite database.
- Run the following commands to initialize the database:
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

4. **Run the server:**
```
  python manage.py runserver
```


