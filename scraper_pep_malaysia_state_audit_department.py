from urllib.parse import urljoin
import csv
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
import re


def main():
    base_url = "https://www.audit.gov.my"
    print("Scraping web...")
    client = httpx.Client(follow_redirects=True)
    r = client.get(urljoin(base_url, "directory"))
    souped = BeautifulSoup(r.content, "html.parser")
    rows = souped.select("div.form-group div.row.mt-4")

    page_links = [(tag.get("href", ""), tag.get_text(strip=True, separator=" ")) for tag in rows[-1].select("h5>a")]
    
    results = list()
    for page in page_links:
        r1 = client.get(page[0])
        souped2 = BeautifulSoup(r1.content, "html.parser")
        tables = souped2.select("div.staff-list.mb-4 .table-responsive table")
        
        pattern = re.compile(r"pengarah|pengarah audit negeri|timbalan|timbalan pengarah|timbalan pengarah audit negeri", re.IGNORECASE)

        for table in tables[:2]:
            rows = table.select("tr")
            for row in rows:
                cols = [col.get_text(strip=True, separator=" ") for col in row.select("td")]
                if cols and pattern.match(cols[1]):
                    cols.append(page[1])
                    results.append(cols)


    file_name = "PEP_Malaysia_State_Audit_Department_{0}.csv".format(datetime.now().strftime("%d%m%Y%H%M%S"))
    print(f"Save to {file_name}...")
    field_names = ("name", "position", "email", "phone_number", "state")
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
