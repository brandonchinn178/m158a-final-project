import os, requests, json
from flask import Flask, jsonify, request

IS_HEROKU = bool(os.environ.get('IS_HEROKU'))
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')

@app.route('/')
def home():
    return jsonify(status='success')

@app.route('/audio-features')
def get_audio_features():
    track_id = request.args.get('track_id')
    if track_id is None:
        return jsonify(status='no track id')

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
    }
    r = requests.post('https://accounts.spotify.com/api/token', data=data)
    access_token = r.json()['access_token']

    r = requests.get('https://api.spotify.com/v1/audio-features/%s' % track_id, headers={
        'Authorization': 'Bearer %s' % access_token,
    })

    if r.status_code == 200:
        return jsonify(**r.json())
    else:
        return jsonify(**r.json()), r.status_code

if __name__ == '__main__':
    app.run(debug=not IS_HEROKU)
