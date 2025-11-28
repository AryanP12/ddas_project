# app.py

from flask import Flask, request, jsonify
from models import db, Dataset
from sqlalchemy import or_  # <--- NEW IMPORT
import datetime

# --- App Initialization ---
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

# --- API Endpoints ---

@app.route('/api/check_duplicate', methods=['POST'])
def check_duplicate():
    """
    Checks if a file is a potential duplicate based on its partial hash OR URL.
    """
    data = request.get_json()
    if not data or 'partial_hash' not in data:
        return jsonify({"error": "Missing 'partial_hash' in request body"}), 400

    partial_hash = data.get('partial_hash')
    source_url = data.get('source_url')

    # --- FIXED QUERY LOGIC ---
    if source_url:
        # Search for EITHER the hash match OR the URL match
        existing_dataset = Dataset.query.filter(
            or_(
                Dataset.file_hash_partial == partial_hash,
                Dataset.source_url == source_url
            )
        ).first()
    else:
        # Search only by hash if no URL is provided
        existing_dataset = Dataset.query.filter(Dataset.file_hash_partial == partial_hash).first()
    # -------------------------

    if existing_dataset:
        return jsonify({
            "status": "duplicate_found",
            "data": existing_dataset.to_dict()
        }), 200
    else:
        return jsonify({"status": "no_duplicate_found"}), 404


@app.route('/api/register_file', methods=['POST'])
def register_file():
    """
    Registers a new file download or adds a new location to an existing file.
    """
    data = request.get_json()
    # Basic validation
    required_fields = ['full_hash', 'partial_hash', 'filename', 'size', 'user_id', 'location_path']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if this exact file (by full hash) already exists
    dataset = Dataset.query.filter_by(file_hash_full=data['full_hash']).first()
    
    new_location_entry = {
        "user": data['user_id'],
        "path": data['location_path'],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    if dataset:
        # File exists, just add the new location
        # We must create a new list to ensure SQLAlchemy detects the change to the JSON field
        current_locations = list(dataset.locations) if dataset.locations else []
        current_locations.append(new_location_entry)
        dataset.locations = current_locations
        message = "Added new location to existing file record."
    else:
        # Brand new file
        dataset = Dataset(
            file_hash_full=data['full_hash'],
            file_hash_partial=data['partial_hash'],
            original_filename=data['filename'],
            file_size_bytes=data['size'],
            source_url=data.get('source_url'),
            first_downloader_id=data['user_id'],
            locations=[new_location_entry],
            custom_metadata=data.get('custom_metadata', {})
        )
        db.session.add(dataset)
        message = "New file registered successfully."

    try:
        db.session.commit()
        return jsonify({"status": "success", "message": message, "data": dataset.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

@app.route('/')
def index():
    return "DDAS Central Server is running!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)