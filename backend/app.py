from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from models import db, ScanResults
from datetime import datetime
from io import BytesIO  # For in-memory file handling
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the absolute path for the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Root route
@app.route('/')
def home():
    return "Welcome to the PDF Scan App Backend!"

# Route to handle PDF scanning
@app.route('/scan', methods=['POST'])
def scan_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    user = request.form.get('user', 'Anonymous')
    file_name = file.filename

    # Read the file into memory
    file_data = file.read()

    # Call the scan function with in-memory file data
    try:
        from scan import scan_pdf
        result = scan_pdf(BytesIO(file_data))  # Pass the in-memory file data
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Save results to the database
    new_scan = ScanResults(
        file_name=file_name,
        user=user,
        result=str(result)  # Ensure result is a string
    )
    db.session.add(new_scan)
    db.session.commit()

    return jsonify({"result": result})

# Route to fetch all scan results
@app.route('/scans', methods=['GET'])
def get_scans():
    scans = ScanResults.query.all()
    scans_list = []
    for scan in scans:
        scans_list.append({
            "id": scan.id,
            "file_name": scan.file_name,
            "date": scan.date.isoformat(),  # Convert datetime to string
            "user": scan.user,
            "result": scan.result
        })
    return jsonify(scans_list)

if __name__ == '__main__':
    with app.app_context():
        # Create the database and tables
        db.create_all()

    # Run the Flask app
    app.run(debug=True)