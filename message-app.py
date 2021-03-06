from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
import requests
import os
import json 

slackurl = os.environ['SLACK_API_KEY']
port = int(os.environ['PORT'])

app = Flask(__name__)

@app.route('/wptoslack/api/v1.0/message', methods=['POST'])
def create_task():
    headers = {'Content-type': 'application/json'}

    author = str(request.form.get("comment_author"))
    content = str(request.form.get("comment_content"))
    date = str(request.form.get("comment_date"))
    approved = int(request.form.get("comment_approved"))
    hook = bool(request.form.get("hook"))

    attachments = {"author_name": author, "text": content, "title": "Posted on " + date}

    data = {"username": "wordpresshelper","icon_emoji": ":squirrel:"}

    if approved == 1:
    	data["text"] = "New comment has been posted"
    else:
    	data["text"] = "New comment needs your approval!"
    	attachments["color"] = "warning"

    data["attachments"] = [attachments]

    r = requests.post(slackurl, data=json.dumps(data), headers=headers)

    return jsonify({'response': "Posted on Slack"}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)