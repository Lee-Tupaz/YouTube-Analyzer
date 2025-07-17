# YouTube-Analyzer
Discover trending YouTube videos based on region.

API:
- To generate your own API key go to, https://console.developers.google.com/
- Search for YouTube-API and click "CREATE CREDENTIALS"
- It will ask you "What data will you be accessing?". Click on Public data.
- Then it will generate your API key.

- Other reference using googleapis: https://github.com/googleapis/google-api-python-client

DATABASE:
- This application runs on localhost
- Enter this SQL Query first 'CREATE DATABASE youtube_trends'
- Go to src/config/settings.py
- Configure your YouTube API key, Database host : 'localhost', username, password, database : 'youtube_trends'

SAMPLE REGION CODES:
CA = Canada
US = United States of America
GB = United Kingdom of Great Britain
HK = Hong Kong
IT = Italy
JP =  Japan
PH = Philippines

Before running this application, enter these on terminal in order to run:
python -m pip install mysql-connector-python
python -m pip install google-api-python client
