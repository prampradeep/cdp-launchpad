# cdp-launchpad
A lightweight, Cloudera-branded Streamlit application that centralises all CDP platform URLs — including Data Catalog, Query Editor, Data Flow, Management Console, and more — into a single dashboard organised by environment (Production, Dev, DR). Built for fast deployment on Cloudera AI Applications.

<img width="1436" height="763" alt="image" src="https://github.com/user-attachments/assets/1c815ac1-b3ab-4577-9487-d025a9b6c3cc" />




# Setup Instructions 

### Step 1: Upload the below files onto a Cloudera AI Project. 
- app.py
- launch_app.py
- requirements.txt

### Step 2: Create Application 

Create an Application in the Cloudera AI by navigating to Applications and clicking on New Application.

Provide a Name and subdomain to be used for the application 

choose the **launch_app.py** as the script, ensure the app.py path is referenced correctly.

choose a runtime (3.9,3.10 etc.) and resource profile (2VCPU/4GB) 

Click on **Create Application**

### Step 3: Launch Application 

Once the application state is changed to Running, Click on the application or use https://subdomain.workspacedomainname.

