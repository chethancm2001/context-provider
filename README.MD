# context-provider 
One of the bigest problem about AI tools are they don't have the context on your full project this will help to upload all the file content in the project that prompt issue your are facing 

# working GIF
![Working GIF](./gif/final2.gif)

# Installation 
1. clone the repo
2. create the .env file
```env
EMAIL="YOUR CHAT GPT EMAIL"
PASSWORD="YOUR CHAT GPT PASSWORD"
```
3. install the requirements
```bash
pip install -r requirements.txt
```
4. create the instance 
```py
from entry import ContextProvider
from dotenv import load_dotenv
import os

load_dotenv()  
       
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
path = "your path"

con = ContextProvider(email,password,path)
con.login()
con.create_new_chat()
con.context_tree()
con.sendContent()
```
5. run and enjoy 