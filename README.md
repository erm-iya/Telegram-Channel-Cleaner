# **Telegram Channel Cleaner**

This is a script that deletes messages from a Telegram channel *except* for the first and last N messages. This is useful for "pruning" a channel, clearing out the middle history while preserving the beginning and the most recent content.

## **⚠️ WARNING: THIS IS DESTRUCTIVE ⚠️**

This script **PERMANENTLY DELETES** messages. There is no undo button. Use this script at your own risk. It is highly recommended to test it on a private, non-critical channel first.

## **Requirements**

* Python 3.7+  
* The Telethon library

## **Installation**

1. **Install the library:**  
   pip install telethon

2. **Get your Telegram API Credentials:**  
   * Go to [my.telegram.org](https://my.telegram.org) and log in.  
   * Click on "API development tools".  
   * Create a new application. You can fill in "App title" and "Short name" with anything (e.g., "My Cleaner").  
   * You will be given an api\_id and api\_hash. You **MUST** keep these secret.

## **How to Run**

This script is run from your terminal or command prompt. You pass your API credentials and the channel ID as arguments.

**Basic Syntax:**

python telegram\_cleaner.py \<YOUR\_API\_ID\> \<YOUR\_API\_HASH\> \<CHANNEL\_ID\_OR\_USERNAME\>

**Optional Flag:**

* \-k N or \--keep N: Specify the number of messages to keep at the start and end. (Default is 10).

### **Example**

To delete all messages from the channel @mytestchannel *except* for the 10 oldest and 10 newest:

python telegram\_cleaner.py 12345678 "a1b2c3d4e5f6g7h8i9j0" "@mytestchannel"

To delete messages from a private channel, keeping the 20 oldest and 20 newest:

python telegram\_cleaner.py 12345678 "a1b2c3d4e5f6g7h8i9j0" \-100123456789 \-k 20

(Private channel IDs are usually long negative numbers).

### **First-Time Login**

The first time you run the script, Telethon will need to authorize your account:

1. It will ask for your phone number. Enter it in international format (e.g., \+1234567890).  
2. Telegram will send you a login code. Enter the code.  
3. If you have 2FA enabled, it will ask for your password.

After this, the script will create a my\_session.session file. This file securely saves your session, so you **will not** have to log in again. **DO NOT** share this session file.
