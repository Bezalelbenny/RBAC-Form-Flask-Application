Flask Role-Based Access Control (RBAC) Task Management System
-----------------------------------------------------------------------------------------------------------------------------
Overview
-----------------------------------------------------------------------------------------------------------------------------
This project is a web-based Task Management System developed using Flask that demonstrates the implementation of Role-Based Access Control (RBAC). Users are assigned one of three roles—Admin, Editor, or Viewer—each with different permissions for interacting with tasks. The application uses Flask-WTF for form handling, SQLAlchemy as the ORM, and SQLite as the database.

The project highlights authentication, authorization, session management, and CRUD operations while maintaining a clean and responsive user interface.
-----------------------------------------------------------------------------------------------------------------------------
Features
-----------------------------------------------------------------------------------------------------------------------------
User Authentication (Login & Logout)
Role-Based Access Control (RBAC)
Session Management
Create, Read, Update and Delete (CRUD) Operations
SQLite Database Integration
SQLAlchemy ORM
Flask-WTF Form Validation
Responsive User Interface
Preloaded User Accounts
Automatic Database Initialization
Permission-Based Navigation
Secure Route Protection
Sample Tasks Loaded Automatically
-----------------------------------------------------------------------------------------------------------------------------
User Roles
-----------------------------------------------------------------------------------------------------------------------------
Role	Permissions
Admin	View, Create, Edit, Delete Tasks
Editor	View, Create, Edit Tasks
Viewer	View Tasks Only
-----------------------------------------------------------------------------------------------------------------------------
Default Login Credentials
-----------------------------------------------------------------------------------------------------------------------------
Username	Password	Role
admin	admin123:Admin
editor	editor123:Editor
viewer	viewer123:Viewer
-----------------------------------------------------------------------------------------------------------------------------


