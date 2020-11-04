from flask import Flask, request

app = Flask(__name__)

@app.route("/what")
def handler():
    return "Type: [{0}]".format(type(request.args))

if __name__ == "__main__":
    app.run(debug=True)
