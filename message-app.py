from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
import requests
import os 

slackurl = os.environ['SLACK_API_KEY']
port = int(os.environ['PORT'])

app = Flask(__name__)

@app.route('/wptoslack/api/v1.0/message', methods=['POST'])
def create_task():
    headers = {'Content-type': 'application/json'}

    author = str(request.form.get("comment_author"))
    content = str(request.form.get("comment_content"))
    date = str(request.form.get("comment_date"))

    data_message = '"username": "wordpresshelper","text":"New comment needs your approval!","icon_emoji": ":squirrel:"'
    attachments = '[{"author_name": "'+ author +'", "text": "' + content + '", "title": "Posted on ' + date + '"}]'

    r = requests.post(slackurl, data='{'+ data_message +', "attachments": ' + attachments + '}', headers=headers)

    return jsonify({'response': "Nice!"}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)