# Automated Test Case Generator for Web Forms

A Flask-based system that parses HTML forms and automatically generates structured test cases including valid, invalid, boundary, negative, and combinatorial inputs. The tool improves testing quality, reduces manual QA effort, and ensures systematic validation of web forms.

## Overview
Web applications rely on form-based input, and validating this input is essential for ensuring robustness, security, and correctness. This project automates the entire form-testing process by converting an HTML form into a complete test-case suite. It extracts input fields, identifies validation constraints, and produces thorough test coverage.

## Abstract
This project builds an automated testing tool that takes any HTML form as input and generates comprehensive test cases such as valid, invalid, boundary, and security-focused inputs. The system uses BeautifulSoup for parsing and a Python-based generator for creating test scenarios. The project demonstrates key software engineering principles, with a focus on performance, reliability, usability, and maintainability.

## Features
### HTML Parsing
- Detects all input field types  
- Reads constraints like required, minlength, maxlength, min, max, pattern  
- Extracts select options, checkbox and radio values  

### Test Case Generation
- Baseline valid test case  
- One-field-at-a-time negative tests  
- Boundary value analysis  
- Invalid format tests  
- Security test cases (SQL injection, XSS payloads)  
- Combinatorial test cases (pairwise-style, capped for performance)

### UI / UX
- Web interface built with HTML, CSS, and JavaScript  
- Paste HTML form directly  
- View JSON test-case output instantly  

### Maintainable Codebase
- Parser, generator, and interface are modular  
- Easy to extend with new rules  

---

## High-Level Architecture (PlantUML)
