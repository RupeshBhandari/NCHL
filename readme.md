# NCHL Integration

## Overview

This project is designed to handle secure transaction requests using a PKCS#12 (.pfx) file for signing. It reads configuration from a file, processes transaction details, signs messages, and sends HTTP requests with the signed data. It also includes logging for tracking and debugging purposes.

## Prerequisites

- Python 3.x
- Required Python packages (see `requirements.txt`)

## Installation

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The project requires a configuration file named `config/config.json`. This file should contain the following settings:

- **PKCS#12 File Path:** Path to the PKCS#12 (.pfx) file used for signing.
- **PKCS#12 Password:** Password for the .pfx file.
- **Request URL:** URL where the POST request will be sent.
- **Transaction Details:** Details of the transaction to be signed and sent.
- **HTTP Headers:** Headers for the HTTP request.
- **Authentication:** Credentials for authenticating the request.
- **Log File Path:** Path to the log file where application logs will be stored.
```json
{
    "pfx_path": "path/to/your/credentials.pfx",
    "pfx_password": "your_pfx_password",
    "url": "https://example.com/api/endpoint",
    "transaction_details": {
        "merchantId": "your_merchant_id",
        "appId": "your_app_id",
        "referenceId": "your_reference_id",
        "txnAmt": "your_transaction_amount"
    },
    "headers": {
        "Content-Type": "application/json"
    },
    "auth": {
        "username": "your_username",
        "password": "your_password"
    },
    "log_file": "path/to/your/logfile.log"
}

```

Ensure that `config/config.json` is properly set up before running the script.

## Usage

To execute the main script and perform the transaction request, run:

```bash
python src/main.py
```

The script will:

1. Load configuration from `config/config.json`.
2. Create a message from transaction details.
3. Sign the message using the PKCS#12 file.
4. Prepare the payload and send a POST request.
5. Log the request and response details.

## Logging

Logs are managed according to the configuration specified in the `config/config.json` file. By default, logs are written to both a file and the console.

## Folder Structure
```
project-root/
│
├── src/
│   ├── main.py
│   ├── signing.py
│   └── config/
│       ├── __init__.py
│       ├── config_loader.py
│       └── config.json
│
├── logs/
│   └── logs.log
│
├── config/
│   ├── __init__.py
│   ├── config_loader.py
│   └── config.json
│
├── venv/
│   └── (virtual environment files)
│
├── README.md
└── requirements.txt
└── .gitignore
```

## Development

To contribute or modify the code:

1. Create a new branch:

    ```bash
    git checkout -b <branch-name>
    ```

2. Make your changes and commit them:

    ```bash
    git add .
    git commit -m "Description of changes"
    ```

3. Push to the remote repository:

    ```bash
    git push origin <branch-name>
    ```

4. Open a pull request on GitHub.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

