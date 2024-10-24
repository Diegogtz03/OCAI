from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto("https://www.oracle.com/cloud/price-list/")
    
    page.wait_for_timeout(5000)
    
    rendered_html = page.content()
    
    browser.close()

soup = BeautifulSoup(rendered_html, "html.parser")

oci_services_section = soup.find("ul", {"aria-labelledby": "topics-label"})
oci_services_info_section = soup.find("section", {"class": "rc34 rc34v2 cpad rw-theme-10bg"})
oci_services_json = {}

for oci_service in oci_services_section.findAll("a"):
    oci_services_json[oci_service["href"][1:]] = {}

with open("output.html", "w", encoding="utf-8") as file:
    file.write(oci_services_info_section.prettify())

for id in oci_services_json.keys():
    service_info = oci_services_info_section.findAll("div", {"data-id": id})

    for service in service_info:
        service_name = service.find("h4").text
        oci_services_json[id].update({service_name: []})

        sub_services_table = service.find("table")
        
        if not sub_services_table:
            continue
        
        sub_services_table_head = sub_services_table.find("thead")
        sub_services_table_head_columns = [col.text.strip() for col in sub_services_table_head.findAll("div")]

        sub_services_table_body = sub_services_table.find("tbody")

        for tr in sub_services_table_body.findAll("tr"):
            row_data_cells = []
            
            row_header = tr.find("th", {"scope": "row"})
            if row_header:
                header_div = row_header.find("div")
                row_data_cells.append(header_div.text.strip() if header_div else row_header.text.strip())

            for td in tr.findAll("td"):
                    row_data_cells.append(td.text.strip())

            if len(row_data_cells) == len(sub_services_table_head_columns):
                row_data = {header: cell for header, cell in zip(sub_services_table_head_columns, row_data_cells)}

                oci_services_json[id][service_name].append(row_data)


with open("oci_services.json", "w") as file:
    json.dump(oci_services_json, file)

print(oci_services_json["pricing-analytics"])