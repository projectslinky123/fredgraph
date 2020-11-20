from flask import escape
import math
import os
from config import Config
import requests

def send_response(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = getgraphdata("W006RC1A027NBEA")
    return 'Hello {}!'.format(escape(name))


def getgraphdata(seriesid):
    desc_request_url = Config['FRED_SERIES_URL']
    request_url = Config['FRED_SERIES_DATA_URL']
    payload = {"api_key": os.environ.get('fred_apikey'),
               "series_id": seriesid,
               "file_type": "json"}
    response1 = requests.get(desc_request_url, params=payload)
    data1 = response1.json()
    response = requests.get(request_url, params=payload)
    data = response.json()
    xlist = []
    ylist = []
    for k in range(len(data["observations"])):
        xlist.append(data["observations"][k]["date"])
        ylist.append(math.floor(float(data["observations"][k]["value"])))

    return data1["seriess"][0]["title"], data, "year", data1["seriess"][0]["units"], xlist, ylist