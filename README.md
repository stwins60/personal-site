Updated README:

# Personal Site

## Description
This repository contains code to build a Docker image for a personal site.

## Prerequisites
- Docker installed on your system.
- Knowledge of setting environment variables.
- Information about setting up RECAPTCHA keys.

## Setup
1. Clone the repository.
2. Modify the Dockerfile to include the correct RECAPTCHA keys.
3. Build the Docker image using the command: `docker build -t personal-site .`

## Usage
- To run the Docker image, use the command: `docker run -d -e RECAPTCHA_SECRET_KEY=<your_secret_key> -e RECAPTCHA_SITE_KEY=<your_site_key> personal-site`

## Contributing
- Fork the repository.
- Make changes.
- Submit a pull request.

## Credits
- Third-party APIs used: OpenAI, Gemini, Groq AI.

## License
This project is licensed under the MIT License.

## Contact
For any questions or feedback, contact the project maintainers.
