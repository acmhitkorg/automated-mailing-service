from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from email.message import EmailMessage
from pymongo import MongoClient
import ssl
import smtplib
from fastapi.middleware.cors import CORSMiddleware
from links import links
from schemas import Email


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(links.MONGO_URI)
db = client[links.DB]
collection = db[links.COLLECTION]


app = FastAPI()


@app.get("/")
def get_api_info():
    return {
        "title": "EmailAPI",
        "description": "This API allows you to send emails with optional image attachments.",
        "authors": [
            {
                "name": "Soumyajit Datta",
                "email": "talentedsd19@gmail.com"
            },
            {
                "name": "Jeet Nandigrami",
                "email": "jeetnandigrami2003@gmail.com"
            }
        ],
        "working": "The API is designed to facilitate email sending. You can use the following endpoints:",
        "endpoints": [
            {
                "path": "/get_all_email_ids",
                "description": "Get a list of all email IDs stored in the database.",
                "method": "GET"
            },
            {
                "path": "/sendmail",
                "description": "Send an email with an optional image attachment.",
                "method": "POST",
                "parameters": {
                    "subject": "str (required) - The email subject.",
                    "body": "str (required) - The email body.",
                    "imagedata": "str (optional) - Base64-encoded image data."
                }
            }
        ],
        "note": "Before using the sendmail endpoint, ensure that the 'email_list' collection in the database contains the email IDs to which you want to send emails."

    }


@app.get("/get_all_email_ids")
def get_all_email_ids():
    email_id_obj = collection.find({}, {"_id": 0, "email": 1})
    email_id_list = [mail["email"] for mail in email_id_obj]
    return email_id_list


@app.post("/sendmail")
def index(email: Email):

    email_sender = links.EMAIL_SENDER
    email_password = links.APP_PASSWORD

    email_id_list = get_all_email_ids()

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_id_list
    em['Subject'] = email.subject
    em.set_content(email.body)

    context = ssl.create_default_context()

    try:

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_id_list, em.as_string())
            return {'status': "mail sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
