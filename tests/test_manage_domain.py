from playwright.sync_api import Playwright, sync_playwright, expect
import pyperclip
import time


def test_manage_domain(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
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
    # page.goto("https://admin.google.com/ac/domains/manage?pli=1&rapt=AEjHL4O0wGIU7y_GAmgJI-2Czlv2ll6U1GaIPghHxzY7vw8ZVl1K60nlYaIsaXjpAD7RygQQQhup0hafFZngeQ8oFRn74bdFUnSYQ0RIjf_WXSH4VBaWNh0")
    page.get_by_label("Add a domain").click()
    print("Adding Domain")
    page.get_by_label("Enter domain name").click()
    page.get_by_label("Enter domain name").fill("help.dnsfilter.com")
    print("Entered the Domain name")
    page.get_by_role("button", name="Add domain and start").click()
    print("Adding Domain")
    page.goto("https://admin.google.com/ac/signup/setup/v2/verify/txt?cid=03n4hx35&sdn=help.dnsfilter.com&admin_return_url=https%3A%2F%2Fadmin.google.com%2Fac%2Fdomains%2Fmanage%3Fpli%3D1%26rapt%3DAEjHL4O0wGIU7y_GAmgJI-2Czlv2ll6U1GaIPghHxzY7vw8ZVl1K60nlYaIsaXjpAD7RygQQQhup0hafFZngeQ8oFRn74bdFUnSYQ0RIjf_WXSH4VBaWNh0")
    page.get_by_label("NEXT: GO TO STEP").click()
    print("clicking on the NEXT: GO TO STEP")
    page.get_by_label("Click to copy the record").click()
    # Retrieve the clipboard content using pyperclip
    clipboard_content = pyperclip.paste()
    print("clipboard_content copied successfully")
    print("clipboard_content: ",clipboard_content)
    time.sleep(2)
    page.get_by_label("VERIFY DOMAIN").click()
    print("clicked on VERIFY DOMAIN")
    time.sleep(30)
    page.get_by_label("Close dialogue").click()
    print("Close dialogue")
    # Check for "Verify domain" link
    # verify_domain_link = page.locator('[data-action-id="ACTIVATE_DOMAIN"]').first_child()
    # if verify_domain_link:
    #     verify_domain_link.click()
    #     print("Clicked on Verify domain")
    #     time.sleep(2)

    #     # Check for "Verified and Activate Gmail" link
    #     activate_gmail_link = page.locator('.RveJvd.snByac').first_child()
    #     if activate_gmail_link:
    #         activate_gmail_link.click()
    #         print("Clicked on Activate Gmail")
    #         time.sleep(2)

    #         # Click "Next"
    #         page.get_by_label("Next").click()
    #         print("Clicked on Next")

    context.close()
    browser.close()


with sync_playwright() as playwright:
    test_manage_domain_result = test_manage_domain(playwright)
