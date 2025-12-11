# 🏦 Secure Bank System with Access Control (DAC)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-SHA256%20%2B%20Salt-red?style=for-the-badge)

A robust command-line banking simulation that implements **Discretionary Access Control (DAC)**. This system allows users to securely manage their funds and explicitly control who has permission to view their financial data.

The project demonstrates core cybersecurity concepts including **Hashing**, **Salting**, **OTP Verification**, and **Permission Matrices**.

---

## 📋 Project Overview

The goal of this project is to implement a secure banking environment where access rights are determined by the data owner. It adheres to the following core requirements:
1.  **Self-Access:** Users can view their own account balance.
2.  **Grant Access:** User A can grant User B the ability to view User A’s balance.
3.  **Revoke Access:** User A can revoke User B's access rights at any time.

---

## 🚀 Features

### 🔐 Security & Authentication
* **Secure Registration:** Validates phone numbers against a pre-approved bank registry.
* **OTP Verification:** Simulates SMS 2FA using Windows Toast Notifications (via `plyer`).
* **Password Hardening:**
    * **SHA-256 Hashing:** No plaintext passwords stored.
    * **Cryptographic Salting:** Unique 16-byte random hex salt per user to thwart rainbow table attacks.
* **Input Validation:** Sanitizes user inputs to prevent crashes and logical errors.

### 🛡️ Access Control (DAC)
* **Access Matrix:** Implements a permission matrix loaded into memory for O(1) lookup speed.
* **Granular Permissions:** Users act as administrators of their own data, granting/revoking read access to specific other users.

### 💾 Data Persistence
* **JSON Database:** Uses persistent local storage for:
    * User Balances
    * Access Matrices
    * Hashed Passwords & Salts
    * Phone Registries

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Libraries:**
    * `hashlib` (Cryptography)
    * `json` (Data Storage)
    * `plyer` (Notifications)
    * `os` & `random` (System & Randomness)

---

## ⚙️ Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/AbdoAli003/Bank-System-with-Access-Control.git
    cd Bank-System-with-Access-Control
    ```

2.  **Install Dependencies**
    This project requires the `plyer` library for desktop notifications.
    ```bash
    pip install plyer
    ```

3.  **Run the Application**
    ```bash
    python main.py
    ```
    *> Note: On the first run, the system will automatically generate all necessary JSON database files and populate the phone registry.*

---

## 📖 Usage Guide

### 1. Registration
* Select **"Register New User"** from the main menu.
* Enter one of the valid phone numbers generated in `phone_numbers.json`.
* Enter the **OTP Code** that appears in the Windows popup.
* Set your **Username** and **Password**.

### 2. Managing Access (The DAC System)
* **Grant Access:** * Choose option `3`.
    * Enter the username of the person you trust (e.g., "Friend1").
    * *Result:* "Friend1" can now see your balance.
* **Revoke Access:**
    * Choose option `4`.
    * Enter the username to block (e.g., "Friend1").
    * *Result:* "Friend1" receives an "ACCESS DENIED" message if they try to view your balance.

### 3. Viewing Funds
* **Your Balance:** Option `1` displays your own funds.
* **Others' Balance:** Option `2` asks for a target username. The system checks the **Access Matrix** before displaying data.

---

## 📂 Project Structure

```text
├── main.py                   # Core application logic
├── accounts_database.json    # User balances
├── password_file.json        # SHA-256 hashed passwords
├── passwords_salts.json      # Unique user salts
├── access_matrix.json        # DAC permission storage
├── phone_numbers.json        # Registry of valid bank numbers
└── users_phones.json         # Map of taken phone numbers
