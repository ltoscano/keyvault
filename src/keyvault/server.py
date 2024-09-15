import argparse
import json
import logging
import os
from pathlib import Path
from flask import Flask, jsonify, request
from waitress import serve

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in configuration file: {config_path}")
        return {}

@app.route('/get_key/<key_name>', methods=['GET'])
def get_key(key_name):
    if key_name in app.config['keys']:
        logger.info(f"Key retrieved: {key_name}")
        return jsonify({key_name: app.config['keys'][key_name]})
    else:
        logger.warning(f"Key not found: {key_name}")
        return jsonify({"error": "Key not found"}), 404

@app.route('/list_keys', methods=['GET'])
def list_keys():
    keys = list(app.config['keys'].keys())
    logger.info(f"Listed {len(keys)} keys")
    return jsonify({"keys": keys})

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

def main():
    parser = argparse.ArgumentParser(description="KeyVault Server")
    parser.add_argument("--config", default="~/.keyvault/config.json", help="Path to config.json")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=38680, help="Port to run the server on")
    args = parser.parse_args()

    config_path = os.path.expanduser(args.config)
    app.config['keys'] = load_config(config_path)

    logger.info(f"Starting KeyVault server on {args.host}:{args.port}")
    serve(app, host=args.host, port=args.port)

if __name__ == '__main__':
    main()