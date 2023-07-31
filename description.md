# Email Service API using NODE JS Documentation

## 1. /
**Method: GET**
**Description:** This endpoint is used to check if the server is running.
**Response:**
- **Status Code:** 200
- **Body:** Welcome to the Email Sender API!

## 2. /send-email
**Method: POST**
**Description:** This endpoint allows users to send an email to multiple recipients with optional attachments.

**Request:**
- **Content-Type:** application/json
- **Request Body Parameters:**
  - `to` (string, required): A comma-separated list of email addresses of the recipients.
  - `subject` (string, required): The subject of the email.
  - `text` (string, required): The text content of the email.
  - `imagePath` (string, optional): The relative path to an image file to be included as an attachment.

**Response:**
- **Status Code:** 200 if the email was sent successfully, 500 if there was an error.

**Example Request:**
To test this API use postman:

POST http://localhost:6000/send-email
Content-Type: application/json
```

{
  "to": "recipient1@example.com,recipient2@example.com",// From your MongoDB Database automatically
  "subject": "Greetings",
  "text": "Hello, this is a test email.",
  "imagePath": "example-image.jpg" // Put the image file in the same directory as your .js files
}
```

**Example Response (Success):**
- **Status Code:** 200
- **Response Body:**
```
{
  "message": "Email sent successfully"
}
```

**Example Response (Error):**
- **Status Code:** 500
- **Response Body:**
```
{
  "error": "Failed to send email"
}
```

## How It Works:

1. The server starts by connecting to the MongoDB database using the provided MongoDB URI.

2. When a POST request is made to /send-email, the server extracts the recipient email addresses from the request body.

3. It then queries the MongoDB collection named 'Your_collection_name' to retrieve all the recipient data.

4. The email addresses are extracted from the email field of each recipient.

5. Nodemailer is used to create an email message with the provided subject and text.

6. If an imagePath is provided in the request body, the corresponding image file is attached to the email.

7. The email is sent to all recipients using the Gmail account specified in the server's configuration.

8. If the email is sent successfully, a success response is returned; otherwise, an error response is returned.

9. The MongoDB connection is closed after the operation is complete.

## Configuration:

1. Ensure that the MongoDB URI provided in the code is valid and points to a database with the appropriate collection containing recipient data. Replace 'Your_collection_name' with the actual name of the collection.

2. Open the `configure.js` file and fill in the required information:
   - `mongodbURI`: Your MongoDB database URI.
   - `gmailUser`: Your Gmail email address for sending emails.
   - `gmailPass`: Your Gmail account password.

3. Make sure to use a valid Gmail account with the correct credentials to authenticate with Nodemailer.

4. The server
