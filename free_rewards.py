import imaplib
import email
import re
from email.header import decode_header
from playwright.sync_api import sync_playwright
import time
import os

imap_server, port = "imap.gmail.com", 993
email_address = "maximistr100@gmail.com"
password =  os.getenv('EMAIL_CODE')
verification_code = None

with sync_playwright() as p:
    # 1. Launch with arguments that strip away bot indicators
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled", # Hides webdriver flag
            "--no-sandbox",
            "--disable-infobars",
            "--window-size=1920,1080"
        ]
    )
    
    # 2. Create a realistic browser context
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=1,
        is_mobile=False,
        has_touch=False,
        locale="en-US"
    )
    
    # 3. Inject JavaScript to explicitly delete the webdriver property
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)
    
    page = context.new_page()
    page.goto("https://store.supercell.com/brawlstars")

    # .all() converts the locator group into a Python list of individual elements
    page.get_by_role("button", name="Accept All Cookies").click()
    time.sleep(1)
    #print(page.locator("body").inner_text())
    # Looks for any link tag where the class name starts with 'LoginButton_LoginButton'
    page.locator("a[class^='LoginButton_LoginButton']").first.click()
    time.sleep(1)
    #print(page.locator("body").inner_text())
    page.get_by_placeholder("Enter your email").press_sequentially(email_address, delay=100)
    time.sleep(3)
    page.get_by_role("button", name="LOG IN").click()
    time.sleep(10)  # Wait for the email to arrive and be processed

    try:
        print("Connecting to the mailbox...")
        mail = imaplib.IMAP4_SSL(imap_server, port)
        mail.login(email_address, password)
        mail.select("INBOX")
        
        status, data = mail.search(None, "ALL")
        mail_ids = data[0].split()[-5:]
        
        for mail_id in mail_ids:
            status, message_data = mail.fetch(mail_id, "(RFC822)")
            for response_part in message_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    from_sender = decode_header(msg["From"])[0][0]
                    from_sender = from_sender.decode() if isinstance(from_sender, bytes) else from_sender

                    if "Supercell" in from_sender and "noreply@id.supercell.com" in from_sender:
                        subject = decode_header(msg["Subject"])[0][0]
                        subject = subject.decode() if isinstance(subject, bytes) else subject
                        verification_code = re.sub(r'\s+', '', re.search(r'\[([^\]]+)\]', subject).group(1))
                        break
        mail.close()
        mail.logout()
        print(f"Verification code: {verification_code}")
        
    except Exception as e:
        print(f"Error: {e}")
        
    if verification_code:
        page.locator("input[name='pin']").press_sequentially(verification_code, delay=100)
        time.sleep(2)
        page.get_by_role("button", name="Continue").click()
        time.sleep(5)
        page.get_by_role("button", name="Claim").click()
