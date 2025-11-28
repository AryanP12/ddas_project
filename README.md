# DDAS - Data Download Duplication Alert System 🚀

DDAS is a smart client-server architecture designed to reduce data redundancy in institutional environments. It prevents users from unknowingly downloading duplicate datasets, saving bandwidth and storage space.

## 🌟 Features

* **Real-time Interception:** Detects downloads in the browser before they complete.
* **Duplicate Detection:** Checks against a central database using SHA-256 hashes and Source URLs.
* **Smart Alerts:** Notifies the user if a file already exists within the network.
* **Race Condition Handling:** Automatically deletes files that finish downloading before the user acts on the alert.
* **Location Tracking:** Tells the user exactly where the existing file is located (e.g., `C:\Downloads\data.zip`).

## 🛠️ Tech Stack

* **Backend:** Python, Flask, SQLAlchemy
* **Database:** PostgreSQL (JSONB support for metadata)
* **Client:** Google Chrome Extension (Manifest V3)
* **Tools:** PowerShell, VS Code

## ⚙️ Installation & Setup

### 1. Backend Setup
1.  Clone the repository.
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate # or venv\Scripts\activate on Windows
    ```
3.  Install dependencies:
    ```bash
    pip install Flask Flask-SQLAlchemy psycopg2-binary
    ```
4.  Configure `config.py` with your PostgreSQL credentials.
5.  Run the server:
    ```bash
    python app.py
    ```

### 2. Chrome Extension Setup
1.  Open Chrome and go to `chrome://extensions`.
2.  Enable **Developer Mode**.
3.  Click **Load Unpacked**.
4.  Select the `chrome_extension` folder from this repository.

## 🚀 Usage
1.  Start the Python server.
2.  Try to download a file in Chrome.
3.  If the file has been downloaded previously by *any* user in the network, you will see a popup alert.

---
*Developed by Aryan Padhye*
