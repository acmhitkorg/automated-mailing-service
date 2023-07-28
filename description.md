Email Service API Documentation

Description:
This API allows you to manage email recipients and send emails to those recipients using a MongoDB database and a Gmail SMTP server.

Before proceeding with the API, make sure to configure the config.py file with your own details and links.

"endpoints": [
{
"url": "/",
"method": "GET",
"summary": "Get information about the API.",
"description": "Provides an overview of the API, its purpose, and the available endpoints.",
},
{
"url": "/recipient_list",
"method": "GET",
"summary": "Get a list of email addresses of recipients.",
"description": "Retrieves a list of email addresses from the MongoDB collection.",
"response": ["email1@example.com", "email2@example.com", "..."]
},
{
"url": "/push_new_recipient",
"method": "POST",
"summary": "Add a new recipient.",
"description": "Adds a new recipient to the MongoDB collection.",
"request": {
"name": "John Doe",
"email": "johndoe@example.com"
},
"response": {
"message": "Data inserted successfully"
}
},
{
"url": "/send_mail",
"method": "POST",
"summary": "Send an email.",
"description": "Sends an email to all recipients in the MongoDB collection.",
"request": {
"subject": "sample subject",
"body": "sample body"
},
"response": {
"status": "mail sent successfully"
}
}
]
