import datetime
import logging

from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask("api")
# Load configuration values for the API component (port and hostname).
app.config.from_pyfile('config.cfg')
logging.basicConfig(level=logging.DEBUG)

# Configure the connection to the database
mongo = MongoClient("db", 27017)
# The collection containing the information about the messages
messages_collection = mongo.database.messages


@app.route('/messages')
def get_all_messages():
    # List containing the relevant fields of all previous messages (most recent first).
    messages = [{"author": x['author'],
                 "message": x['message'],
                 "timestamp": x['timestamp']
                 } for x in messages_collection.find({}).sort("timestamp", -1)]
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
    # Store the record in MongoDB
    messages_collection.insert_one({'message': data['message'], 'author': data['author'], 'timestamp': str(timestamp)})
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
