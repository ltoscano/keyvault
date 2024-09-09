import os
import json
import logging
from flask import Flask, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '../.secrets', 'config.json')

def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {CONFIG_FILE_PATH}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in configuration file: {CONFIG_FILE_PATH}")
        return {}

@app.route('/get_key/<key_name>', methods=['GET'])
def get_key(key_name):
    config = load_config()
    if key_name in config:
        logger.info(f"Key retrieved: {key_name}")
        return jsonify({key_name: config[key_name]})
    else:
        logger.warning(f"Key not found: {key_name}")
        return jsonify({"error": "Key not found"}), 404

@app.route('/list_keys', methods=['GET'])
def list_keys():
    config = load_config()
    keys = list(config.keys())
    logger.info(f"Listed {len(keys)} keys")
    return jsonify({"keys": keys})

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

def run_server():
    host = os.environ.get('KEYVAULT_HOST', '0.0.0.0')
    port = int(os.environ.get('KEYVAULT_PORT', 38680))
    app.run(host=host, port=port)

if __name__ == '__main__':
    run_server()