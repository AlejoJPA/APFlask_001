from flask import Flask, request, jsonify

app = Flask(__name__)

data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]

#This endpoint only check if the hardcoded data exist
@app.route("/data")
def get_data():
    try:
        # Check if 'data' exists and has a length greater than 0
        if data and len(data) > 0:
            # Return a JSON response with a message indicating the length of the data
            return {"message": f"Data of length {len(data)} found"}
        else:
            # If 'data' is empty, return a JSON response with a 500 Internal Server Error status code
            return {"message": "Data is empty"}, 500
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a 404 Not Found status code
        return {"message": "Data not found"}, 404


# Endpoint for seraching for a person in data
@app.route("/name_search")
def find_person():
    """Find a person in the database. 
    It intends to deal with a requues like:     
                curl -X GET -i -w '\n' "localhost:5000/name_search?q=Abdel"
                or "https://localhost:5000/name_search?q=Abdel"

                    ? → Indicates the beginning of query parameters.
                    q=Abdel → A key-value pair where: 
                                    q is the parameter name.
                                    Abdel is the value being passed.
    Returns:
        json: Person if found, with status of 200
        404: If not found
        422: If argument 'q' is missing
    """
    # setup the query format. It uses request.args.get() to fetch parameters (e.g., 'q')

    query = request.args.get('q') #Get the argument 'q' from the query parameters of the request

    # Check if the query parameter 'q' is missing (does not exist)
    if not query:
        # Return a JSON response with a message indicating 'q' is missing and a 422 Unprocessable Entity status code
        return {"message": "Query parameter 'q' is missing"}, 422

    # Iterate through the 'data' list to look for the person whose first name matches the query
    for person in data:
        if query.lower() in person["first_name"].lower():
            # If a match is found, return the person as a JSON response with a 200 OK status code
            return person
            
    # If no match is found, return a JSON response with a message indicating the person was not found and a 404 Not Found status code
    return {"message": "Person not found"}, 404


# GET endpoint/count endpoint
@app.get('/count')
def count_data():
    '''
        This endpoint attempts to return a JSON response with the count of items in 'data' , 
        i.e, len(data), status code: 200
        It returns a JSON response with a message otherwise with a 500 Internal Server Error status code  
    '''
    #Cofigure exceptions
    try:
        return ({'data count': len(data)}, 200)
   
    except NameError:
        returm ({'message':"data not defined"}, 500)


# Endpoint: search for a person with a matching ID
@app.route("/person/<uuid:id>") # Note: <uuid:id> must be in this <key:value> otherwise it is just a literal
def find_by_uuid(id):
    ''' for person in data:
            if person["id"] == str(id):
                return person
    '''
    # Rurn the person searched by 'id' using list comprehention format
    person = [ p for p in data if p["id"] == str(id) ]

    if person:
        return jsonify(person)
    else:
        #  Return a JSON response: 404 Not Found status code if no matching person is found
        return ({'message': 'Person not found'}, 404)

# Endpoint: delete person with a matching ID
@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_by_uuid(id):
    '''# Iterate through the 'data' list to search for a person with a matching ID
    for person in data:
        # Check if the 'id' field of the person matches the 'id' parameter
        if person["id"] == str(id):
            # Remove the person from the 'data' list
            data.remove(person)
            # Return a JSON response with a message confirming deletion and a 200 OK status code
            return {"message": f"Person with ID {id} deleted"}, 200'''
    person = [data.remove(p) for p in data if p["id"] == str(id)]
    if person:
        return {"message": f"Person with ID {id} deleted"}, 200
    # If no matching person is found, return a JSON response with a message and a 404 Not Found status code
    return {"message": "person not found"}, 404

#Endpoint: add person
@app.route("/person", methods= ['POST'])
def create_person():
    new_person = request.get_json()
    if not new_person:
        return ({"message": "Invalid input, no data provided"}, 400)
    
    #Appending new person to 'data'
    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500
    
    #return {"message": f"{new_person['id']}"}, 200
    return {"message": f"the person with ID: {new_person['id']} was created succesfully"}, 200


#Error Handler
@app.errorhandler(404)
def api_not_found(error):
        # This function is a custom error handler for 404 Not Found errors
        # It is triggered whenever a 404 error occurs within the Flask application
    return {"message": "API not found"}, 404