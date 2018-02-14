# Network Analytics Insight

## About:
Idea behind this application is to implement self-service network intelligence.
1. Connect to your datastore.
2. Get to know trend-lines, anomalies and classification within your network flows.

## Setup:
1. `git clone` this repository and go to network_analytics folder.
2. `pip install -r requirements.txt`
3. Setup flask app environment variable
   `export FLASK_APP=netanalytics.py`
4. Run the server:
   flask run [--host=<ip>]
5. Go to http://<ip:5000> on web browser and start using application
