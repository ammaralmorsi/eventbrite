# EventBrite

EventBrite is an online event registration service that allows users to find and register for events, and allows event
organizers to plan and promote their events.

## Installation Instructions

**Note for Windows Users:**
Please go away and don't come back until you have a Linux machine.

For all other users, please follow the installation instructions below:

1. Create a conda environment with Python 3.10.4 using the following command:

```bash
conda create -n eventbrite python=3.10.4
``` 

2. Activate the conda environment:

```bash
conda activate eventbrite
```

3. From inside the virtual environment, install the required packages specified in the "requirements.txt" file you
   created:

```bash
pip install -r requirements.txt
```
4. Add the following environment variables:
    
```bash
export MONGO_URI="your mongo connection string"
export MONGO_DB="your database name"
```
5. From inside the virtual environment, demonstrate your ability to run the Python script from the command-line:

```bash
uvicorn main:app --reload
```
6. Navigate through docs to learn more about the API with the following link [docs](http://127.0.0.1:8000/docs)



## Contributors
If you want to contribute to this project, please follow the instructions below:
1. You should be invited to the project as a collaborator.
2. Create a new branch based on *temp* with the following naming convention: `your-feature-name`
3. Make your changes and push them to the remote repository.
4. Create a pull request from your branch to the *temp* branch.


## Issues
If you have any issues, or you want to improve the apis and docs, please create an issue in the repository documents
what exactly the issue is, and how should we help you solve it. So for example if our api doesn't fit your needs, you
should create an issue that describes what you want to do, and how you want to do it. If you want to improve the docs,
you should create an issue that describes what you want to improve, and how you want to improve it.
*do not send whatsapp messages*
