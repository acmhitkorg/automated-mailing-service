import json
from fastapi import FastAPI, HTTPException, status
from email.message import EmailMessage
from pymongo import MongoClient
import ssl
import smtplib
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from config import configuration
from schemas import Email, New

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
client = MongoClient(configuration.MONGO_URI)
db = client[configuration.DB]
collection = db[configuration.COLLECTION]


@app.get("/")
def get_api_info():
    """
    Root endpoint to check if the API is working.
    """
    return {
        "title": "Email Service API",
        "description": "This API allows you to manage email recipients and send emails to those recipients using a MongoDB database and a Gmail SMTP server.",
        "status": "working"
    }


@app.get("/recipient_list")
def get_recipient_list():
    """
    Get a list of email addresses of recipients from the MongoDB collection.

    Returns:
        List[str]: A list of email addresses of recipients.
    """
    try:
        # Use meaningful variable names and only retrieve 'email' field from the collection
        recipient_emails = collection.find({}, {"_id": 0, "email": 1})

        # Extract the email addresses from the database result
        email_addresses = [recipient["email"]
                           for recipient in recipient_emails]

        return email_addresses
    except Exception as e:
        # Proper error handling and exception details
        raise HTTPException(
            status_code=500, detail="Failed to retrieve recipient list.")


@app.post("/push_new_recipient", response_model=dict)
def push_new_recipient(recipient: New):
    """
    Add a new recipient to the MongoDB collection.

    Parameters:
        - recipient: New (Pydantic model representing the new recipient's data)

    Returns:
        dict: A message indicating that the data was inserted successfully.

    Raises:
        HTTPException: If the data insertion fails or if there are validation errors.
    """
    try:

        inserted_data = collection.insert_one(jsonable_encoder(recipient))
        if not inserted_data.acknowledged:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to insert data")

        return {"message": "Data inserted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/send_mail")
def send_mail(email: Email):
    """
    Send an email to all recipients in the MongoDB collection.

    Parameters:
        - email: Email (Pydantic model representing the email details)

    Returns:
        dict: A message indicating that the email was sent successfully.

    Raises:
        HTTPException: If there are validation errors or if the email sending fails.
    """

    email_sender = configuration.EMAIL_SENDER
    email_password = configuration.APP_PASSWORD
    email_recipients = get_recipient_list()

    # Check if there are recipients to send the email to
    if not email_recipients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No recipients found. Please add recipients first.")

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_recipients
    em['Subject'] = email.subject
    em.set_content(email.body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_recipients, em.as_string())
            return {'status': "mail sent successfully"}
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to send email: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error occurred: {str(e)}")
