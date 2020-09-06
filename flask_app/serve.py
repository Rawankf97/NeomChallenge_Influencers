
from flask import Flask, jsonify, request, render_template
from multiprocessing import Process, Queue
from streamData import main

app = Flask(__name__)

pqueue = Queue()
msg = None
p = None


@app.route("/data", methods=['GET'])
def data():
    """
    When a request is received on route '/data' returns the latest results
    """
    global msg
    return jsonify(msg)


@app.route("/updated")
def updated():
    """
    When a request is received on route '/updated' waits for new results from the model
    then responds with a message signaling the data has been updated and is ready to be sent
    """
    global msg
    msg = pqueue.get()
    return "changed!"


@app.route("/", methods=['GET', 'POST'])
def index():
    """
    When a GET request is received on route '/' renders the search.html page
    When a POST request is received on route '/' sends the query parameters and starts the streaming process
    """
    global pqueue, p
    if request.method == 'POST':
        pqueue = Queue()
        print('Post request received')
        data = request.get_json()
        p = Process(target=main, args=((pqueue), data,))
        p.start()
        return jsonify('processing form and finding influencers...')
    return render_template("search.html")


@app.route('/dashboard')
def dashboard():
    """
    When a GET request is received on route '/dashboard' renders the dashboard.html page
    """
    return render_template('dashboard.html')


@app.route('/terminate')
def terminate():
    global p
    if p:
        p.kill()
    return 'Done'


if __name__ == "__main__":
    app.run(debug=True)
