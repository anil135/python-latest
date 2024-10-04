
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/mydatabase'
db = SQLAlchemy(app)

# Define the User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


# Default route for testing
@app.route('/')
def index():
    return "Hello, World!"

# Create a route to insert a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    
    # Validate the incoming data
    if not data or 'name' not in data:
        return jsonify({'message': 'Invalid request, name is required'}), 400

    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': f"User '{new_user.name}' added successfully"}), 201

# Create a route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users]), 200


if __name__ == '__main__':
    # Create database tables if they do not exist
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=5000)

