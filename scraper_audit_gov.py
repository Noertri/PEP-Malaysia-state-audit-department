from urllib.parse import urljoin
import csv
from datetime import datetime
import httpx
from bs4 import BeautifulSoup


def main():
    base_url = "https://www.audit.gov.my"
    print("Scraping web...")
    client = httpx.Client(follow_redirects=True)
    r = client.get(urljoin(base_url, "directory"))
    souped = BeautifulSoup(r.content, "html.parser")
    rows = souped.select("div.form-group div.row.mt-4")

    page_links = [tag.get("href", "") for tag in rows[-1].select("h5>a")]
    
    results = list()
    for link in page_links:
        r1 = client.get(link)
        souped2 = BeautifulSoup(r1.content, "html.parser")
        tables = souped2.select("div.staff-list.mb-4 .table-responsive table")
        first_row = [col.get_text(strip=True, separator=" ") for col in tables[0].select("tbody tr")[0].select("td")]
        second_row = [col.get_text(strip=True, separator=" ") for col in tables[1].select("tbody tr")[0].select("td")]
        results.append(first_row)
        results.append(second_row)

    file_name = "audit_gov_{0}.csv".format(datetime.now().strftime("%d%m%Y%H%M%S"))
    print(f"Save to {file_name}...")
    field_names = ("name", "position", "email", "phone_number")
    try:
        with open(file_name, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(field_names)
            writer.writerows(results)
            f.close
            print("Done!!!")
    except Exception as error:
        print(f"{error}")
        
    
        
if __name__ == "__main__":
    main()
