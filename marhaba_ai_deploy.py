# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 17:36:13 2024
"""

import time
import os
import streamlit as st
import ollama
from openai import OpenAI
import base64

### UI Functions
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.20)
        
### Input (company text, images etc.,)
marhabaailogo = 'marhaba ai logo-01.jpg'
company_text = "Your gateway to cutting-edge solutions for marketing & advertising. We empower brands to captivate audiences like never before! We are a team of tech & creative enthusiasts specializing in Artifical Intelligence, Machine Learning, Augumented & Virtual Reality"
os.environ['OPENAI_API_KEY'] = st.secrets["openai_secret_key"]

### Actual UI

## Creating the sidebar ux here

with st.sidebar:
    st.image(marhabaailogo,width=150)
    listofproducts = st.selectbox("Choose a product for demo:",("-","Adengappa kadhaigal!","Back to school!","Break your fast!","Create a recipe!"),)
    if listofproducts == "-": choicetext = ""
    elif listofproducts == "Adengappa kadhaigal!": choicetext = "Miss your grandparent's stories?! Now, get anyone to recite a story!"
    elif listofproducts == "Back to school!": choicetext = "Joining back school after your summer holidays? Paint a picture of how would you want your school to change!"
    elif listofproducts == "Break your fast!": choicetext = "This Ramadan, Create an iftaar table using AI"
    else: choicetext = "Struggling with what to cook? Ask our AI and create a recipe!"
    st.write(choicetext)

# Landing page
if listofproducts=="-":
    st.title("Marhaba AI")
    st.write_stream(stream_data(company_text))

# adengappa kadhaigal page
elif listofproducts=="Adengappa kadhaigal!":
    st.title("Adengappa kadhaigal!")
    img_file_buffer_adengappa = st.camera_input("Click a picture!. You get to recite a story to your kid")
    if img_file_buffer_adengappa is not None:
        image_bytes_adengappa = img_file_buffer_adengappa.getvalue()
        image_base64 = base64.b64encode(image_bytes_adengappa.getvalue()).decode('utf-8')
        client = OpenAI()
        adengappa_response = client.chat.completions.create(
              model="gpt-4o-mini",
              messages=[
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "text",
                      "text": "Describe the image",
                    },
                    {
                      "type": "image_url",
                      "image_url": {
                        "url":  f"data:image/jpeg;base64,{image_base64}"
                      },
                    },
                  ],
                }
              ],
            )
        st.markdown(adengappa_response.choices[0])
        
# back to school page
elif listofproducts=="Back to school!":
    st.title("Back to school season!")
    st.caption("Sample Prompt: Create a realistic image of a classroom surrounded by nature. Add trees, flowers, and fluffy chairs with students sitting in them, a digital board and butterflies flying.")
    school_prompttext = st.chat_input("Imagine, describe and create your dream school with AI")
    if school_prompttext is not None:
        if (("school" in school_prompttext) | ("School" in school_prompttext)):
            st.caption("Your Prompt: " + school_prompttext)
            client = OpenAI()
            school_response = client.images.generate(
                model="dall-e-3",
                prompt=school_prompttext,
                size="1024x1024",
                quality="standard",
                n=1,
                )
            image_url = school_response.data[0].url
            st.image(image_url)
        else:
            st.write("The prompt should contain the word 'school' as the campaign is about 'Back to school!'")

# ramadan iftaar table
elif listofproducts == "Break your fast!":
    st.title("Ramadan Season!")
    st.caption("Sample Prompt: Create a realistic image of an iftaar table which has traditional dishes and the surrounding is also decked up for Ramadan festivities!")
    ramadan_prompttext = st.chat_input("Create your own iftaar/sehri table for this Ramadan using AI")
    
    if (ramadan_prompttext is not None):
        if (("iftaar" in ramadan_prompttext) | ("Iftaar" in ramadan_prompttext) | ("sehri" in ramadan_prompttext) | ("Sehri" in ramadan_prompttext)):
            st.caption("Your Prompt: " + ramadan_prompttext)
            client = OpenAI()
            ramadan_response = client.images.generate(
                model="dall-e-3",
                prompt=ramadan_prompttext,
                size="1024x1024",
                quality="standard",
                n=1,
                )
            image_url = ramadan_response.data[0].url
            st.image(image_url)
        else:
            st.write("The prompt should contain the word 'iftaar' or 'sehri' as the campaign is about 'Ramadan Festivities'")
else:
    st.title("Create your recipe with AI!")
    img_file_buffer_recipe = st.file_uploader("Upload a picture of a food item!",type=['png','jpg','jpeg'],accept_multiple_files=False)
    if img_file_buffer_recipe is not None:
        image_bytes_recipe = img_file_buffer_recipe.getvalue()
        print("image ready, calling ollama")
        recipe_response = ollama.chat(model = 'llava',messages=[
                {
                'role':'user',
                'content': 'Create an arabic recipe basis the food item name mentioned in the provided image',
                'images':[image_bytes_recipe]
                }
            ]
        )
        st.mardown(recipe_response['message']['content'])
