from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import csv

# filter = "-Talent -Analytics -Category -Business -Media -Fulfilment -Planning -Program -Customer -Experience -Creative -Revenue -Zonal -HR -Relations -Marketplace -Taxation -Finance -Initiatives -Insights -Marketing -Branch -Cashier -indirect -Supply -HRBP -Buying -chain -staff -sales"
filter = " -assistant"

config = {
    "comp": ["Flipkart"],
    "desg": ["CEO", "CTO", "CIO", "CPO", "VP", "Head", "Director"],
    "xpath": "//*[contains (text(),'Current:')]"
}
def login(username,password,url):
    driver = webdriver.Chrome("E:\\Drivers\\chromedriver.exe")
    driver.get(url)
    driver.find_element_by_xpath(".//*[@id='login-email']").send_keys(username)
    driver.find_element_by_xpath(".//*[@id='login-password']").send_keys(password)
    driver.find_element_by_xpath(".//*[@id='login-submit']").click()
    return driver

base_url = 'https://www.linkedin.com/'
username = ''
password = ''
driver = login(username,password,base_url)

driver.implicitly_wait(10)
with open('test_url.csv', 'ab') as csvfilewriter:
    fieldnames = ['Company', 'Designation', 'URL']
    writer = csv.DictWriter(csvfilewriter, fieldnames=fieldnames)
    writer.writeheader()
    for each_comp in config["comp"]:
        # print each_comp
        for each_designation in config["desg"]:
            # print each_designation
            company = each_comp
            designation = each_designation
            search_str = designation + " of " + company + filter
            # Searching [designation] of [company name] -[Filters]
            driver.get("https://www.linkedin.com/search/results/index/?keywords=" + search_str + "&origin=GLOBAL_SEARCH_HEADER")
            driver.implicitly_wait(10)

            current_xpath = config["xpath"]
            elements = driver.find_elements_by_xpath(current_xpath)

            links = []
            count = 0
            for i in elements:
                count += 1
                if "current" in i.text.lower() and designation.lower() in i.text.lower() and company.lower() in i.text.lower():
                    links.append(driver.find_element_by_xpath("(" + current_xpath +")[" + str(count) + "]/../a").get_attribute('href'))

            if len(links) == 0:
                time.sleep(1)
                ActionChains(driver).send_keys(Keys.CONTROL).send_keys(Keys.HOME).perform()
                time.sleep(1)
                current_xpath = current_xpath + "/preceding-sibling::p[2]"
                elements = driver.find_elements_by_xpath(current_xpath)
                count = 0
                for i in elements:
                    count += 1
                    if designation.lower() in i.text.lower() and company.lower() in i.text.lower():
                        links.append(driver.find_element_by_xpath("(" + current_xpath + ")[" + str(count) + "]/../a").get_attribute('href'))
            if len(links) != 0:
                fp = open("url.txt",'a+')
                for each_link in links:
                    fp.write(each_link + '\n')

                url_dict = {}
                url_dict['Company'] = company
                url_dict['Designation'] = designation
                url_dict['URL'] = links
                writer.writerow(url_dict)

            # print links

csvfilewriter.close()
driver.close()