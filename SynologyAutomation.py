from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
#this script saves all your files from your synology server

#Put in your details here
website = "https://yourwebsite.quickconnect.to/"
login = "ursername"
pw = "password"
#directory decides where your files will be saved
directory = "/Users/frehml/Documents/Files"

class SynologyBot:
    def __init__(self, website, login, pw):
        self.login = login
        self.website = website
        self.pw = pw
        self.file = 1
        
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : directory}
        chromeOptions.add_experimental_option("prefs",prefs)
        chromedriver = "./chromedriver"
        self.driver = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)
        self.driver.get(self.website)

        sleep(20)
        self.log()

    def log(self):
        self.driver.find_element_by_xpath("/html/body/div[7]/div[3]/div[2]/div/form/div[1]/div/div/div[1]/input").send_keys(self.login)
        self.driver.find_element_by_xpath("/html/body/div[7]/div[3]/div[2]/div/form/div[1]/div/div/div[2]/input").send_keys(self.pw)
        self.driver.find_element_by_xpath("/html/body/div[7]/div[3]/div[2]/div/form/div[1]/div/div/span[1]/em/button").click()
        sleep(20)
        self.open_files()

    def open_files(self):
        self.driver.find_element_by_xpath("/html/body/div[11]/ul/li[2]/li/div[1]").click()
        sleep(10)
        self.loop()
    
    def next_folder(self):
        self.file += 1
        self.driver.find_element_by_xpath("/html/body/div[11]/div[29]/div[3]/div[1]/div/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div[1]/div/ul/div/li[2]/ul/li["+str(self.file)+"]/div").click()
        sleep(20)

    def select_files(self):
        check = True
        place = 1
        ActionChains(self.driver).key_down(Keys.SHIFT).perform()

        while check:
            try:
                self.driver.find_element_by_xpath("/html/body/div[11]/div[29]/div[3]/div[1]/div/div/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div[2]/div[1]/div/div/div["+str(place)+"]/table/tbody/tr").click()
            except:
                check = False

            place += 1
        ActionChains(self.driver).key_up(Keys.SHIFT).perform()

    def download_files(self):
        elem = self.driver.find_element_by_xpath("/html/body/div[11]/div[29]/div[3]/div[1]/div/div/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div[2]/div[1]/div/div/div/table/tbody/tr")
        self.select_files()
        sleep(2)

        actions = ActionChains(self.driver)
        actions.context_click(elem)
        actions.perform()

        sleep(2)

        self.driver.find_element_by_css_selector("[aria-labelledby='ext-gen2030']").click()

        sleep(2)

    def loop(self):
        check = True

        while check:
            self.download_files()
            try:
                self.next_folder()
            except:
                check = False

        print("Download complete")


bot = SynologyBot(website, login, pw)