# Email Service API Documentation

**Description:**

- This API allows you to manage email recipients and send emails to those recipients using a MongoDB database and a Gmail SMTP server.

**Before proceeding with the API, make sure to configure the `config.py` file with your own details and links.**

**Endpoints:**

- **GET /:**

  - **Method:** GET
  - **Summary:** Get information about the API.
  - **Description:** Provides an overview of the API, its purpose, and the available endpoints.

- **GET /recipient_list:**

  - **Method:** GET
  - **Summary:** Get a list of email addresses of recipients.
  - **Description:** Retrieves a list of email addresses from the MongoDB collection.
  - **Response:** List of email addresses, e.g., ["email1@example.com", "email2@example.com", "..."]

- **POST /push_new_recipient:**

  - **Method:** POST
  - **Summary:** Add a new recipient.
  - **Description:** Adds a new recipient to the MongoDB collection.
  - **Request:**
    ```
    {
        "name": "John Doe",
        "email": "johndoe@example.com"
    }
    ```
  - **Response:**
    ```
    {
        "message": "Data inserted successfully"
    }
    ```

- **POST /send_mail:**
  - **Method:** POST
  - **Summary:** Send an email.
  - **Description:** Sends an email to all recipients in the MongoDB collection.
  - **Request:**
    ```
    {
        "subject": "sample subject",
        "body": "sample body"
    }
    ```
  - **Response:**
    ```
    {
        "status": "mail sent successfully"
    }
    ```

**Note:**

- Before using the API, ensure that you modify the `config.py` file with your own configuration details and links. This includes setting up the MongoDB connection and providing the necessary Gmail SMTP server details to enable the email sending functionality. Failure to configure these settings correctly may result in errors or unsuccessful email delivery.
