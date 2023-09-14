from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for development

# Configure MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_database'
mysql = MySQL(app)

@app.route('/api', methods=['POST'])
def create_person():
    # Add a new person to the database
    # Handle request data validation and insert into MySQL
    new_person = request.json
    name = new_person.get('name')
    if name:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO persons (name) VALUES (%s)", (name))
            mysql.connection.commit()
            cur.close()
    		return jsonify({"message": "Person added successfully"}), 201
    else:
    		return jsonify({"message": "Name is required"}), 400
    pass

@app.route('/api/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def person(user_id):
    # Fetch, update, or delete a person by user_id
    
    if request.method == 'GET':
        # Retrieve a person by user_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM persons WHERE id = %s", (user_id,))
        person = cur.fetchone()
        cur.close()
        if person:
            return jsonify(person), 200
        else:
            return jsonify({"message": "Person not found"}), 404
	
	elif request.method == 'PUT':
        # Update a person by user_id
        data = request.get_json()
        name = data.get('name')
        
        if name:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE persons SET name = %s WHERE id = %s", (name, user_id))
            mysql.connection.commit()
            cur.close()
            return jsonify({"message": "Person updated successfully"}), 200
        else:
            return jsonify({"message": "A name is required"}), 400
    
    elif request.method == 'DELETE':
        # Delete a person by user_id
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM persons WHERE id = %s", (user_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Person deleted successfully"}), 200
    pass

if __name__ == '__main__':
    app.run(debug=True)