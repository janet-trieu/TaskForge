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

**Prerequisites:**
 - Python version >= 3.10.x, refer https://www.python.org/downloads/
 - Latest version of Nodejs, refer https://nodejs.org/en/download

**Backend Setup:**
 - cd ~/capstone-project-3900w16ccompgpt/backend
 - pip install -r requirements.txt

**Frontend Setup:**
 - cd ~/capstone-project-3900w16ccompgpt/frontend
 - npm install

**Running Backend Server:**
 - cd ~/capstone-project-3900w16ccompgpt/backend
 - python3 main.py

**Running Frontend Server:**
 - cd ~/capstone-project-3900w16ccompgpt/frontend
 - npm run dev

**idk if this is necessary**
*Potential Error*
 - when installing nodejs in ubuntu 20.04, the node version (check by 'node -v') may install an outdated version of nodejs
 - if this is the case, when running the Frontend Server, an error may occur:
    ```
    import { performance } from 'node:perf_hooks'
        ^

    SyntaxError: Unexpected token {
        at Module._compile (internal/modules/cjs/loader.js:723:23)
        at Object.Module._extensions..js (internal/modules/cjs/loader.js:789:10)
        at Module.load (internal/modules/cjs/loader.js:653:32)
        at tryModuleLoad (internal/modules/cjs/loader.js:593:12)
        at Function.Module._load (internal/modules/cjs/loader.js:585:3)
        at Function.Module.runMain (internal/modules/cjs/loader.js:831:12)
        at startup (internal/bootstrap/node.js:283:19)
        at bootstrapNodeJSCore (internal/bootstrap/node.js:623:3)
    npm ERR! code ELIFECYCLE
    npm ERR! errno 1
    npm ERR! frontend@0.0.0 dev: `vite`
    npm ERR! Exit status 1
    npm ERR! 
    npm ERR! Failed at the frontend@0.0.0 dev script.
    npm ERR! This is probably not a problem with npm. There is likely additional logging output above.
    ```
 - to fix this, manually install nodejs version (v18.15.0 or higher)
 - Steps: https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-20-04 *Option 3*
    - curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh
    - curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
    - source ~/.bashrc
    - nvm list-remote
    - nvm install v18.15.0