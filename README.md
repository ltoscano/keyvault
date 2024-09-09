# KeyVault

## Introduction

Simple, fast, convenient! KeyVault is a simple yet effective solution born out of the growing need to centralize the management of cloud service keys, particularly in development environments. With the proliferation of cloud services, especially those related to Large Language Models (LLMs) and other AI technologies, developers often find themselves juggling multiple API keys and secrets across various projects.

This application addresses the challenge by providing a centralized point for storing and retrieving these keys, streamlining the development process and enhancing security practices. While primarily designed for personal development environments, KeyVault can also serve as a lightweight solution for small teams or projects.

Key features and benefits include:

- Centralized storage of API keys and secrets
- Easy integration with development workflows
- Simplified key management across multiple projects
- Improved security through centralized access control

It's important to note that while KeyVault is a practical solution for development environments, it is not intended as a robust, production-grade secret management system. In production contexts, this solution can be easily replaced by more comprehensive, battle-tested alternatives provided by cloud service providers or specialized secret management tools.

The simplicity and flexibility of KeyVault make it an ideal stepping stone, allowing developers to establish good key management practices in their development workflow, which can then be seamlessly transitioned to more robust solutions in production environments.

## Features

- Secure storage of key-value pairs
- RESTful API for key retrieval and listing
- Python client for easy integration
- Dockerized server for easy deployment
- Logging and improved error handling
- Support for both Docker and Docker Compose deployment
- Easy key management with local volume mapping

## Prerequisites

- Python 3.7+
- Docker and Docker Compose (for containerized deployment)

## Quickstart

1. Clone the repository and navigate to the project directory:
   ```
   git clone https://github.com/yourusername/keyvault.git
   cd keyvault
   ```

2. Create a `.secrets` directory and add your configuration:
   ```
   mkdir .secrets
   echo '{"OPENAI_API_KEY": "your-api-key-here", "OTHER_KEY": "another-key-value"}' > .secrets/config.json
   ```

3. Start the server using Docker Compose:
   ```
   KEYVAULT_PORT=38680 docker-compose up -d
   ```
   You can change the port by modifying the KEYVAULT_PORT environment variable.

4. Verify that the server is running:
   ```
   curl http://localhost:38680/list_keys
   ```

5. Use the client to interact with the server. Create a file named `test_client.py`:

   ```python
   from keyvault.client import KeyVaultClient
   import logging
   import os

   logging.basicConfig(level=logging.INFO)

   # Use environment variables or default values
   host = os.environ.get('KEYVAULT_HOST', 'localhost')
   port = os.environ.get('KEYVAULT_PORT', '38680')

   client = KeyVaultClient(f"http://{host}:{port}")

   try:
      # Get a specific key
      api_key = client.get_key('OPENAI_API_KEY')
      print("API Key:", api_key)

      # List all keys
      keys = client.list_keys()
      print("Available keys:", keys)
   except Exception as e:
      print(f"An error occurred: {str(e)}")
   ```

6. Run the client:
   ```
   python test_client.py
   ```

### Using Docker

1. Build the Docker image:
   ```
   docker build -t keyvault-server .
   ```

2. Run the Docker container, mapping your local `.secrets` directory:
   ```
   docker run -d -p 38680:38680 -v $(pwd)/.secrets:/app/.secrets:ro --name keyvault-server keyvault-server
   ```

The server will be available at `http://localhost:38680`.

## Configuration

Store your keys in the `keyvault/.secrets/config.json` file:

```json
{
  "OPENAI_API_KEY": "your-api-key-here",
  "OTHER_KEY": "another-key-value"
}
```

KeyVault can be configured using the following environment variables:

KEYVAULT_HOST: The host address on which the KeyVault server will listen. Default is 0.0.0.0.
KEYVAULT_PORT: The port on which the KeyVault server will listen. Default is 38680.

You can update this file at any time, and the changes will be immediately reflected in the running container without the need to rebuild or restart.

## Intended Usage and Security Considerations

KeyVault is designed to be used as a component within a development environment, typically composed of multiple containers communicating over a private Docker network. In this setup, each new development project has its own set of containers and communicates with the KeyVault container to retrieve the appropriate keys when needed.

### Best Practices:

1. **Private Network**: It is strongly recommended to run KeyVault on a private Docker network, accessible only to your development containers.

2. **Not for Public Access**: KeyVault should never be exposed to the public internet. It is designed for local development environments only.

3. **Responsible Configuration**: When using KeyVault in a multi-container setup on a private network, it's not necessary to expose the port on the host (i.e., you don't need to use 0.0.0.0). The KeyVault container can be accessed only by other containers on the same private network, enhancing security.

4. **Separate Instances**: For different projects or development environments, consider running separate instances of KeyVault to maintain isolation.

5. **Regular Updates**: Keep your KeyVault instance and its dependencies up to date to ensure you have the latest security patches.

### Example Setup:

Here's a basic example of how you might set up KeyVault in a Docker network without exposing ports to the host:

```yaml
version: '3.8'

networks:
  dev-network:
    driver: bridge

services:
  keyvault:
    build: .
    networks:
      - dev-network
    environment:
      - KEYVAULT_PORT=38680
    volumes:
      - ./.secrets:/app/.secrets:ro

  your-app:
    build: ./your-app
    networks:
      - dev-network
    environment:
      - KEYVAULT_HOST=keyvault
      - KEYVAULT_PORT=38680
    depends_on:
      - keyvault
```

In this setup:
- KeyVault is not exposing any ports to the host system.
- `your-app` can access KeyVault at `http://keyvault:38680` within the `dev-network`.
- KeyVault is not accessible from outside the `dev-network`, providing an additional layer of security.

Remember, the security of your development environment and the keys stored in KeyVault is your responsibility. Always follow best practices for securing sensitive information.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
