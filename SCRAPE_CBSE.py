#importing all the needed modules/lib
from selenium import webdriver
from selenium.webdriver.support.ui import Select
#using beautiful soup parser
from bs4 import BeautifulSoup
#using csv instead of pandas-dataframe
from csv import writer
#using re to clear out unwanted tab/space from text(strings)
import re


def OpenPage():
    #getting the webpage
    driver.get("http://cbseaff.nic.in/cbse_aff/schdir_Report/userview.aspx")
    #selecting  "State Wise" radio button
    radio1 = driver.find_element_by_xpath("//input[@id='optlist_2']")
    #clicking the button
    radio1.click()
    #waiting down for some time(so that webpage can)
    driver.implicitly_wait(countDown)

countDown = 3
#setting path to chromium driver (if in path then not needed)
driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe")
OpenPage()

#opening the dataset.csv
with open('dataset.csv','w') as csv_file:
    csv_writer = writer(csv_file)
    #setting up the headers (taking name state and upto)
    headers = ['Name','State','upto',"Address","telephone/Mobile no.","Principal name"]
    csv_writer.writerow(headers) 

    for i in range(1,38): #TOTAL_NO_OF_STATES = 38

        #selecting the state
        Select(driver.find_element_by_xpath("//select[@id='ddlitem']")).select_by_index(i)
        driver.implicitly_wait(countDown)

        #clicking search button
        driver.find_element_by_xpath("//input[@id='search']").click()
        driver.implicitly_wait(countDown)

        #finding the total number of pages to loop
        total_schools = int(driver.find_element_by_xpath("//span[@id='tot']").text)
        total_pages = int(total_schools/25) + 1

        for k in range(total_pages):
            print("[+info+]Page ",k+1,"/",total_pages," of ",Select(driver.find_element_by_xpath("//select[@id='ddlitem']")).first_selected_option.text," (",i,")")
            soup = BeautifulSoup(driver.page_source,'html.parser')
    
            #rows will contain atmost 26 results of which 1st entry is the header
            rows = soup.select("table#T1 > tbody > tr > td > table")
            rows.pop(0) #removes header table
            state = Select(driver.find_element_by_xpath("//select[@id='ddlitem']")).first_selected_option.text
            for row in rows:
                col1 = row.select("tbody > tr > td")[1]
                col2 = row.select("tbody > tr > td")[7]
                #selecting name validation
                name = col1.select("tbody > tr a")[0].getText()
                upto = col1.select("tbody > tr ")[4].getText()
                principal_name= col1.select("tbody > tr ")[2].getText()
                #getting important details!!
                address = re.sub(r"[\n\t]*", "", col2.select("table > tbody > tr")[0].getText()[9:])
                phone = re.sub(r"[\n\t]*", "", col2.select("table > tbody > tr")[1].getText()[10:])
                email = re.sub(r"[\n\t\s]*", "", col2.select("table > tbody > tr")[2].getText()[8:])
                #appending each data in csv file 
                csv_writer.writerow([name,state,upto,address,phone,principal_name])    
            #to move to next page
            nextButton = driver.find_element_by_xpath("//input[@id='Button1']")
            driver.execute_script("arguments[0].click();", nextButton)


        OpenPage()
        Select(driver.find_element_by_xpath("//select[@id='ddlitem']")).select_by_index(i)
        driver.implicitly_wait(countDown)
#closing the driver
driver.close()
