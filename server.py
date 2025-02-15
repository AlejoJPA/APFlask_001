#Setting up the the simplest flask server
from flask import Flask , make_response
app = Flask(__name__) # create an object image of Flask

# general endpoint route to a root URL (localhost:5000)
@app.route("/") 
def index():
    '''It delivers a plain hello world mesaage'''
    return "Hello World!!! 12345...10"

## empty endpoint (localhost:5000/no_content)
@app.route("/no_content")
def no_content():
    """return 'No content found' with a status of 204
    Returns:
        string: No content found
        status code: 204
    """
    return ({"message": "No content found"}, 204)

# Endpoint to send an explicit response HTTP code with make_response()
@app.route("/exp")
def explicit_feedback():
    """return 'Hello World' message with a status code of 200
    Returns:
        string: Hello World
        status code: 200
    """
    response = make_response({"message": "Hello World"})
    response.statust_code = 200
    return response

