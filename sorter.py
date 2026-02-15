import imaplib
import email
import os
from email.header import decode_header

# 1. Configuration from Environment Variables
IMAP_SERVER = "imap.gmail.com"  # Change to your provider's IMAP if not Gmail
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

RULES = {
    "invoice": "Finance",
    "receipt": "Finance",
    "newsletter": "Read Later",
    "meeting": "Work",
    "urgent": "Priority"
}

def connect_to_mail():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        return mail
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

def clean_header(header_val):
    """Decodes email headers safely."""
    decoded, encoding = decode_header(header_val)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding or "utf-8")
    return decoded

def run_sorter():
    mail = connect_to_mail()
    if not mail: return

    mail.select("inbox")
    # Search for all unread (UNSEEN) emails
    status, messages = mail.search(None, 'UNSEEN')
    
    if status != 'OK' or not messages[0]:
        print("No new emails to sort.")
        mail.logout()
        return

    for num in messages[0].split():
        # Fetch email headers
        res, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = clean_header(msg["Subject"]).lower()
                sender = clean_header(msg["From"]).lower()
                
                print(f"Processing: {subject}")

                # Check rules
                target_folder = None
                for keyword, folder in RULES.items():
                    if keyword in subject or keyword in sender:
                        target_folder = folder
                        break
                
                # Move the email
                if target_folder:
                    mail.create(target_folder)
                    mail.copy(num, target_folder)
                    mail.store(num, '+FLAGS', '\\Deleted')
                    print(f"Moved to {target_folder}")

    # Permanently remove emails marked for deletion from Inbox
    mail.expunge()
    mail.logout()
    print("Sorting complete.")

if __name__ == "__main__":
    run_sorter()
