from selenium import webdriver
import csv
import MailChecker

xpaths = {
    "fieldnames" : ['URL', 'First Name',	'Last Name', 'Current Designation',	 'MailID', 'Location',	'Connections',
                  'Designation1','Company1', 'Time Worked1', 'Designation2','Company2', 'Time Worked2',
                  'Designation3', 'Company3',	'Time Worked3', 'Designation4', 'Company4',
                  'Time Worked4', 'Designation5',	'Company5', 'Time Worked5', 'School1',
                  'Degree1', 'School2',	'Degree2', 'School3', 'Degree3', 'Skill1', 'Skill2','Skill3'],
    "login" : {
        "username" : ".//*[@id='login-email']",
        "password" : ".//*[@id='login-password']",
        "submit" : ".//*[@id='login-submit']"
    },
    "fullname" : ".//*/div[3]/div[1]/h1",
    "current_designation" : ".//*/div[3]/div[1]/h2",
    "location" : ".//*/div[3]/div[1]/h3[1]",
    "connections" : ".//*/div[3]/div[1]/h3[2]/span[1]",
    "designation" : ".//*[@class='Sans-17px-black-85%-semibold']",
    "company" : ".//*[@class='pv-profile-section experience-section ember-view']//*[@class='pv-position-entity__secondary-title pv-entity__secondary-title Sans-15px-black-55%']",
    "school" : ".//*/div[2]/div/h3",
    "duration" : "(//*[(text() = 'Experience')]/../following-sibling::ul/li)[%s]//p[1]/span[2]",
    "degree1" : "(//*[@class='education-entity pv-profile-section__card-item ember-view']/div[2]/div/h4[1]/span[2])[%s]",
    "degree2" : "(//*[@class='education-entity pv-profile-section__card-item ember-view']/div[2]/div/h4[2]/span[2])[%s]",
    "skills" : ".//*[@class='pv-skill-entity__pill-contents static-pill']//span[1]"
}


def login(username,password,url):
    driver = webdriver.Chrome("E:\\Drivers\\chromedriver.exe")
    driver.maximize_window()
    driver.get(url)
    driver.find_element_by_xpath(xpaths["login"]["username"]).send_keys(username)
    driver.find_element_by_xpath(xpaths["login"]["password"]).send_keys(password)
    driver.find_element_by_xpath(xpaths["login"]["submit"]).click()
    return driver

def read_url():
    fp = open("url.txt", 'r')
    URL = fp.read().split('\n')
    return URL

def validate_mail_id(fname,lname,company):
    company = company.lower().strip()
    if ' ' in company:
        company = company.split(' ')[0]
    if '.com' not in company:
        domain = company + '.com'
    else:
        domain = company
    fname = fname.lower()
    lname = lname.lower()
    mailID=''
    mailIDList = [fname + '@' + domain, lname + '@' + domain, fname + '.' + lname + '@' + domain,
                  lname + '.' + fname + '@' + domain]
    for each_mailID in mailIDList:
        if (MailChecker.mailchecker(each_mailID) == 'Success'):
            mailID = each_mailID
            break
        else:
            mailID=''

    return mailID

# main program
base_url = 'https://www.linkedin.com/'
username = ''
password = ''
driver = login(username,password,base_url)
count_profiles = 0

url_list=read_url()

with open('test.csv', 'ab') as csvfilewriter:
    fieldnames = xpaths['fieldnames']
    writer = csv.DictWriter(csvfilewriter, fieldnames=fieldnames)
    writer.writeheader()
    for each_url in url_list:
        details = {}
        details['URL'] = each_url
        driver.get (each_url)
        driver.implicitly_wait(2)
        try:
            name=driver.find_element_by_xpath(xpaths["fullname"]).text.split(' ')
            details['First Name']=name[0]
            details['Last Name']=name[1]
        except:
            pass
        try:
            current_designation=driver.find_element_by_xpath(xpaths["current_designation"]).text.encode('utf8')
            details['Current Designation']=current_designation
        except:
            pass
        try:
            details['Location'] = driver.find_element_by_xpath(xpaths["location"]).text
        except:
            pass
        try:
            details['Connections'] = driver.find_element_by_xpath(xpaths["connections"]).text
        except:
            pass
        try:
            designation = driver.find_elements_by_xpath(xpaths["designation"])
            company = driver.find_elements_by_xpath(xpaths["company"])
            try:
                details['MailID'] = validate_mail_id(name[0], name[1], company[0].text.encode('utf8'))
            except:
                details['MailID'] = ''
            for i in range(1, 6):
                dur = 'Time Worked' + str(i)
                try:
                    duration_ele = (xpaths["duration"] %i )

                    details[dur] = driver.find_element_by_xpath(duration_ele).text.encode('utf8')
                except:
                    details[dur] = ''

            count = 1
            for i in designation:
                if count <= 5:
                    degn = 'Designation' + str(count)
                    details[degn] = i.text.encode('utf8')
                else:
                    break
                count += 1

            count = 1
            for each_company in company:
                if count <= 5:
                    comp = 'Company' + str(count)
                    details[comp] = each_company.text.encode('utf8')
                else:
                    break
                count += 1

            if count <= 5:
                for j in range(count, 6):
                    degn = 'Designation' + str(j)
                    comp = 'Company' + str(j)
                    details[degn] = ''
                    details[comp] = ''

        except:
            pass
        try:
            school = driver.find_elements_by_xpath(xpaths["school"])
            count = 1
            for each_school in school:
                if count <= 3:
                    scl = 'School' + str(count)
                    details[scl] = each_school.text.encode('utf8')
                else:
                    break
                count += 1

            for i in range(1, 4):
                deg = 'Degree' + str(i)
                try:
                    deg_ele1 = (xpaths['degree1']%i)
                    deg1 = driver.find_element_by_xpath(deg_ele1).text.encode('utf8')
                    try:
                        deg_ele2 = (xpaths["degree2"]%i)
                        deg2 = driver.find_element_by_xpath(deg_ele2).text.encode('utf8')
                    except:
                        deg2 = ''
                    degree = deg1 + ' ' + deg2
                    details[deg] = degree
                except:
                    details[deg] = ''
        except:
            pass

        # act = ActionChains(driver)
        try:
            skill_ele = xpaths["skills"]
            for eachy in range(100, 5000, 400):
                scroll = "window.scrollTo(0," + str(eachy) + ")"
                driver.execute_script(scroll)
                try:
                    try:
                        driver.implicitly_wait(1)
                        if (driver.find_elements_by_xpath(skill_ele)):
                            skills = driver.find_elements_by_xpath(skill_ele)
                            count = 1
                            for i in skills:
                                if count<=3:
                                    skl = 'Skill' + str(count)
                                    details[skl] = i.text
                                    count += 1
                                else:
                                    break

                            if count <= 3:
                                for i in range(count,4):
                                    skl = 'Skill' + str(i)
                                    details[skl] = ''

                            break
                    except:
                        continue
                except:
                    for i in range(1,4):
                        skl = 'Skill' + str(i)
                        details[skl] = ''
        except:
            pass

        driver.implicitly_wait(2)
        count_profiles += 1
        writer.writerow(details)
driver.close()
print 'Parsing of ' + str(count_profiles) + ' profiles completed successfully!!'
csvfilewriter.close()