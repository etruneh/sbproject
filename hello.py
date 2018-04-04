from flask import abort, Flask, request
import json
app = Flask(__name__)


@app.route("/hello/")
def hello():
    name = request.args.get("name")
    if not name:
        abort(400, "/hello requires string argument 'name'")

    return json.dumps(["This is a list of greetings", "Hello " + name, "How goes it?"])

@app.route("/")
def greeting():
	message = "Hello, welcome to my little API. Use via query string parameters."
	return message


app.run()



