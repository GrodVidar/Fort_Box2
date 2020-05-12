import flask
import sqlite3

app = flask.Flask(__name__)


connection = sqlite3.connect('code', check_same_thread=False)
cursor = connection.cursor()


@app.route('/', methods=['GET', 'POST'])
def home():
    print(flask.request.form)
    code = flask.request.form.get('code')
    if code:
        with open('text.txt', 'w') as f:
            f.write(str(code))
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False)
