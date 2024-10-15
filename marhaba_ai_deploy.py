# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 17:36:13 2024

@author: rahul
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:07:19 2024

@author: rahul
"""

import time
import os
import streamlit as st
import ollama
from openai import OpenAI

### UI Functions
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.20)
        
### Input (company text, images etc.,)
marhabaailogo = r'C:\Users\rahul\Desktop\Secondary Income\Marhaba AI\MARHABA AI LOGO\marhaba ai logo-01.jpg'
company_text = "Your gateway to cutting-edge solutions for marketing & advertising. We empower brands to captivate audiences like never before! We are a team of tech & creative enthusiasts specializing in Artifical Intelligence, Machine Learning, Augumented & Virtual Reality"
os.environ['openai_secret_key'] = st.secrets["openai_secret_key"]

### Actual UI

## Creating the sidebar ux here

with st.sidebar:
    st.image(marhabaailogo,width=150)
    listofproducts = st.selectbox("Choose a product for demo:",("-","Adengappa kadhaigal!","Back to school!"),)
    if listofproducts == "-": choicetext = ""
    elif listofproducts == "Adengappa kadhaigal!": choicetext = "Miss your grandparent's stories?! Now, get anyone to recite a story!"
    else: choicetext = "Joining back school after your summer holidays? Paint a picture of how would you want your school to change!"
    st.write(choicetext)

# Landing page
if listofproducts=="-":
    st.title("Marhaba AI")
    st.write_stream(stream_data(company_text))
# adengappa kadhaigal page
elif listofproducts=="Adengappa kadhaigal!":
    st.title("Adengappa kadhaigal!")
    img_file_buffer = st.camera_input("Click a picture!. You get to recite a story to your kid")
    if img_file_buffer is not None:
        image_bytes = img_file_buffer.getvalue()
        print("image ready, calling ollama")
        response = ollama.chat(model = 'llava',messages=[
                {
                'role':'user',
                'content': 'Describe the image',
                'images':[image_bytes]
                }
            ]
        )
        st.mardown(response['message']['content'])
#back to school page
else:
    st.title("Back to school season!")
    st.caption("Sample Prompt: Create a realistic image of a classroom surrounded by nature. Add trees, flowers, and fluffy chairs with students sitting in them, a digital board and butterflies flying.")
    prompttext = st.chat_input("Imagine, describe and create your dream school with AI")
    if prompttext is not None:
        st.caption("Your Prompt: " + prompttext)
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompttext,
            size="1024x1024",
            quality="standard",
            n=1,
            )
        image_url = response.data[0].url
        st.image(image_url)