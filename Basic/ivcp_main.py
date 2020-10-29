import requests
import requests.packages.urllib3
from bs4 import BeautifulSoup
import csv
import pymysql

requests.packages.urllib3.disable_warnings()
PUNCTUATION = '◈'


def main():
    url = "https://ic.tpex.org.tw/"
    try:
        source_code = requests.get(url, verify=False)
        source_code.raise_for_status()
        source_code.encoding = "utf-8"
        html = source_code.text
        web_parser(url, html)
    except requests.exceptions.RequestException as err:
        print(f'Error: {err}')
    # finally:


def web_parser(url, html):
    soup = BeautifulSoup(html, "lxml")
    data = soup.find_all("div", class_="item")
    # get database connection and sql command
    db, sql = mysql_database()
    # data pointer
    cursor = db.cursor()
    # open csv file
    with open("stock.csv", "w", encoding="utf-8-sig", newline="")as f:
        # create csv writer
        writer = csv.writer(f)
        # cvs first row
        writer.writerow(["main_category", "sub_category", "third_category", "link"])
        for category in data[:len(data) - 1]:
            get_name = category.find("span", class_="txt")
            category_name = get_name.text
            get_link = category.find("a")
            if str(get_link)[22:31] == "introduce":
                # sql values
                values = (category_name, "", "", str(url + get_link["href"]), str(url + get_link["href"]))
                # write in csv
                writer.writerow([category_name, "", "", url + get_link["href"]])
                # print(f'{category_name} {url + get_link["href"]}')
            sub_menu = category.find("ul", class_="subMenu")

            if sub_menu:
                sub_data = sub_menu.find_all("li", class_="listItem")
                for get_sub_data in sub_data:
                    get_sub_list_name = get_sub_data.find("span", class_="")
                    sub_name = get_sub_list_name.text
                    sub_get_link = get_sub_data.find("a")
                    if str(sub_get_link)[9:18] == "introduce":
                        # sql values
                        values = (category_name, sub_name, "", url + sub_get_link["href"], url + sub_get_link["href"])
                        # write in csv
                        writer.writerow([category_name, sub_name, "", url + sub_get_link["href"]])
                        # print(f'{category_name} {sub_name} {url + sub_get_link["href"]}')
                    third_menu = get_sub_data.find("div", class_="thirdMenu")
                    if third_menu:
                        third_data = third_menu.find_all("span")
                        for get_third_data in third_data:
                            get_third_list_name = get_third_data.text.strip(PUNCTUATION).replace(" ", "")
                            # sql values
                            values = (category_name, sub_name, get_third_list_name, url + str(get_third_data)[47:68],
                                      url + str(get_third_data)[47:68])
                            # write in csv
                            writer.writerow(
                                [category_name, sub_name, get_third_list_name, url + str(get_third_data)[47:68]])
                            # print(
                            #     f'{category_name} {sub_name}  {get_third_list_name} {url + str(get_third_data)[47:68]}')

                            # execute sql command with values
                            cursor.execute(sql, values)
                    cursor.execute(sql, values)
            cursor.execute(sql, values)
        # data write into database
        db.commit()
        # close database
        db.close()


def mysql_database():
    db_settings = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "Passw0rd",
        "db": "stock",
        "charset": "utf8mb4"
    }
    try:
        # connect to database
        db = pymysql.connect(**db_settings)
    except Exception as err:
        print(f'Error: {err}')
    finally:
        # sql command
        sql = "INSERT INTO category SELECT %s, %s, %s, %s FROM dual " \
              "WHERE not exists (SELECT link FROM category WHERE link = %s)"
        return db, sql


if __name__ == "__main__":
    main()
