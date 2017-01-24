import datetime
import logging

from flask import Flask, jsonify, request

app = Flask("api")
# Load configuration values for the API component (port and hostname).
app.config.from_pyfile('config.cfg')
logging.basicConfig(level=logging.DEBUG)


@app.route('/messages')
def get_all_messages():
    # List containing the previous messages (should be retrieved from MongoDB later).
    messages = [{
        "author": "Anonymous",
        "message": "I'm an anonymous legionary",
        "timestamp": str(datetime.datetime.now())
    }]
    return jsonify({
        "error": None,
        "data": messages
    })


@app.route('/send', methods=['POST'])
def send_message():
    # Load the content of the POST request.
    data = request.get_json()
    # Retrieve the current timestamp to store with the message content.
    timestamp = datetime.datetime.now()
    # Log the received message (should be stored in MongoDB later).
    app.logger.debug("Message '{}' from '{}' received at '{}'".format(data['message'], data['author'], str(timestamp)))
    return jsonify({
        "error": None,
        "data": {
            "author": data['author'],
            "message": data['message'],
            "timestamp": str(timestamp)
        }
    })


def main():
    app.run(host=app.config['HOSTNAME'], port=int(app.config['PORT']))


if __name__ == "__main__":
    main()
