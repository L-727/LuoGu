import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# URL of the Luogu login page
driver = webdriver.Edge('I:\edgedrive\msedgedriver.exe')
url = "https://www.luogu.com.cn/auth/login"
#url = "https://www.baidu.com"
# Initialize a WebDriver (you need to have a compatible driver installed, e.g., ChromeDriver)

#driver = webdriver.Edge()

driver.get(url)

try:
    # Open the Luogu login page
    

    # Wait for a few seconds to ensure the page is fully loaded (you can adjust this time)
    time.sleep(5)

    # Locate the username and password input fields and submit button by their HTML attributes
    username_field = driver.find_element_by_id("username")
    password_field = driver.find_element_by_id("password")
    login_button = driver.find_element_by_id("login_button")

    # Input your Luogu username and password
    username_field.send_keys("YourUsername")
    password_field.send_keys("YourPassword")

    # Click the login button to submit the form
    login_button.click()

    # Wait for a few seconds to see if the login was successful (you can adjust this time)
    time.sleep(5)

    # You can now continue crawling the authenticated pages or perform other actions

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the WebDriver when you're done
    driver.quit()
