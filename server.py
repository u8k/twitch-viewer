from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# force update of static files on every refresh
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/twitch", methods = ['GET'])
def twitch():
    return render_template('twitch.html')

@app.route("/twitch", methods = ['POST'])
def twitchAPI():
    channel = request.data
    url = "https://api.twitch.tv/kraken/streams/" + channel + "?client_id=f9548j618zhrxjedzvjdinqmx44lsl"
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    #if they aren't currently streaming, then check if the channel is dead
    if data['stream'] == None:
        url = "https://api.twitch.tv/kraken/channels/" + channel + "?client_id=f9548j618zhrxjedzvjdinqmx44lsl"
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]
        data = json.loads(result)
        if data['status'] == 404:
            return jsonify(' is a defunct channel', 'false')
        return jsonify(' is currently offline', 'false')
    return jsonify(" is playing " + data['stream']['game'], 'true')


if __name__ == '__main__':
    #app.debug = True
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0')
