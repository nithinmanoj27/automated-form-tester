# Automated Test Case Generator for Web Forms

This project automatically parses any HTML form and generates valid, invalid, boundary, and combinatorial test cases based on field constraints. The output is returned in structured JSON format.

---

## Overview

The system takes HTML form input from the user, extracts field metadata, and produces a complete test suite.  
It helps developers test form validation logic without manually writing test cases.

---

## Tech Stack

- Python (Flask)
- HTML, CSS, JavaScript
- BeautifulSoup (lxml)
- JSON Output

---

## Project Structure

automated-form-tester/
│── app.py
│── templates/
│ └── index.html
│── static/
│ ├── main.js
│ ├── style.css
│ └── sample_hint.txt
│── examples/
│ └── sample_form.html
│── requirements.txt
│── README.md



---

## Features

- Parses HTML forms automatically  
- Extracts field types and constraints  
- Generates valid inputs  
- Generates invalid and boundary inputs  
- Generates combinatorial test cases  
- Displays results as formatted JSON in the browser  

---

## How It Works

1. **User pastes HTML form** into the UI.
2. The frontend sends it to `/generate`.
3. Backend parses form using BeautifulSoup.
4. Valid/invalid/boundary values are created.
5. A full test suite is generated and returned.

---

## How to Run

python -m venv venv
venv\Scripts\activate # Windows
pip install -r requirements.txt
python app.py



Then open:
http://127.0.0.1:5000/


---

## Example Output Format

```json
{
  "fields": [
    // Array of field metadata objects
  ],
  "test_cases": [
    // Array of generated test case objects
  ]
}

---

## Contributors

- **Nithin Manoj** – Backend logic, parser, test generation  
- **Suresh** – User interface, testing, documentation  

---

