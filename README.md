# Restaurant Management System
## Overview
- This project is a command-line based Restaurant Management System developed using Python and MySQL. It is designed to manage basic restaurant operations such as menu handling, order processing, and billing. The system demonstrates fundamental concepts of database integration, structured programming, and user interaction.
---
## Features
- Add, view, update, and delete menu items
- Place and manage customer orders
- Display all orders with calculated totals
- Generate total bill per customer and table
- Automatic database and table creation
---
## Technologies Used
- Python 3
- MySQL
- mysql-connector-python
---
## Database Structure
### Menu Table
- MenuID (Primary Key)
- Name
- Description
- Price
### Orders Table
- OrderID (Primary Key)
- CustomerName
- TableNumber
- MenuID (Foreign Key)
- Quantity
---
## How to Run
1. Install Python (>=3.x)
2. Install MySQL and start the server
3. Install required package:
   pip install mysql-connector-python
