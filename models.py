from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# Shared SQLAlchemy database instance
# This object will be initialized inside app.py

db = SQLAlchemy()


class Contact(db.Model):
    """Represents a user contact that may be linked/merged with others."""

    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)

    linkedId = db.Column(
        db.Integer, db.ForeignKey("contacts.id"), nullable=True, index=True
    )  # self-referencing FK to primary contact

    linkPrecedence = db.Column(
        db.String(10), nullable=False, default="primary"
    )  # "primary" | "secondary"

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deletedAt = db.Column(db.DateTime, nullable=True)

    # Relationship to jump from a secondary contact to its primary
    primary_contact = db.relationship("Contact", remote_side=[id], uselist=False) 