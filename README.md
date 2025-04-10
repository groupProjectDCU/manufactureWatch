## Project Overview

**Name:** Factory Machinery Status & Repair Tracking System  
**Purpose:** A web application (Django + Docker) that allows ACME Manufacturing Corp. to track machine statuses, manage faults and repairs, and generate management reports.

### Key Technologies
- **Python 3.11 (Django framework)**
- **Docker & Docker Compose**
- **PostgreSQL** (configurable using `dj-database-url`)
- **HTML/CSS + JavaScript** (front-end)
- **GitHub Issues & Projects** (task management)

---

## Set Up Options

We provide two setup options:

1. **Docker Setup (Recommended)**: The easiest way to get started with proper PostgreSQL configuration.
2. **Local Setup (Optional)**: Requires manual PostgreSQL setup and configuration.

We strongly recommend using the Docker setup for development to ensure consistent database configuration.

---

### Environment Variables
Before running the app, create a file named .env to define environment variables:
```
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=mydatabase
DB_HOST=db
DB_PORT=5432
```
alternatively, you can use the .env.example file as a template and modify the values as needed.
``` bash
cp .env.example .env
```
**Note: The .env file is needed for not only the docker setup but also the local setup.**

## Set Up Option 1: Docker Usage (Recommended)
We provide a Dockerfile and a docker-compose.yml that can build and run the website. This setup allows you to configure the SQL database at runtime using environment variables (e.g., DATABASE_URL or POSTGRES_USER, POSTGRES_PASSWORD, etc.), and automatically applies SQL migrations when the container starts. You may also mount a Docker volume for persistent file storage. The website will be fully operational even with a fresh blank database.

### 1. **Install Docker**
Download docker desktop  [here](https://www.docker.com/products/docker-desktop/) to install Docker.

### 2. **Build & Run with Docker Compose**
`docker-compose.yml` file defines the services for the web app and the database. There are currently 2 services:
- **web**: Django application, connects to the database via the environment variables.
- **db**: PostgreSQL database

To build and run the containers, run the following commands:
``` bash
docker compose build # pull and build the necessary images
docker compose up # start the web (Django) and db (Postgres) containers
```

After running the containers, you can check the app by going to http://localhost:8000.
Django will run **migrations** automatically on container startup, so you don't need any manual steps for an empty database.

To stop the containers, run the following command:
``` bash
docker compose down
```

### 3. **Creating Migration Files**
If you make changes to the models, you need to create migration files:
```bash
# If running locally:
python manage.py makemigrations
    
# Or if using Docker:
docker compose run --rm web python manage.py makemigrations
```
These migration files should be committed to your repository.
The Docker setup will automatically apply migrations on startup, but won't create them.

### 3. **Loading Test Data and Development**:
You can include test data in your migrations or provide fixtures.
#### Using the Provided Test Data
We've created comprehensive test data fixtures for all models in the system. To load this test data:

Run the custom management command:
```bash
docker compose run web python manage.py load_test_data
```
This will load test users with different roles (managers, technicians, repair staff), sample machinery, collections, warnings, and fault cases with notes. It will also automatically reset all test user passwords to match the documentation.

The test data includes:
- 9 users with different roles
- 3 machines with different statuses
- 3 collections with machine assignments
- 2 warnings (1 active, 1 resolved)
- 2 fault cases (1 open, 1 resolved)
- 4 fault notes

**Note:** All test users will have the password "password123" after loading the test data. This is handled automatically by the `load_test_data` command.

Visit http://localhost:8000/admin to see the test data.

### 4. **Persistent Storage**:
The docker-compose.yml defines a volume for PostgreSQL data (pgdata:/var/lib/postgresql/data) to persist your database across container restarts.
If your app requires file uploads, you can also map a volume for file storage (e.g., media/ folder).

### 5. **Manual One-Container Approach**:
You can run single container manually using docker compose as well.
To start database, run the following command:
``` bash
docker compose up -d db
```
To start the web app, run the following command:
``` bash
docker compose up -d web
```
To start the web app with database url, run the following command:
``` bash
docker compose run -e DATABASE_URL=postgresql://myuser:mysecretpassword@db:5432/mydatabase web
```
Note: the database url has the format:
```bash
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
```

## Set Up Option 2: Local Setup

1. **Clone the Repository**  
   ```bash
   git clone git@github.com:groupProjectDCU/manufactureWatch.git
   cd manufactureWatch
   ```

2. **Create a Virtual Environment**  (recommended)
    ```bash
    # option1: using venv
    python -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate

    # option2: using conda
    conda create -n manufactureWatch python=3.11
    conda activate manufactureWatch
    ```

3. **Install Postgres**
    - Windows: 
      - Download installer from postgresql.org
    - macOS: 
      - ````brew install postgresql````
    - Linux: 
      - ````apt install postgresql postgresql-contrib````


4. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5. **Set Up Database**
    ```bash
    # Install PostgreSQL (if not already installed)
    # For Ubuntu/Debian:
    # sudo apt install postgresql
    # For macOS with Homebrew:
    # brew install postgresql
    
    # Create a PostgreSQL database
    createdb mydatabase
    
    # Configure database settings in .env file
    echo "DATABASE_URL=postgresql://myuser:mysecretpassword@localhost:5432/mydatabase" > .env
    # Or set individual variables:
    # echo "POSTGRES_DB=mydatabase" > .env
    # echo "POSTGRES_USER=myuser" >> .env
    # echo "POSTGRES_PASSWORD=mypassword" >> .env
    # echo "DB_HOST=localhost" >> .env
    # echo "DB_PORT=5432" >> .env

    # Generate migration files from your models when you make changes to the models
    python manage.py makemigrations
    
    # Apply migrations to create the database schema
    python manage.py migrate
    ```

6. **Run Development Server**
    ```bash
    python manage.py runserver
    ```
    visit http://127.0.0.1:8000/ to see the app.

---

## Django Project Apps Structure
    
Each app in Django serves a specific concern in your application:

- **core**
    - Contains shared functionality, base templates, and utilities used throughout the project.

- **accounts**
    - Handles user authentication, permissions, and user profiles for your different roles (Managers, Technicians, Repair personnel, View-only users).

- **machinery**
    - Manages all machinery-related data: machine details, status tracking, collections, and assignments.

- **repairs**
    - Contains the fault case management system, including fault entries, images, and repair history.

- **dashboard**
    - Handles visualization, reporting, and data presentation for different user roles.

------------------------------------------

## Start

Database Schema  [in progress] 
In order to contruct back-end properly, we need a proper database schema.
The code can be found in `database.sql`.
Based on that, you'll create models. One table - one Django model.
Diagrams:


1) ![Imgur](https://imgur.com/f9IaWjw.png)


2) ![img](https://imgur.com/R6PA4hx.png)

## Main page

To run app, use ``python manage.py runserver``. Click on the localhost url.
When you enter you app, you'll see the entry/main page:

![img](https://imgur.com/OstTlLQ.png)

This view comes from ``core`` directory. ``Core`` directory is our main directory.

