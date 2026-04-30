# cdp-launchpad
A lightweight, Cloudera-branded Streamlit application that centralises all CDP platform URLs — including Data Catalog, Query Editor, Data Flow, Management Console, and more — into a single dashboard organised by environment (Production, Dev, DR). Built for fast deployment on Cloudera AI Applications.

<img width="1488" height="761" alt="image" src="https://github.com/user-attachments/assets/ac03a731-18da-4866-b463-cc1b844af026" />



# Setup Instructions 

### Step 1: Upload the below files onto a Cloudera AI Project. 
- app.py
- launch_app.py
- requirements.txt

### Step 2: Create Application 

Create an Application in the Cloudera AI by navigating to Applications and clicking on New Application.

Provide a Name and subdomain to be used for the application 

choose the **launch_app.py** as the script

choose a runtime (3.9,3.10 etc.) and resource profile (2VCPU/4GB) 

Click on **Create Application**

### Step 3: Launch Application 

Once the application state is changed to Running, Click on the application or use https://subdomain.workspacedomainname.

