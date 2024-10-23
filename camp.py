from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import smtplib
#SERVER = "localhost"

FROM = 'hanh00740@gmail.com'
TO = ["hanh00740@gmail.com"] # must be a list


# Start display
display = pyvirtualdisplay.Display(visible=0, size=(1024, 768))
display.start()

# Setup Chrome options (optional, for headless mode)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("window-size=1200x600")
#chrome_options.setPage
#chrome_options.add_experimental_option("detach", True)

# ChromeDriver should already be in the PATH if installed via Homebrew
driver = webdriver.Chrome(options=chrome_options)

# URL of the reservation website
url = "https://reserve.fumotoppara.net/reserved/reserved-calendar-list"
login_url = "https://reserve.fumotoppara.net/"




#Login to page
driver.get(login_url)


#Close pop up at the initial page
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'el-dialog__headerbtn')))
close_button = driver.find_element(By.CLASS_NAME,'el-dialog__headerbtn')
driver.execute_script("arguments[0].click();", close_button)


# Wait until the login page loads
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'el-main')))
login_elements = driver.find_elements(By.TAG_NAME, "input")
login_elements[0].send_keys("hanh00740@gmail.com")
login_elements[1].send_keys("Nguyenhaiha89")
login_button = driver.find_element(By.TAG_NAME,"form").find_element(By.TAG_NAME,"div").find_element(By.TAG_NAME,"button")
driver.execute_script("arguments[0].click();", login_button)




# Open the reservation calendar page
#driver.get(url)

# Wait until the calendar loads
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'el-form')))

# Define the specific dates you want to check for availability (e.g., YYYY-MM-DD)
check_dates = ["12/7"]

# Allow some time for the calendar to fully render
time.sleep(5)

# Find all date elements in the calendar
date_elements = driver.find_elements(By.CLASS_NAME, "cell-date")
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
camp_status = driver.find_element(By.TAG_NAME,"tbody").find_elements(By.TAG_NAME,"tr")[1]
idx = 0

# Check the availability of the target dates
for date_element in date_elements:
    date = date_element.accessible_name.split( )[0]
    
    if date in check_dates:
        availability = camp_status.find_elements(By.TAG_NAME,"td")[idx].find_element(By.TAG_NAME,"p").text
        
        if availability in ["〇","△"]:
            #Click to reserve on this day
            camp_status.find_elements(By.TAG_NAME,"td")[idx].click()


            #Wait until the reservation dialog is displayed 
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'el-dialog__body')))
            #resv_button = driver.find_element(By.CLASS_NAME,'el-dialog__body').find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME,'div').find_element(By.TAG_NAME,'div').find_element(By.LINK_TEXT,'予約する')
            resv_button = driver.find_element(By.XPATH,'//button[@class="el-button el-button--success"]')
            resv_button.click()
           
            #Wait for page to load and enter reservation info
            wait.until(EC.presence_of_element_located((By.XPATH, '//main[@class="el-main"]')))
            timer_element = driver.find_element(By.XPATH, '//input[@class="el-input__inner"]')
            timer_element.click()
            #wait.until(EC.element_to_be_clickable((By.XPATH, '//li[@class="el-select-dropdown__item"]/span[7]')))
            timer_elements = driver.find_elements(By.XPATH, '//li[@class="el-select-dropdown__item"]/span[contains(text(),"11:00")]')
            
            #timer_elements[0].click()
            driver.execute_script("arguments[0].click();", timer_elements[0])

            adult_element = driver.find_element(By.XPATH, '//div[@class="number-input-text el-input el-input-group el-input-group--append el-input-group--prepend"]/input')
            adult_element.send_keys("2")
           
            adult_element = driver.find_elements(By.XPATH, '//div[@class="number-input-text el-input el-input-group el-input-group--append el-input-group--prepend"]/input')
            adult_element[1].send_keys("1")
           
            #Submit information
            submit_btn_elements = driver.find_elements(By.XPATH, '//button[@class="el-button el-button--primary"]')
            driver.execute_script("arguments[0].click();", submit_btn_elements[0])

            #Click on final confirmation button
            wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="el-button el-button--primary"]')))
            confirm_btn_element = driver.find_elements(By.XPATH, '//button[@class="el-button el-button--primary"]')
            driver.execute_script("arguments[0].click();", submit_btn_elements[0])


            print(f"Date {date} is available!")
            #Ports 465 and 587 are intended for email client to email server communication - sending email
            server = smtplib.SMTP('smtp.gmail.com', 587)

            #starttls() is a way to take an existing insecure connection and upgrade it to a secure connection using SSL/TLS.
            server.starttls()

            #Next, log in to the server
            server.login("hanh00740@gmail.com", "nuno btzj coxr leer")

            msg = f"Date {date} is available!"

            #Send the mail
            server.sendmail("hanh00740@gmail.com", "hanh00740@gmail.com", msg)
            server.quit()
        else:
            print(f"Date {date} is unavailable.")
    idx += 1
# Close the browser session
driver.quit()
display.stop()

