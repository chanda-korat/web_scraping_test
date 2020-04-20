import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

"""
This is a scrapper file.
It would scrape data from web site : https://www.landwatch.com upto 100 pages and 
saved the same into excel file under /logs/current_date_time_stamp.xlsx file
"""

__author__ = "Chanda Korat"

base_url = "https://www.landwatch.com"

project_root = os.path.dirname(os.path.dirname(__file__))
logs_path = os.path.join(project_root, "logs")


def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match


def get_current_time_stamp():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S.%f")
    return timestampStr


def save_data_to_excel_file(result_list):
    my_df = pd.DataFrame(result_list)
    timestampStr = get_current_time_stamp()
    my_df.to_excel(os.path.join(logs_path, "Demo_{}.xlsx".format(timestampStr)))


def get_all_urls_to_scrap_data():
    url_dict = {}
    for i in range(2):
        url_list = []
        url = r'https://www.landwatch.com/Florida_land_for_sale/page-{}'.format(i + 1)
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
        soup = BeautifulSoup(response.text, "html.parser")
        all_div = soup.find_all('div',
                                attrs={'class': lambda e: e.startswith('result flex-grid displaytype') if e else False})
        for div in all_div:
            a = div.find('a')
            url_list.append(a.get("href"))
        url_dict["Page {}".format(i + 1)] = url_list

    return url_dict


def scrap_data(url_dict):
    result_list = []
    for each_page, url_list in url_dict.items():
        for each in url_list:
            final_dict = {"Page No": each_page}
            try:
                print('############### {} : {}'.format(each_page, each))
                response = requests.get(base_url + each, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
                soup = BeautifulSoup(response.text, "html.parser")
                all_scripts = soup.find_all('script')
                for index, each_script in enumerate(all_scripts):
                    if "window.dataLayer.push" in str(each_script):
                        place_info = \
                            str(each_script).replace("window.dataLayer.push(", "").replace(");", "").replace(
                                "</script>",
                                "").strip().split(
                                ";")[-1].strip()
                        place_dict = eval(place_info)

                        try:
                            final_dict["country"] = place_dict["country"]
                        except:
                            final_dict["country"] = "Not available"

                        try:
                            final_dict["state"] = place_dict["state"]
                        except:
                            final_dict["state"] = "Not available"

                        try:
                            final_dict["city"] = place_dict["city"]
                        except:
                            final_dict["city"] = "Not available"

                        try:
                            final_dict["zip"] = place_dict["zip"]
                        except:
                            final_dict["zip"] = "Not available"
                        break

                txt_list = []
                all_div = soup.find_all('div', class_="marginleft marginright marginbottom")

                for each_div in all_div:
                    all_txt = each_div.text.strip().split("\n")
                    txt_list.append(all_txt)
                try:
                    final_dict["proprty_classification"] = txt_list[0][0]
                except:
                    final_dict["proprty_classification"] = "Not available"
                for index, data in enumerate(range(0, len(txt_list[1]), 2)):
                    try:
                        if len(txt_list[1][data].strip()) > 0:
                            final_dict[txt_list[1][data]] = txt_list[1][data + 1]
                    except IndexError:
                        continue
                try:
                    final_dict["Agent"] = txt_list[1][-1].split("Email")[0].replace("Agent:", "")
                except:
                    pass
                contact_num = soup.find('div', class_="agentlinks agentlinkstopright")
                phoneicon = contact_num.find('div', class_="phoneicon")
                anc = phoneicon.find('a')
                try:
                    phonenum_text = str(anc.get("onclick")).split(":")[1].split("<")[0].strip()
                    final_dict["Contact_num"] = phonenum_text
                except:
                    final_dict["Contact_num"] = "Not available"

                try:
                    property_desc = soup.find(class_="margin marginright marginbottom")
                    final_dict["Property_description"] = property_desc.text
                except:
                    final_dict["Property_description"] = "Not available"

                try:
                    all_image_link = soup.find(id="PhotoContainer")
                    a_link = all_image_link.find_all("a")
                    image_links = []
                    for each_image_link in a_link:
                        image_links.append(each_image_link.get("href"))
                    final_dict["Images"] = ",".join(image_links)
                except:
                    final_dict["Page_url"] = "Not available"
                try:
                    final_dict["Page_url"] = base_url + each
                except:
                    pass
                result_list.append(final_dict)
            except Exception as e:
                print(e)
                result_list.append(final_dict)


url_dict = get_all_urls_to_scrap_data()
result_list = scrap_data(url_dict)
save_data_to_excel_file(result_list)
