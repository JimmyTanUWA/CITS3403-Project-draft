from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to create the database tables
def create_tables():
    conn = sqlite3.connect('website.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS content
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, content TEXT, FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

# Function to register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    conn = sqlite3.connect('website.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Username already exists'}), 400

# Function to submit content
@app.route('/submit-content', methods=['POST'])
def submit_content():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    content = data.get('content')
    
    if not username or not password or not content:
        return jsonify({'error': 'Username, password, and content are required'}), 400
    
    conn = sqlite3.connect('website.db')
    c = conn.cursor()
    
    # Check if the user exists and the password is correct
    c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    if user:
        user_id = user[0]
        # Insert content associated with the user
        c.execute("INSERT INTO content (user_id, content) VALUES (?, ?)", (user_id, content))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Content submitted successfully'}), 201
    else:
        conn.close()
        return jsonify({'error': 'Invalid username or password'}), 401

# Function to retrieve content
@app.route('/get-content', methods=['GET'])
def get_content():
    conn = sqlite3.connect('website.db')
    c = conn.cursor()
    c.execute("SELECT content FROM content")
    content = c.fetchall()
    conn.close()
    return jsonify({'content': content})

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)