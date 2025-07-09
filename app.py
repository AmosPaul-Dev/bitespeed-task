from flask import Flask, jsonify, request
from sqlalchemy import or_
import os

from models import db, Contact


def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)

    
    db_url = os.environ.get("DATABASE_URL", "sqlite:///local.db")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Create tables if they don't exist yet
    with app.app_context():
        db.create_all()

    # ----------------------- Routes -----------------------
    @app.route("/")
    def index():
        """Health check / root endpoint."""
        return jsonify({"message": "Hello from Flask on Render!"})

    @app.route("/identify", methods=["POST"])
    def identify():
        """Consolidate contacts based on provided email / phone using simplified logic."""
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        phone_no = data.get("phoneNumber")
        phone_no = str(phone_no) if phone_no is not None else None

        # Validation – at least one field provided
        if not email and not phone_no:
            return (
                jsonify({"error": "At least one of 'email' or 'phoneNumber' is required."}),
                400,
            )

        with db.session.begin():  # atomic-like transaction
            # Build dynamic filters
            filters = []
            if email:
                filters.append(Contact.email == email)
            if phone_no:
                filters.append(Contact.phoneNumber == phone_no)

            contacts_query = (
                Contact.query.filter(or_(*filters)) if filters else Contact.query.filter(False)
            )

            contacts = contacts_query.order_by(Contact.createdAt).all()

            # If no contacts found, create a new primary contact
            if not contacts:
                primary = Contact(
                    email=email,
                    phoneNumber=phone_no,
                    linkPrecedence="primary",
                )
                db.session.add(primary)
                db.session.flush()  # get primary.id
            else:
                candidate = contacts[0]  # earliest created
                # If candidate is SECONDARY and has linkedId, true primary is linked contact
                if candidate.linkPrecedence == "secondary" and candidate.linkedId:
                    primary = Contact.query.get(candidate.linkedId)
                else:
                    primary = candidate

                # Ensure every contact sharing same email or phone is linked to this primary
                related_matches = Contact.query.filter(
                    or_(Contact.email == primary.email, Contact.phoneNumber == primary.phoneNumber)
                ).filter(Contact.id != primary.id).all()

                for c in related_matches:
                    if c.linkPrecedence != "secondary" or c.linkedId != primary.id:
                        c.linkPrecedence = "secondary"
                        c.linkedId = primary.id

                # Create a secondary if incoming data introduces new email/phone in this cluster
                existing_emails = {c.email for c in contacts if c.email}
                existing_phones = {c.phoneNumber for c in contacts if c.phoneNumber}

                if (email and email not in existing_emails) or (
                    phone_no and phone_no not in existing_phones
                ):
                    new_secondary = Contact(
                        email=email,
                        phoneNumber=phone_no,
                        linkPrecedence="secondary",
                        linkedId=primary.id,
                    )
                    db.session.add(new_secondary)

            db.session.flush()

            # Build response payload – include primary and all linked secondaries ordered by createdAt
            group = (
                Contact.query.filter(or_(Contact.id == primary.id, Contact.linkedId == primary.id))
                .order_by(Contact.createdAt)
                .all()
            )

            emails, phones, secondary_ids = [], [], []
            for idx, contact in enumerate(group):
                if idx > 0:
                    secondary_ids.append(contact.id)
                if contact.email and contact.email not in emails:
                    emails.append(contact.email)
                if contact.phoneNumber and contact.phoneNumber not in phones:
                    phones.append(contact.phoneNumber)

            response_payload = {
                "contact": {
                    "primaryContactId": primary.id,
                    "emails": emails,
                    "phoneNumbers": phones,
                    "secondaryContactIds": secondary_ids,
                }
            }

            return jsonify(response_payload), 200

    return app


# The WSGI-compliant app object for gunicorn/Render
app = create_app()

if __name__ == "__main__":
    # When running locally, Flask's built-in server is sufficient.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) 