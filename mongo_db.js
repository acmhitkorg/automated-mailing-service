const { MongoClient } = require('mongodb');
const { MONGODB_URI } = require('./configure');

/**
 * Connects to the MongoDB database.
 * @returns {import('mongodb').Db} The connected database instance.
 * @throws {Error} If there's an error connecting to the database.
 */
async function connectToDatabase() {
  try {
    const client = new MongoClient(MONGODB_URI, { useUnifiedTopology: true });
    await client.connect();
    return client.db();
  } catch (error) {
    console.error('Error connecting to the database:', error);
    throw error;
  }
}

module.exports = {
  MongoClient,
  connectToDatabase,
};
