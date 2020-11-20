from flask import escape
import math
import os
import io
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

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
        title, data, xaxisLabel, yaxisLabel, xlist, ylist = getgraphdata("W006RC1A027NBEA")
        fig = create_figure("year", yaxisLabel, xlist, ylist)
        results = fig
    return 'Hello {}!'.format(escape(results))


def getgraphdata(seriesid):
    desc_request_url = "https://api.stlouisfed.org/fred/series"
    request_url = "https://api.stlouisfed.org/fred/series/observations"
    payload = {"api_key": os.environ.get('FRED_API_KEY'),
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


def create_figure(xtitle, ytitle, x, y):
    fig = plt.figure(figsize=(15, 5))
    axis = fig.add_subplot(1, 1, 1)
    axis.set_xlabel(xtitle)
    axis.set_ylabel(ytitle)
    axis.grid()
    axis.plot(list(map(int, y)))
    xlabels = [""]
    xticks = [0]
    spacing = len(x)//10
    for i in range(11):
        xticks.append(spacing*i)
        xlabels.append(x[spacing*i])

    axis.set_xticks(xticks)
    axis.set_xticklabels(xlabels, rotation=70)
    fig.tight_layout()

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

