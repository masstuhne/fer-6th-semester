import sys
import re
import urllib.request
from urllib.parse import urlparse


class Constants:
    EXIT_SUCCESS = 0,
    EXIT_FAILURE = 1


def handle_exit(exit_code, exit_message):
    print("Error message: " + exit_message)
    sys.exit(exit_code)


def fetch_webpage(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf8')
    except Exception as e:
        handle_exit(Constants.EXIT_FAILURE, f"Error fetching the webpage: {e}")


def find_links(content):
    return re.findall(r'href="(http[s]?://[^"]+)"', content)


def find_hosts(links):
    hosts = {}
    for link in links:
        parsed_url = urlparse(link)
        host = parsed_url.netloc
        if host in hosts:
            hosts[host] += 1
        else:
            hosts[host] = 1
    return hosts


def find_emails(content):
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)


def count_images(content):
    return len(re.findall(r'<img [^>]*src="[^"]+"', content))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        handle_exit(Constants.EXIT_FAILURE, "Students.txt does not exist in the given directory!")

    page_url = sys.argv[1]

    page_content = fetch_webpage(page_url)
    print(page_content)

    links = find_links(page_content)
    print("\nLinks found:")
    for link in links:
        print(link)

    hosts = find_hosts(links)
    print("\nHosts found:")
    for host, count in hosts.items():
        print(f"{host}: {count} references")

    emails = find_emails(page_content)
    print("\nEmail addresses found:")
    for email in emails:
        print(email)

    image_count = count_images(page_content)
    print(f"\nNumber of image links: {image_count}")
