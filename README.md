## Order Tracker

Order tracking app built with fastapi. Mostly an experiment

Current functionality:
- List orders and highlight them based on their current status

### Starting the app locally
    pip3 install -r requirements.txt
    uvicorn app:app --reload


### Loading the db
You need to start the app at least once to create the DB. Then run below:

    python3 order_tracker/database/add_samples.py