<h1>Django Project Apps Structure</h1>
    
<p>Each app in Django serves a specific concern in your application:</p>

<h2>core</h2>
<p>Contains shared functionality, base templates, and utilities used throughout the project.</p>

<h2>accounts</h2>
<p>Handles user authentication, permissions, and user profiles for your different roles (Managers, Technicians, Repair personnel, View-only users).</p>

<h2>machinery</h2>
<p>Manages all machinery-related data: machine details, status tracking, collections, and assignments.</p>

<h2>repairs</h2>
<p>Contains the fault case management system, including fault entries, images, and repair history.</p>

<h2>api</h2>
<p>Provides REST API endpoints for:</p>
<ul>
    <li>External monitoring systems to report warnings/faults</li>
    <li>Machine status viewing</li>
    <li>Fault case management</li>
</ul>

<h2>dashboard</h2>
<p>Handles visualization, reporting, and data presentation for different user roles.</p>

------------------------------------------

<h1>Start</h1>

<h2> Database Schema  [in progress] </h2>
In order to contruct back-end properly, we need a proper database schema.
The code can be found in <code>database.sql</code>.
Based on that, you'll create models. One table - one Django model.
Diagrams:


1) ![Imgur](https://imgur.com/f9IaWjw.png)


2) ![img](https://imgur.com/R6PA4hx.png)

<h2>Main page</h2>

To run app, use ``python manage.py runserver``. Click on the localhost url.
When you enter you app, you'll see the entry/main page:

![img](https://imgur.com/OstTlLQ.png)

This view comes from ``core`` directory. ``Core`` directory is our main directory.

<h2>Machines page</h2>

All machines would be here, ```/machinery```.

![img](https://i.imgur.com/sgu0NJy.png)

To access a particular machine: ````/machinery/machine1````

<h1>Migrations</h1>

````python manage.py migrate````



