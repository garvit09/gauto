from playwright.sync_api import sync_playwright
import pyperclip
import time
from playwright.sync_api import TimeoutError

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
    time.sleep(5)

def is_domain_exists(page, domain):
    try:
        page.wait_for_selector(f"text={domain}", timeout=5000)
        return True
    except TimeoutError:
        return False

def get_existed_and_not_existed_domains(page, new_domains):
    existed_domains = []
    not_existed_domains = []

    for domain in new_domains:
        if is_domain_exists(page, domain):
            existed_domains.append(domain)
        else:
            not_existed_domains.append(domain)

    return existed_domains, not_existed_domains

def print_domain_lists(existed_domains, not_existed_domains):
    print("Domains that already exist:")
    for domain in existed_domains:
        print(f"- {domain}")

    print("\nDomains that do not exist:")
    for domain in not_existed_domains:
        print(f"- {domain}")
    print("----------------------------------")


def add_domains(page, not_existed_domains):
    added_domains = []

    for domain in not_existed_domains:
        retries = 0
        max_retries = 5  # Adjust as needed
        retry_sleep_time = 5  # Optional sleep time between retries (in seconds)

        while retries <= max_retries:
            try:
                total_time_elapsed = 0

                # Attempt to add the domain
                start_time = time.time()
                page.reload()
                time.sleep(10)
                page.get_by_label("Add a domain").click()
                time.sleep(3)
                print(f"Adding Domain: {domain}")
                page.get_by_label("Enter domain name").click()
                page.get_by_label("Enter domain name").fill(domain)
                print(f"Entered the domain name: {domain}")
                page.get_by_role("button", name="Add domain and start").click()
                print(f"Add domain and start for domain: {domain}")

                # Check for the error message
                error_selector = "div.GroiIe:has-text('This domain name has already been used as an alias or domain.')"
                if page.is_visible(error_selector):
                    print(f"Error: This domain name has already been used as an alias or domain. for domain {domain}")
                    break  # Move to the next domain

                # page.goto(f"https://admin.google.com/ac/signup/setup/v2/verify/txt?cid=03n4hx35&sdn={domain}")
                time.sleep(5)
                page.get_by_label("NEXT: GO TO STEP").click()
                time.sleep(5)
                print(f"NEXT: GO TO STEP for domain: {domain}")
                page.get_by_label("Click to copy the record").click()

                # ... (rest of the code remains unchanged)

                elapsed_time = time.time() - start_time
                total_time_elapsed += elapsed_time
                print(f"Time taken for attempt {retries + 1}: {elapsed_time} seconds")

                # If successful, break out of the loop
                added_domains.append(domain)
                break

            except TimeoutError as timeout_error:
                print(f"Timeout error occurred. Details: {timeout_error}")
                # Add debugging information about the current page state
                print(f"Current URL: {page.url}")
                print(f"Page title: {page.title}")
                print(f"Domain {domain} not added successfully. Retrying...")

                # Reload the page before retrying
                page.reload()
                time.sleep(7)

                retries += 1
                if retries <= max_retries:
                    print(f"Waiting for {retry_sleep_time} seconds before the next attempt...")
                    time.sleep(retry_sleep_time)
                continue

            except Exception as e:
                print(f"Error occurred while adding domain {domain}. Details: {e}")
                retries += 1
                if retries <= max_retries:
                    print(f"Waiting for {retry_sleep_time} seconds before the next attempt...")
                    time.sleep(retry_sleep_time)
                continue

        if retries > max_retries:
            print(f"Max retries reached for domain {domain}. Moving to the next domain...")

        print("----------------------------------")

    return added_domains

def print_results(existed_domains, not_existed_domains, added_domains):
    print("\nResults:")
    print("--------")
    if existed_domains:
        print("Domains that already exist:")
        for domain in existed_domains:
            print(f"- {domain}")
    else:
        print("No domains already exist.")

    print("\nDomains that do not exist:")
    for domain in not_existed_domains:
        print(f"- {domain}")

    if added_domains:
        print("\nDomains added successfully:")
        for domain in added_domains:
            print(f"- {domain}")
    else:
        print("No domains added.")

# List of domains to process
domains_to_process = ["smartcheckemail.com", "smartcheckemail.in", "themagicallyverify.com", "themagicallyverify.in", 
                      "trymagically.in", "trymagicallyverify.com", "trymagicallyverify.in", "tryverifier.in", "tryverify.in",
                      "usemagically.in", "thebettablue.com", "magicallyverify.com", "themonkadvisor.com" ]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    login(page)

    # Get existed and not existed domains
    existed_domains, not_existed_domains = get_existed_and_not_existed_domains(page, domains_to_process)

    # Print existed and not existed domains
    print_domain_lists(existed_domains, not_existed_domains)

    if not_existed_domains:
        # Add domains that do not exist
        added_domains = add_domains(page, not_existed_domains)
    else:
        added_domains = []

    # Print the final results
    print_results(existed_domains, not_existed_domains, added_domains)

    context.close()
    browser.close()


