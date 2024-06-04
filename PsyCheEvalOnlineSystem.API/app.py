from flask import Flask, jsonify, request
from flask_cors import CORS
from db import conn
from flask_bcrypt import Bcrypt  # Import the Bcrypt module
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
bcrypt = Bcrypt(app)  # Create an instance of Bcrypt


@app.route('/api/checkusername', methods=['POST'])
def check_username():
    username = request.json["username"]

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [User] WHERE username = ?", username)
    existing_user = cursor.fetchone()
    cursor.close()

    if existing_user:
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})


@app.route('/api/register', methods=['POST'])
def signup():
    fullname = request.json["fullname"]
    username = request.json["username"]
    password = request.json["password"]

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hash the password
    cursor = conn.cursor()
    cursor.execute("INSERT INTO [User] ([fullname], [username], [password]) VALUES (?, ?, ?)",
                   (fullname, username, hashed_password))
    conn.commit()
    cursor.close()

    return jsonify({
        "fullname": fullname,
        "username": username,
        "password": hashed_password
    })


@app.route('/api/ProfessionalRegister', methods=['POST'])
def register():
    Name = request.json["Name"]
    ContactNumber = request.json["ContactNumber"]
    Email = request.json["Email"]
    Qualifications = request.json["Qualifications"]
    Link = request.json["Link"]
    Status = request.json["Status"]

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO [Resource] ([Name], [ContactNumber], [Email], [Qualifications], [Link], [Status]) VALUES (?, ?, ?, ?, ?, ?)",
        (Name, ContactNumber, Email, Qualifications, Link, Status))
    conn.commit()
    cursor.close()

    return jsonify({
        "Name": Name,
        "ContactNumber": ContactNumber,
        "Email": Email,
        "Qualifications": Qualifications,
        "Link": Link,
        "Status": Status
    })


@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [User] WHERE username = ?", username)
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.check_password_hash(user.password, password):
        # Passwords match, login is successful
        return jsonify({'message': 'Login successful',
                        'username': username})

    # Passwords do not match or the user doesn't exist, login failed
    return jsonify({'message': bcrypt.check_password_hash(user.password, password)})


def get_x_y(file_path):
    data = pd.read_csv(file_path)
    input_data = data.iloc[:, :-1]
    output_data = data.iloc[:, -1]
    return input_data, output_data


def prediction(curr_data, data_file):
    X, Y = get_x_y(data_file)
    clf = LinearRegression()
    clf = clf.fit(X, Y)
    prediction = clf.predict([curr_data])
    return str(prediction[0])


@app.route("/api/submit_ptsd", methods=["POST"])
def submit():
    data = request.get_json()
    result_ptsd = prediction(
        data, "D:\DataSet\Post Traumatic Stress Disorder.csv"
    )

    return jsonify({"result_ptsd": str(result_ptsd)})


@app.route("/api/submit_depression", methods=["POST"])
def submit2():
    data = request.get_json()
    result_depression = prediction(
        data, "D:\DataSet\Major Depression.csv"
    )
    return {
        "result_depression": str(result_depression),
    }


@app.route("/api/submit_bipolarDisorder", methods=["POST"])
def submit3():
    data = request.get_json()
    result_BipolarDisorder = prediction(
        data, "D:\DataSet\Bipolar Disorder.csv"
    )
    return {
        "result_BipolarDisorder": str(result_BipolarDisorder),
    }


@app.route("/api/submit_generalizedAnxiety", methods=["POST"])
def submit4():
    data = request.get_json()
    result_GeneralizedAnxiety = prediction(
        data, "D:\DataSet\Generalized Anxiety.csv"
    )
    return {
        "result_GeneralizedAnxiety": str(result_GeneralizedAnxiety),
    }


@app.route('/api/get_data', methods=['GET'])
def get_data():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Resource WHERE Status =1")
    data = cursor.fetchall()
    cursor.close()
    result = []
    for row in data:
        result.append({
            'ResourceId': row[0],
            'Name': row[1],
            'ContactNumber': row[2],
            'Email': row[3],
            'Qualifications': row[4],
            'Link': row[5],
            'Status': row[6],
        })
    return jsonify(result)


if __name__ == "_main_":  # Use "__main" instead of "_main"
    app.run(debug=True)
