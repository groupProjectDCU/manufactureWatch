
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

## Local Setup

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

## Docker Usage (optional)
If you prefer using Docker for local development:

```
# Build the image
docker build -t your_image_name .

# Run the container
docker run -p 8000:8000 -e DB_URL=your_database_url your_image_name
```

---

## Django Project Apps Structure
    
Each app in Django serves a specific concern in your application:

- **Core**
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
