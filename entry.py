import time
from typing import Any
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc 
import time 
import os
from tree import DisplayablePath
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv



class ContextProvider:
    #global variables
    openai_url = "https://chat.openai.com/auth/login"
    

    def __init__(self,Email,password,path="./upload"):
        # instance variables
        self.email = Email
        self.password = password
        self.path = path
        # settings up the driver
        options = uc.ChromeOptions() 
        options.headless = False
        self.driver = uc.Chrome(use_subprocess=True, options=options)
        self.wait = WebDriverWait(self.driver, 10) 
    
    def login(self):
        self.driver.get(self.openai_url) 
        self.driver.maximize_window() 
        time.sleep(3) 
        log_button = self.driver.find_elements(By.XPATH,"//button")
        log_button[0].click()
        time.sleep(2)
        input_email = self.driver.find_element(By.XPATH,'//input[@inputmode="email"]')
        input_email.send_keys(email)
        time.sleep(1)
        submit_button = self.driver.find_element(By.XPATH,"//button[@type='submit']")
        submit_button.click()
        time.sleep(2)
        password_input = self.driver.find_element(By.XPATH,"//input[@name='password']")
        password_input.send_keys(password)
        time.sleep(1)
        final_submit = self.driver.find_elements(By.XPATH,"//button[text()='Continue']")
        final_submit[1].click()
        
 
    def create_new_chat(self):
        escape = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="radix-:rh:"]/div[2]/div/div[4]/button')))
        escape.click()
        new_chat = self.driver.find_elements(By.XPATH,"//a")
        new_chat[0].click()
        
    def gettree(self):
        path = self.path
        def is_not_hidden(path):
            return not path.name.startswith(".")
# 
        paths = DisplayablePath.make_tree(Path(self.path), criteria=is_not_hidden)
        string = ""
        for path in paths:
            string += path.displayable()
            string += "\n"  
        return string
    
    def context_tree(self):
        initial = r"You are a code interpreter and summariser. You'll receive file tree of the project and also the contents of individual files. You'll analyze the code and write a brief summary about the project and also respond to queries within the context. The file tree will be sent now but the code of each files will be sent in subsequent messages. Do not reply or make any commentary until i instruct you so in curly braces as {START}. The file tree:"
        tree = self.gettree()
        textarea = self.driver.find_element(By.XPATH,"//textarea")
        textarea.send_keys(initial)
        time.sleep(2)
        send = self.driver.find_element(By.XPATH,"//div/button[@data-testid='send-button']")
        send.click()
        time.sleep(2)
        textarea.send_keys(tree)
        time.sleep(2)
        wait = WebDriverWait(self.driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div/button[@data-testid='send-button']")))
        button.click()
        time.sleep(5)

    def sendContent(self):
        print("sending content")
        directory_path = self.path
        for root, dirs, files in os.walk(directory_path):
          
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                file_path = os.path.join(root, file)

                # Check if the path is a file (not a directory)
                if os.path.isfile(file_path):
                    try :
                        with open(file_path, 'r') as f:
            
                            file_contents = f.read()
                            time.sleep(4)
                            textarea = self.driver.find_element(By.XPATH,"//textarea")
                            textarea.send_keys(fr"filename:{file}")
                            textarea.send_keys("\n")
                            time.sleep(2)
                            textarea.send_keys(file_contents)
                            time.sleep(2)
                            wait = WebDriverWait(self.driver, 10)
                            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div/button[@data-testid='send-button']")))
                            time.sleep(2)
                            button.click()
                            time.sleep(4)
                        
                    except:
                        print(f"error in {file}")
                        

            # You can read the contents of the file here
          
          
load_dotenv()         
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


con = ContextProvider(email,password)
con.login()
con.create_new_chat()
con.context_tree()
con.sendContent()

