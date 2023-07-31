// MongoDB connection configuration
const MONGODB_URI = 'Your_mongodb_connection_string/Your_database_name';
const MONGODB_COLLECTION_NAME = 'email2';

// Email configuration
const EMAIL_ADDRESS = 'Your_email_ID';
const EMAIL_PASSWORD = 'Your_app_password';

// Server configuration
const PORT = 5000;

module.exports = {
  // MongoDB connection settings
  MONGODB_URI,
  MONGODB_COLLECTION_NAME,

  // Email settings
  EMAIL_ADDRESS,
  EMAIL_PASSWORD,

  // Server settings
  PORT,
};
