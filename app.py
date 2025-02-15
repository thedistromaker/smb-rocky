from flask import Flask, jsonify
from samba_info import update_data
import logging

# Set up logging for the Flask app
logging.basicConfig(filename='flask_app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

@app.route('/update_data', methods=['GET'])
def get_data():
    logging.info("Request received for data update.")
    data = update_data()
    
    if 'error' in data:
        logging.error(f"Data update failed: {data['error']}")
        return jsonify(data), 500

    # Log successful response
    logging.info("Data update successful, sending response to frontend.")
    return jsonify(data)

if __name__ == '__main__':
    logging.info("Starting Flask application.")
    app.run(debug=True, host='0.0.0.0', port=5000)
