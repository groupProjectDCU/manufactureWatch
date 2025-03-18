
## Project Overview

**Name:** Factory Machinery Status & Repair Tracking System  
**Purpose:** A web application (Django + Docker) that allows ACME Manufacturing Corp. to track machine statuses, manage faults and repairs, and generate management reports.

### Key Technologies
- **Python 3.11 (Django framework)**
- **Docker & Docker Compose**
- **SQLite** (configurable using `dj-database-url`)
- **HTML/CSS + JavaScript** (front-end)
- **GitHub Issues & Projects** (task management)

---

## Set Up Option 1: Local Setup

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

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Database**
    ```bash
    python manage.py migrate
    ```

5. **Run Development Server**
    ```bash
    python manage.py runserver
    ```
    visit http://127.0.0.1:8000/ to see the app.

---

## Set Up Option 2: Docker Usage (Recommended)
We provide a Dockerfile and a docker-compose.yml that can build and run the website. This setup allows you to configure the SQL database at runtime using environment variables (e.g., DATABASE_URL or POSTGRES_USER, POSTGRES_PASSWORD, etc.), and automatically applies SQL migrations when the container starts. You may also mount a Docker volume for persistent file storage. The website will be fully operational even with a fresh blank database.

1. Build & Run with Docker Compose
    1. Create/Update .env (if needed)
- In the project root, you can create a file named .env to define environment variables like:
```
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=mydatabase
DB_HOST=db
DB_PORT=5432
```
alternatively, you can use the .env.example file as a template and modify the values as needed.
```
cp .env.example .env
```

    2. Build & Start
```
docker compose build
docker compose up
```
    - docker compose build pulls and builds the necessary images.
    - docker compose up starts the web (Django) and db (Postgres) containers.

    3. Check the App
    - Once containers start, go to http://localhost:8000.
    - Django will run migrations automatically on container startup, so you don’t need any manual steps for an empty database.
    4. Stop the Containers
```
docker compose down
```

2. Loading Test Data
    - You can include test data in your migrations or provide fixtures.
    - If you have a fixture like initial_data.json, you can modify the entrypoint.sh (or a similar startup script) to run:
```
python manage.py loaddata initial_data.json
```

3. Persistent Storage
    - The docker-compose.yml defines a volume for PostgreSQL data (pgdata:/var/lib/postgresql/data) to persist your database across container restarts.
    - If your app requires file uploads, you can also map a volume for file storage (e.g., media/ folder).

4. Manual One-Container Approach
    - If you prefer to run a single container (without Compose), you can still build and run it manually:
```
# Build the image
docker build -t your_image_name .

# Run the container, specifying environment variables as needed
docker run -p 8000:8000 \
  -e DATABASE_URL="postgres://myuser:mysecretpassword@host:5432/mydatabase" \
  your_image_name
```

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

- **api**
    - Provides REST API endpoints for:
        - External monitoring systems to report warnings/faults
        - Machine status viewing
        - Fault case management

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

## Machines page

All machines would be here, ```/machinery```.

![img](https://i.imgur.com/sgu0NJy.png)

To access a particular machine: ````/machinery/machine1````
