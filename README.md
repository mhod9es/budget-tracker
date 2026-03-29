# Budget Tracker (Flask Web App)

A beginner-friendly web-based budget tracker built with **Python (Flask)**, **SQLite**, **HTML/CSS**, and **Chart.js**.

This application allows users to:

* Add income and expense transactions
* Edit and delete transactions
* View total income, expenses, and balance
* See a pie chart of expenses by category
* Get instant feedback with flash messages
* Enjoy a clean, color-coded UI



## Features

* Add, edit, and delete transactions
* Input validation (type, amount, date)
* Flash messages for success and errors
* Pre-filled date (today’s date)
* Color-coded income vs expense rows
* Pie chart of expenses by category (Chart.js)
* SQLite database (no setup required)



## Project Structure

```
budget-tracker/
  - app.py
  - budget.db (auto-created)
  - templates
    - index.html
    - edit.html
  - static
    - style.css
 ```
 


## Requirements

Make sure you have the following installed:

* Python 3.x
* pip (Python package manager)



## Setup Instructions

### 1. Create Project Folder

```bash
mkdir budget-tracker
cd budget-tracker
```



### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux

# OR (Windows)
venv\Scripts\activate
```



### 3. Install Dependencies

```bash
pip install flask
```



### 4. Add Project Files

Create the following structure:

```
budget-tracker/
  - app.py
  - budget.db (auto-created)
  - templates
    - index.html
    - edit.html
  - static
    - style.css
```

Copy and paste the provided code into each file.



### 5. Run the Application

```bash
python3 app.py
```



### 6. Open in Browser

Go to:

```
http://127.0.0.1:5000
```



## How to Use

1. Add a transaction (income or expense)
2. View totals and balance at the top
3. Edit or delete transactions as needed
4. View expense breakdown in the pie chart



## Technologies Used

* Python (Flask)
* SQLite
* HTML5 / CSS3
* Chart.js



## Future Improvements

* Filter by category or date
* Monthly reports
* CSV export/import
* User authentication



## Author
Micah Hodges
Created for FGCU Eaglehacks 2026

