from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.common.keys import Keys
import re
import openai

openai.api_key = "YourKey"

driver = webdriver.Firefox()

# Navigate to the WhatsApp Web page
driver.get('https://web.whatsapp.com/')

# Wait for the user to scan the QR code
input('Press Enter once you have scanned the QR code.')

chat_name = "Audio 2"

# Find the chat you want to interact with
search_box = driver.find_element(By.CSS_SELECTOR, 'div[contenteditable="true"]')
search_box.send_keys(chat_name)
time.sleep(2)

# Open the chat
chat = driver.find_element(By.XPATH, f'//span[@title="{chat_name}"]')
chat.click()

def send_text(string):
    message_box = driver.find_elements(By.CSS_SELECTOR, 'div[contenteditable="true"]')[1]
    message_box.clear()
    char_list = list(string)
    for n in range(len(string)):
        message_box.send_keys(char_list[n])
    message_box.send_keys(Keys.ENTER)


# Wait for a response
last_response_time = 0
last_message_id = None
aux_polar = 0

while True:
    if aux_polar == 0:
        messages = driver.find_elements(By.CSS_SELECTOR, 'div.message-in')
        
    if aux_polar == 1:
        messages = driver.find_elements(By.CSS_SELECTOR, 'div.message-out')
    
    try: 
        last_message = messages[-1]
        message_id = last_message.get_attribute('data-id')
    except:
        last_message = "NF"
        message_id = 0
        
    if message_id != last_message_id:
        try:
            message_text = last_message.find_element(By.CSS_SELECTOR, 'span.selectable-text').text
        except:
            message_text = "nao suportado"
        message_text = message_text.lower()
        if message_text[:5] == "[gpt]":
            current_time = time.time()
            if current_time - last_response_time > 10: # wait at least 10 seconds between responses
                message_text = message_text[5:]
                response = openai.Completion.create(model="text-davinci-003",
                                                    prompt= message_text,
                                                    temperature=0,
                                                    max_tokens=1000)
                response = "[BOT GPT] " + response.choices[0]['text']
                send_text(response)
        last_message_id = message_id
    aux_polar = (aux_polar + 1)%2
    time.sleep(1)
