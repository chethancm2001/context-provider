import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc 
import time 
import os
from tree import DisplayablePath
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv



options = uc.ChromeOptions() 
load_dotenv()

options.headless = False  
openai_url = "https://chat.openai.com/auth/login"
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

driver = uc.Chrome(use_subprocess=True, options=options) 


def login(driver,email,password):
    driver.get(openai_url) 
    driver.maximize_window() 
    time.sleep(3) 
    log_button = driver.find_elements(By.XPATH,"//button")
    log_button[0].click()
    time.sleep(2)
    input_email = driver.find_element(By.XPATH,'//input[@inputmode="email"]')
    input_email.send_keys(email)
    time.sleep(1)
    submit_button = driver.find_element(By.XPATH,"//button[@type='submit']")
    submit_button.click()
    time.sleep(2)
    password_input = driver.find_element(By.XPATH,"//input[@name='password']")
    password_input.send_keys(password)
    time.sleep(1)
    final_submit = driver.find_elements(By.XPATH,"//button[text()='Continue']")
    final_submit[1].click()
    time.sleep(10)

def createNewChat():
    escape = driver.find_elements(By.XPATH,"//button[@as='button']")
    escape[-1].click()
    new_chat = driver.find_elements(By.XPATH,"//a")
    new_chat[0].click()
    time.sleep(2)

def send_tree():
    initial = r"You are a code interpreter and summariser. You'll receive file tree of the project and also the contents of individual files. You'll analyze the code and write a brief summary about the project and also respond to queries within the context. The file tree will be sent now but the code of each files will be sent in subsequent messages. Do not reply or make any commentary until i instruct you so in curly braces as {START}. The file tree:"
    tree = gettree()

    textarea = driver.find_element(By.XPATH,"//textarea")
    textarea.send_keys(initial)
    time.sleep(2)

    send = driver.find_element(By.XPATH,"//div/button[@data-testid='send-button']")
    send.click()
    time.sleep(2)


    textarea.send_keys(tree)
    time.sleep(2)
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div/button[@data-testid='send-button']")))
    button.click()
    time.sleep(2)

def sendContent():
    directory_path = "./"

    # Loop through all files in the directory and its subdirectories
    for root, dirs, files in os.walk("./"):
        # Filter out hidden folders (those starting with a dot)
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            file_path = os.path.join(root, file)

            # Check if the path is a file (not a directory)
            if os.path.isfile(file_path):
                try :
                      with open(file_path, 'r') as f:
         
                        file_contents = f.read()
                        data = f"filename:{file}"+ "\n" + file_contents
                        senddata(data)
                    
                except:
                    pass
                # You can read the contents of the file here
              


    time.sleep(100)   
    driver.close()






    

def gettree():
    def is_not_hidden(path):
        return not path.name.startswith(".")
# 
    paths = DisplayablePath.make_tree(Path('./'), criteria=is_not_hidden)
    string = ""
    for path in paths:
        string += path.displayable()
        string += "\n"  
    return string





def senddata(data):
    textarea = driver.find_element(By.XPATH,"//textarea")
    textarea.send_keys(data)
    time.sleep(2)
    button = WebDriverWait.until(EC.element_to_be_clickable((By.XPATH, "//div/button[@data-testid='send-button']")))
    button.click()
    time.sleep(2)





login(driver,email,password)
createNewChat()
send_tree()
sendContent()

time.sleep(100)   
driver.close()

#//div/button[@data-testid='send-button']
# 



