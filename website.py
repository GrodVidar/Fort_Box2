import flask

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    code = flask.request.form.get('code')
    if code:
        with open('key.txt','w') as file:
            file.write(str(code))
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug = False)
