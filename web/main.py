import logging

import requests
from flask import Flask, url_for, redirect, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask("web", template_folder="templates")
# Load configuration values for the web component (secret key used for CSRF, port and hostname).
app.config.from_pyfile('config.cfg')
logging.basicConfig(level=logging.DEBUG)
# Enable the Bootstrap plugin to make the UI more attractive.
Bootstrap(app)


# The form through which users send new messages.
class MessageForm(FlaskForm):
    name = StringField("Your name")
    message = StringField("Your message")
    submit = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
def show_index():
    # List containing the previous messages (should be retrieved from API later).
    r = requests.get("http://api:5000/messages")
    data = r.json()
    messages = data['data']
    form = MessageForm()
    if form.validate_on_submit():
        # Log the received message (should be processed by the API later).
        app.logger.info("Received message '{}' from '{}'".format(form.message.data, form.name.data))
        r = requests.post('http://api:5000/send', json={
            "author": form.name.data,
            "message": form.message.data
        })
        data = r.json()
        app.logger.info("Received following response from the API: {}".format(data))
        # If the message is successfully received, redirect the user to the GET version of the page
        # to prevent them from sending the message again when refreshing.
        return redirect(url_for('show_index'))
    return render_template('home.html', form=form, messages=messages)


def main():
    app.run(host=app.config['HOSTNAME'], port=int(app.config['PORT']))


if __name__ == "__main__":
    main()
