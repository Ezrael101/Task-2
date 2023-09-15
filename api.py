from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ezrael_postgre_sql_user:QrzWEJWxSVwKnbbOsGPagmDoRTUrQ4ki@dpg-ck1nt6821fec73e7vio0-a/ezrael_postgre_sql'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define a Person model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    track = db.Column(db.String(255), nullable=False)

    def __init__(self, name, track):
        self.name = name
        self.track = track

# Create the database tables
db.create_all()

# Create a new Person
@app.route('/api', methods=['POST'])
def create_Person():
    data = request.get_json()
    new_Person = Person(name=data["name"], track=data["track"])
    db.session.add(new_Person)
    db.session.commit()
    return jsonify(new_Person.serialize()), 201

# Read a specific Person
@app.route('/api/<int:user_id>', methods=['GET'])
def get_Person(Person_id):
    Person = Person.query.get(Person_id)
    if Person:
        return jsonify(Person.serialize())
    return "Person not found", 404

# Update a Person
@app.route('/api/<int:user_id>', methods=['PUT'])
def update_Person(Person_id):
    data = request.get_json()
    Person = Person.query.get(Person_id)
    if Person:
        Person.name = data["name"]
        db.session.commit()
        return jsonify(Person.serialize())
    return "Person not found", 404

# Delete a Person
@app.route('/api/<int:user_id>', methods=['DELETE'])
def delete_Person(Person_id):
    Person = Person.query.get(Person_id)
    if Person:
        db.session.delete(Person)
        db.session.commit()
        return "Person deleted", 204
    return "Person not found", 404

if __name__ == '__main__':
    app.run(debug=True)
