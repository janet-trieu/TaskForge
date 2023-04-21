COMP3900 Capstone Project 2023 Term 1
Tutorial: W16C Team CompGPT
Project: TaskForge - Task Management System

Member Details:
Dabin Haam     z5258354 (Scrum Master)
Francis Nguyen z5316596
Joseph Saad    z5309442
Janet Trieu    z5320262
Vincent Do     z5207667

**Required Credentials**:
 - Google Firebase:
 - Username: compgpt3900@gmail.com
 - Password: 2023t1w16ccompgpt

**Setup Instructions**:
Our system is intended to run using the **VM** option, not the CSE computers.

**To setup the system in the Lubuntu VM, do the following steps in the terminal:**

Install nvm and nodejs.
- Run “wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash”.
- Close and reopen the terminal.
- Run “nvm install node”.

Install pip.
- Run “sudo apt update”.
- Run “sudo apt install python3-pip”.

Clone the git repository.

Install backend requirements.
- Navigate to the “backend” folder in the repo.
- Run “pip install -r requirements.txt”.

Install frontend requirements.
- Navigate to the “frontend” folder in the repo.
- Run “npm install”.

**To run the system, do the following steps:**

Open 2 terminal instances.

In one terminal, run the backend server.
- Navigate to the “backend” folder in the repo.
- Run “python3 main.py”.

In the second terminal, run the frontend server.
- Navigate to the “frontend” folder in the repo.
- Run “npm run dev”.

Open “http://localhost:5173” in a browser.
