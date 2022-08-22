from bs4 import BeautifulSoup
import mysql.connector
import time
from datetime import datetime
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains

# function used to get an int height out of the string that is provided
def getHeight(height):
    heightFinal = 0
    heightList = height.split("-")
    heightList[0] = int(heightList[0]) * 12
    for t in heightList:
        heightFinal += int(t)
    return heightFinal

# Function being used to set up SQL query along with initiating the collection of the data
def yearCollection(url, driver, rosterYear):
    val = []
    sql = f'INSERT IGNORE INTO roster (id, roster_year, first_name, last_name, height, position, hometown, home_state, weight, class, highschool) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    if (rosterYear > 2020) or (rosterYear <= 2018):
        for x in LinkCollection(url, rosterYear):
            # opening the chrome window
            if 'jimbo-fisher' in x:
                pass
            driver.get(url[0: 19]+str(x)+'#sidearm-roster-player-stats')
            val.append(Collection(driver.page_source, rosterYear))
    else:
        driver.get(url)
        val = Collection2(driver.page_source, rosterYear)

        # Executing the data to the SQL server
    mycursor.executemany(sql, val)
    mydb.commit()

# Function used to create a unique id from the last name of the player
def uid(lastName):
    CODE = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13,
            'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25,
            'Z': 26, ' ': 27, '-': 28, '.': 29, ',': 30, 'Ö': 31, "'": 32}
    id = ''
    for k in lastName:
        if (k != "-") and (k != "."):
            id += str(CODE[k.upper()])
        else:
            id += str(CODE[k])
    while len(id) <= 6:
        id += '0'
    return id[0:6]

# Collection function used to scrape the data from the players stats page
def Collection(page, rosterYear):
    data = {}
    soup = BeautifulSoup(page, 'html.parser')
    firstName = soup.find("span", class_="sidearm-roster-player-first-name").text.strip()
    lastName = soup.find("span", class_="sidearm-roster-player-last-name").text.strip()
    id = uid(lastName)
    topStats = soup.find_all("dl", class_="flex-item-1")
    for x in topStats:
        data[x.find("dt").text.strip()] = x.find("dd").text.strip()
    height = getHeight(data['Height'])
    weight = data['Weight']
    position = data['Position']
    schoolClass = data['Class']
    homeCity = data['Hometown'].split(', ')[0]
    homeState = data['Hometown'].split(', ')[1]
    highSchool = data['Highschool']
    return (id, rosterYear, firstName, lastName, height, position, homeCity, homeState, weight, schoolClass, highSchool)

#second collection function used for years that the format of the page changes
def Collection2(page, rosterYear):
    data = []
    soup = BeautifulSoup(page, 'html.parser')
    fullName = soup.find_all("tr", role="row")
    fullName.pop(0)
    for x in fullName:
        playerInfo = []
        if x.text.strip().split("\n")[0] == "ImageNameTitle":
            break
        playerInfo.append(int(uid(x.text.strip().split("\n")[1].split(" ", 1)[1])))
        playerInfo.append(rosterYear)
        playerInfo.append(x.text.strip().split("\n")[1].split(" ",1)[0])
        playerInfo.append(x.text.strip().split("\n")[1].split(" ", 1)[1])
        playerInfo.append(getHeight(x.text.strip().split("\n")[3]))
        playerInfo.append(x.text.strip().split("\n")[2])
        playerInfo.append(x.text.strip().split("\n")[7].split(" / ")[0].split(", ")[0])
        playerInfo.append(x.text.strip().split("\n")[7].split(" / ")[0].split(", ")[1])
        playerInfo.append(int(x.text.strip().split("\n")[4]))
        playerInfo.append(ClassAbbrevetation(x.text.strip().split("\n")[5]))
        playerInfo.append(x.text.strip().split("\n")[7].split(" / ")[1])
        playerInfo = tuple(playerInfo)
        print(playerInfo)
        data.append(playerInfo)
    return data

# Function used to change the abbreviated classes to full words
def ClassAbbrevetation(classIden):
    if "SR" in classIden.upper():
        return "Senior"
    elif "JR" in classIden.upper():
        return "Junior"
    elif "SO" in classIden.upper():
        return "Sophomore"
    elif "FR" in classIden.upper():
        return "Freshman"
    elif "GR" in classIden.upper():
        return "Graduate Student"


# Function used to get the links of all the players and return a list to iterate through
def LinkCollection(url, year):

    # opening the chrome window
    driver.get(url)
    time.sleep(1)
    linksList = []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if year > 2020:
        links = soup.find_all("a", class_="sidearm-roster-player-bio-link", href=True)
        for x in links:
            if 'coaches' not in x['href']:
                linksList.append(x['href'])
    elif year < 2019:
        links = soup.find_all("div", class_="sidearm-roster-player-bio hide-on-small-down")
        for t in links:
            linkSoup = t.find("a", href=True)
            linksList.append(linkSoup['href'])
    return linksList

if __name__ == '__main__':
    # Connecting to mysql database
    mydb = mysql.connector.connect(
        host="localhost",
        user="noahalsina",
        database="football"
    )
    year = 0
    mycursor = mydb.cursor()



    print("----------------EXTRACTING DATA----------------")
    # url containing information being loaded into driver
    url = 'https://12thman.com/sports/football/roster'

    # setting the chrome options to not open a window
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    yearIndex = 2022
    while yearIndex >= 2009:
        print(yearIndex)
        yearCollection(url+f"/{yearIndex}", driver, yearIndex)
        yearIndex -= 1










