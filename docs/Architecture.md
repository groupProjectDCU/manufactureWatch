# Architecture

## 1. High-Level Overview
The Factory Machinery Status & Repair Tracking System is designed to help ACME Manufacturing Corp. monitor machine statuses and manage repair workflows. The core goal is to provide a centralized web platform where managers, technicians, and repair personnel can:
- View machinery statuses (OK, Warning, Fault).
- Create and update fault cases (with notes, images).
- Assign roles and track responsibilities.
- Generate and review historical repair logs.

From a technology standpoint, the system is built with Django (Python framework) on the backend and leverages Docker + Docker Compose to simplify deployment. A PostgreSQL database stores all operational data. This ensures seamless environment configuration, automatic migrations, and an environment-variable–driven connection to the database at runtime.

## 2. System Architecture

### 2.1 Components & Layers
Presentation Layer (Front-End)
- Django Templates for rendering HTML/CSS/JavaScript.
- Dynamic pages show machine lists, fault details, user dashboards.
- Role-based interface elements (e.g., manager sees a different dashboard than a technician).

Application Layer (Django)
- Views & Models:
- The Machine, FaultCase, Warning models encapsulate the system’s data and logic.
- Views handle requests, checking user roles (Manager, Technician, Repair) for permissions.
- Authentication & Authorization:
- Django’s built-in auth system manages user credentials.
- Each role sees only the features and data relevant to their responsibilities.

Data Layer (PostgreSQL)
- Default connection established via environment variables (POSTGRES_USER, POSTGRES_PASSWORD, DATABASE_URL), parsed by dj-database-url.
- Stores all records for machinery, fault logs, user info, etc.
- Automatic migrations run at container startup, ensuring a fresh blank DB is initialized if needed.

Docker & Orchestration
- Dockerfile: Defines how to build the image (Python installation, copying project files, etc.).
- docker-compose.yml: Spins up two containers—web (Django) and db (Postgres)—and links them via a Docker network.
- Entrypoint: A script that runs migrations and starts Django automatically on container launch.

### 2.2 Architecture Diagram (Conceptual)
                 +------------------------------+
                 |    Web Browser (Users)      |
                 |  (Managers/Technicians/etc) |
                 +--------------+--------------+
                                |  HTTP/HTTPS
                                v
        +---------------------------------------------------+
        |               Django Application (web)            |
        |---------------------------------------------------|
        |  - Views/URLs (manages front-end templates)       |
        |  - Role-based logic (Manager, Technician, Repair) |
        |  - REST endpoints for external systems            |
        |  - Models & Business logic                       |
        |---------------------------------------------------|
        |  Docker Container orchestrated by docker-compose |
        +----------------------+----------------------------+
                               | (Docker network)
                               v
        +---------------------------------------------------+
        |       PostgreSQL Database (db) Container          |
        |---------------------------------------------------|
        |  - Tables for Machinery, FaultCase, Warning, etc. |
        |  - Uses environment vars for credentials          |
        |  - Automatic migrations on container startup      |
        +---------------------------------------------------+

## 3. Data Flow

### 3.1 Internal User Workflow
	1.	User Login
- A user (Manager/Technician/Repair) logs into the Django web interface.
- Django validates credentials and session.
	2.	Viewing Machine Statuses
- The user sees a list of machines. Statuses are fetched from the database (OK, Warning, or Fault).
- If any warnings are active, the system marks the machine as “Warning.” If a fault case is open, it appears as “Fault.”
	3.	Creating a Fault Case (Technician)
- A Technician noticing a breakdown creates a new fault case via a form.
- Data is sent to a Django view, which creates a new FaultCase record in the database.
	4.	Updating Faults (Repair Personnel)
- Repair staff see fault cases assigned to them.
- They add notes/images or mark them as resolved, which updates the FaultCase record and changes the machine’s status to “OK” once fully repaired.
	5.	Manager Oversight
- Managers see aggregated dashboards of all machines (filter by building, assigned staff, etc.).
- They can add new machines, delete old ones, assign technicians, or generate reports.

### 3.2 External Integration Workflow (Optional)
	1.	External System
- An external monitoring sensor or system detects an anomaly and sends a JSON POST request to /api/machines/<id>/faults/ or a generic endpoint.
    2.	REST Endpoint
- The Django view authenticates the request, logs a new warning/fault in the database.
- If a new fault is created, it triggers notifications or updates the manager dashboard.

### 4. API Endpoints

Note: If using Django REST Framework or custom JSON views, these endpoints might differ slightly. Below is an example structure.
### 4.1.  Machines
- GET /api/machines/
    - Description: Returns a list of all machines, their status, assigned users, etc.
    - Permissions: Any authenticated user can see machine statuses.
- POST /api/machines/
    - Description: Create a new machine entry (Manager role only).
    - Body (JSON):
```
{
  "name": "Machine A",
  "location": "Building 1",
  "importance": 5
}
```
    - Permissions: Manager only.

### 4.2. Fault Cases
- GET /api/machines/<machine_id>/faults/
    - Description: List all fault cases for a given machine.
    - Permissions: Manager/Technician/Repair.
- POST /api/machines/<machine_id>/faults/
    - Description: Create a new fault case for the specified machine (Technician role or external system).
    - Body (JSON):
    ```
{
  "description": "Machine is overheating",
  "severity": "High"
}
    ```
    - Permissions: Technician or external system token.
- PATCH /api/faults/<fault_id>/resolve/
    - Description: Marks a fault as resolved, changing the machine status back to “OK.”
    - Permissions: Repair role or Manager.

### 4.3. Warnings
- POST /api/machines/<machine_id>/warnings/
    - Description: Adds a warning string to the machine’s active warnings.
    - Permissions: Technician role or external system.
- DELETE /api/machines/<machine_id>/warnings/<warning_id>/
    - Description: Removes a specified warning.
    - Permissions: Repair or Technician role.

### 4.4. Auth / Login
- POST /api/login/ or POST /auth/token/
    - Description: Obtain authentication token or session to access subsequent endpoints.
    - Permissions: Public endpoint for user login, though valid credentials are required.

## 5. Security Considerations

### 5.1. Authentication
- Django’s built-in auth system handles user credentials.
- API endpoints require valid tokens for authentication.

### 5.2. Authorization
- Each role has specific permissions:
    - Managers can view all machines, add/delete machines, assign technicians.
    - Technicians can view assigned machines, create/update fault cases.
    - Repair staff can view assigned fault cases, mark them as resolved.


