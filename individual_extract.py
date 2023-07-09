import requests
from bs4 import BeautifulSoup
import csv
import os


def write_to_file(category, name, address, telephone):
    filename = f"{category}.csv"

    # Check if the file already exists
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write header if the file doesn't exist
        if not file_exists:
            writer.writerow(["Name", "Address", "Telephone"])

        writer.writerow([name, address, telephone])


def get_company_detail(url):

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    company_detail = soup.find("div", class_="cmp_details_in")

    name = "-"
    address = "-"
    telephone = "-"
    mobile_phone = "-"

    try:
        name = company_detail.find(id="company_name").text.strip()
    except:
        name = "Unknown"

    try:

        address_div = company_detail.find("div", class_="location")
        address = address_div.contents[0].strip()
    except:
        address = "unknown"
    try:
        phone_number_div = company_detail.find("div", class_="text phone")
        telephone = phone_number_div.text.strip()
    except:
        telephone = "unknown"

    try:
        mobile_phone_div = company_detail.find(
            "div", class_="label", text="Mobile phone"
        )
        mobile_phone = mobile_phone_div.find_next_sibling("div").text.strip()
    except:
        mobile_phone = ","

    return (name, address, f"{telephone},{mobile_phone},")


def get_category_detail(url):

    response = requests.get(url)
    category = url.split("/")
    if len(category) >= 6:
        category = category[-2]
    else:
        category = category[-1]
    category = category.lower()

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    listings = soup.find("div", id="listings")
    companies = listings.find_all("div", class_="company")
    count = 0

    for company in companies:
        if '<ins class="adsbygoogle" data-ad-client' not in company.text:
            company_ = company.find("a")
            count += 1
            try:

                company_url = company_["href"]
                name, address, telephone = get_company_detail(
                    f"https://www.nepalyp.com{company_url}"
                )
                write_to_file(category, name, address, telephone)

            except Exception as e:
                print(count, e)
                continue

    try:
        pagination = soup.find("div", class_="pages_container")
        if pagination:
            next_page = pagination.find("a", rel="next")
            if next_page:
                next_page_url = next_page["href"]
                print("NEXT PAGE URL")
                print(next_page_url)
                name, address, telephone = get_category_detail(
                    f"https://www.nepalyp.com{next_page_url}"
                )
                write_to_file(category, name, address, telephone)
    except:
        pass


if __name__ == "__main__":
    get_category_detail("https://www.nepalyp.com/category/Security_services")
    # get_company_detail(
    #     "https://www.nepalyp.com/company/29786/Nepal_Security_Guard_Supply_Service_P_Ltd"
    # )
