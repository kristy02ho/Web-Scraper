import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def main():
    while 1:
        # Create menu for user to choose which webscraping
        print("1. Webscrape from CU Denver Website")
        print("2. Webscrape from COVID data")
        print("3. Exit")
        menu = input("Please choose an option: ")
        if menu == "1":
            denver_webscrape()
        elif menu == "2":
            covid_webscrape()
        elif menu == "3":
            return
        else:
            print("Invalid choice. Please choose from 1-3")

def denver_webscrape():
    url = "http://www.ucdenver.edu/pages/ucdwelcomepage.aspx"
    header = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    # Get request
    request = requests.get(url, headers=header)
    # Get HTML with BeautifulSoup
    soup = BeautifulSoup(request.content, 'html.parser')
    # Find all scripts with
    scripts = soup.find_all('script', {"type":"application/ld+json"})

    # For each script, get the text and use json.loads
    # to parse the data and put into dictionary
    for script in scripts:
        script_content = script.get_text()
        result = json.loads(script_content)

    # Initialize department list
    department_list = []

    # Create dictionary for each department
    for department in result['department']:
        department_info = {
            "department_name": department['name'],
            "telephone": department.get('telephone'),
            "url": department['url'],
        }
        # Append each department's info to the department list
        department_list.append(department_info)

    # Dump list of departments into JSON file
    with open('data.json', 'w') as outfile:
        json.dump(department_list, outfile, indent=4)

    print("Output extracted as data.json")

def covid_webscrape():
    url = "https://cdphe.colorado.gov/covid-19/data"
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    # Get request
    request = requests.get(url, headers=header)
    # Get HTML with BeautifulSoup
    soup = BeautifulSoup(request.content, 'html.parser')
    # Find table
    main_table = soup.find("table", attrs={'dir':'ltr'})
    # Find all rows in table
    rows = main_table.find_all('tr')
    row_list = []

    # For each row, append the data to the row list
    for row in rows:
        row_list.append([el.text.strip() for el in row.find_all('td')])

    # Put first row of row list into header and delete
    header_list = row_list[0]
    del row_list[0]

    # Create table with pandas
    frame = pd.DataFrame(row_list, columns=header_list)

    # Convert the table to html
    html = frame.to_html(justify='left')

    # Creat html file to view table
    with open("data.html", "w") as file:
        file.write(html)


main()


