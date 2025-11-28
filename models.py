# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
import datetime

# Initialize SQLAlchemy without a specific app
db = SQLAlchemy()

class Dataset(db.Model):
    __tablename__ = 'datasets'

    id = db.Column(db.Integer, primary_key=True)
    file_hash_full = db.Column(db.String(64), unique=True, nullable=False)
    file_hash_partial = db.Column(db.String(64), nullable=False, index=True)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size_bytes = db.Column(db.BigInteger, nullable=False)
    source_url = db.Column(db.Text, index=True)
    first_download_timestamp = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    first_downloader_id = db.Column(db.String(100))
    
    # Store multiple locations [{user, path, timestamp}, ...]
    locations = db.Column(JSONB)
    
    # Store domain-specific data {period, spatial_domain, ...}
    custom_metadata = db.Column(JSONB)

    def to_dict(self):
        """Converts the object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'original_filename': self.original_filename,
            'file_size_bytes': self.file_size_bytes,
            'first_downloaded_by': self.first_downloader_id,
            'first_downloaded_at': self.first_download_timestamp.isoformat(),
            'known_locations': self.locations,
            'source_url': self.source_url,
            'metadata': self.custom_metadata
        }