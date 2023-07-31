// Import required modules
const express = require('express');
const nodemailer = require('nodemailer');
const path = require('path');
const { MongoClient, connectToDatabase } = require('./mongo_db');
const { MONGODB_URI, MONGODB_COLLECTION_NAME, EMAIL_ADDRESS, EMAIL_PASSWORD, PORT } = require('./configure');

// Create an Express application
const app = express();

// Middleware to parse incoming JSON data
app.use(express.json());

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

// Create a Nodemailer transporter
const transporter = nodemailer.createTransport({
  service: 'Gmail', // You can replace 'Gmail' with your email service provider
  auth: {
    user: EMAIL_ADDRESS,
    pass: EMAIL_PASSWORD,
  },
});

// Endpoint for the root route
app.get('/', (req, res) => {
  res.send('Welcome to the Email Sender API!');
});

// Endpoint to send an email
app.post('/send-email', async (req, res) => {
  const { to, subject, text } = req.body;

  try {
    // Connect to the MongoDB database
    const db = await connectToDatabase();

    // Retrieve all email recipients from the 'recipients' collection
    const recipientsCollection = db.collection(MONGODB_COLLECTION_NAME);
    const recipients = await recipientsCollection.find({}).toArray();

    // Extract the email addresses from the 'email' field of each recipient
    const allRecipients = recipients.map((recipient) => recipient.email);

    // Define the email options
    const mailOptions = {
      from: EMAIL_ADDRESS,
      to: allRecipients.join(','), // Join the email addresses into a comma-separated string
      subject,
      text,
      attachments: [], // Initialize an empty array for attachments
    };

    // Check if the request contains an 'imagePath' field
    if (req.body.imagePath) {
      // Get the absolute path of the image file
      const imagePath = path.join(__dirname, req.body.imagePath);

      // Add the image file as an attachment
      mailOptions.attachments.push({
        path: imagePath,
      });
    }

    // Send the email using the Nodemailer transporter
    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        console.log('Error sending email:', error);
        res.status(500).json({ error: 'Failed to send email' });
      } else {
        console.log('Email sent:', info.response);
        res.status(200).json({ message: 'Email sent successfully' });
      }
    });

  } catch (error) {
    console.log('Error sending email:', error);
    res.status(500).json({ error: 'Failed to send email' });
  }
});
