from playwright.sync_api import sync_playwright
import pyperclip
import time

def login(page):
    page.goto("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fadmin.google.com%2Fu%2F2%2Fac%2Fdomains%2Fmanage&followup=https%3A%2F%2Fadmin.google.com%2Fu%2F2%2Fac%2Fdomains%2Fmanage&ifkv=ASKXGp2kzA9nPrXbpIyeqziljk3WN-eoHGFN_CNgIwYOu8u3PTa6zF_rIU0dHg0POWS9udShJZ26&osid=1&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1190938480%3A1703657885253519&theme=glif")
    page.get_by_label("Email or phone").click()
    page.get_by_label("Email or phone").fill("saksham@tryverifier.in")
    page.get_by_role("button", name="Next").click()
    page.get_by_label("Enter your password").click()
    page.get_by_label("Enter your password").fill("Thedayisgood@1.")
    page.get_by_label("Show password").check()
    page.get_by_label("Show password").uncheck()
    page.get_by_role("button", name="Next").click()
    print("Signed into the landing page....")

def add_domain(page, domain):
    page.get_by_label("Add a domain").click()
    print(f"Adding Domain: {domain}")
    page.get_by_label("Enter domain name").click()
    page.get_by_label("Enter domain name").fill(domain)
    print(f"Entered the domain name: {domain}")
    page.get_by_role("button", name="Add domain and start").click()
    print(f"Add domain and start for domain: {domain}")

    page.goto(f"https://admin.google.com/ac/signup/setup/v2/verify/txt?cid=03n4hx35&sdn={domain}&admin_return_url=https%3A%2F%2Fadmin.google.com%2Fac%2Fdomains%2Fmanage%3Fpli%3D1%26rapt%3DAEjHL4O0wGIU7y_GAmgJI-2Czlv2ll6U1GaIPghHxzY7vw8ZVl1K60nlYaIsaXjpAD7RygQQQhup0hafFZngeQ8oFRn74bdFUnSYQ0RIjf_WXSH4VBaWNh0")
    page.get_by_label("NEXT: GO TO STEP").click()
    print(f"NEXT: GO TO STEP for domain: {domain}")
    page.get_by_label("Click to copy the record").click()

    # Retrieve the clipboard content using pyperclip
    clipboard_content = pyperclip.paste()
    print(f"Clipboard content for {domain}: {clipboard_content}")

    time.sleep(3)
    page.get_by_label("VERIFY DOMAIN").click()
    print(f"Verifying the domain: {domain}")
    # page.get_by_label("Close dialogue").click()
    page.click("[aria-label='Close dialogue']")
    page.wait_for_load_state("domcontentloaded")
    print("domcontentloaded....")

# List of domains to process
domains_to_process = ["smartcheckemail.com", "smartcheckemail.in", "themagicallyverify.com", "themagicallyverify.in", 
                      "trymagically.in", "trymagicallyverify.com", "trymagicallyverify.in", "tryverifier.in", "tryverify.in",
                      "usemagically.in", "thebettablue.com", "magicallyverify.com", "themonkadvisor.com" ]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    login(page)

    for domain in domains_to_process:
        add_domain(page, domain)

    context.close()
    browser.close()
