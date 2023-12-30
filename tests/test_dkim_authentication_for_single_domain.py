from playwright.sync_api import Playwright, sync_playwright, expect
import time

# List of domains to iterate through
domains = []  # Empty list to store domains

def test_dkim_authentication(playwright: Playwright, target_domain: str) -> None:
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
    time.sleep(5)
    print("Signed into the landing page....")
    page.goto("https://admin.google.com/u/2/ac/apps/gmail/authenticateemail")
    print("Redirecting to authenticateemail page")

    # Extract the list of domains and add them to the 'domains' list
    domains = page.locator(".vRMGwf").inner_text().split("\n")
    print("Domains: ", domains)

    # Check if the target domain exists in the list
    if target_domain not in domains:
        print(f"Target domain '{target_domain}' does not exist.")
    else:
        print("Target domain '{target_domain}' Exist.")
    
        # Close the browser
        context.close()
        browser.close()
        return
    
    #checking domain
    for domain in domains:
        if domain != target_domain:
            continue

        # Select the specific domain
        page.click(f'.vRMGwf:has-text("{domain}")')
        print("Generating DNS record for the domain: ", domain)
        page.get_by_role("button", name="Generate new record").click()

        # Extract data values into a list
        options = page.evaluate('''() => {
            const options = Array.from(document.querySelectorAll('.ur98K .jgvuAb [data-value]'));
            return options.map(option => option.textContent);
        }''')

        # Remove duplicates from the options list
        unique_options = list(set(options))
        filtered_options = [data_value for data_value in unique_options if data_value in ["2048", "1024"]]
        print("Selected DKIM key bit length drop-down values: ", filtered_options)

        # Define authentication_status_checked outside the loop
        authentication_status_checked = False

        # Iterate over each option
        for data_value in filtered_options:
            print("Selected DKIM key bit length: ", data_value)
            # Perform actions specific to each option
            if data_value == "2048" or data_value == "1024":
                # Using JavaScript to click the element
                page.evaluate(f'''() => {{
                    const option = document.querySelector('.ur98K .jgvuAb [data-value="{data_value.strip()}"]');
                    if (option) {{
                        option.click();
                        return true;
                    }} else {{
                        return false;
                    }}
                }}''')
                time.sleep(2)

                # Click "Generate"
                page.get_by_role("button", name="Generate").click()

                dns_record_generated = page.locator(".SysJ4e").is_enabled()
                print("dns_record_generated: ", dns_record_generated)

                # If the record is not generated, regenerate and continue
                if not dns_record_generated:
                    # Click "Generate new record" or any other action to regenerate the record
                    page.get_by_role("button", name="Generate new record").click()

                    # Add a delay if needed before retrying
                    time.sleep(2)

                    # Check again if the DNS record is generated
                    dns_record_generated = page.locator(".SysJ4e").exists()

                while True:
                    # Additional actions for DNS record generation
                    page.get_by_role("button", name="Start authentication").click()
                    time.sleep(2)

                    status_element = page.locator(".UW1bKe strong").nth(0)

                    if status_element and not authentication_status_checked:
                        status_text = status_element.inner_text().strip()
                        print("Authentication Status text: ", status_text)
                        authentication_status_checked = True  # Set the flag to True

                    # Check the authentication status
                    if authentication_status_checked and (status_text == "Authenticated" or status_text == "Not authenticating email"):
                        # Break out of the loop if authentication status is checked
                        if status_text == "Authenticated":
                            print("Authentication successful!")
                            break
                        else:
                            print("Not authenticating email")

        # Close the browser
        context.close()
        browser.close()

# Specify the target domain
target_domain = "tryverifier.in"

with sync_playwright() as playwright:
    test_dkim_authentication_result = test_dkim_authentication(playwright, target_domain)
