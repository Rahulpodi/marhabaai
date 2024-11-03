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
    st.image(marhabaailogo)
    listofproducts = st.selectbox("Choose a product for demo:",("-","Adengappa kadhaigal!","Back to school!","Ramadan Campaign!","Ramadan Campaign! (Arabic)","Create your Ramadan recipe!"),)
    if listofproducts == "-": choicetext = ""
    elif listofproducts == "Adengappa kadhaigal!": choicetext = "Scan your household item , turn them into stories and become your Kid's favourite Storyteller!"
    elif listofproducts == "Back to school!": choicetext = '''IMAGINE & CREATE!  
    The Perfect School with AI'''
    elif listofproducts == "Ramadan Campaign!": choicetext = '''IMAGINE & CREATE!  
    Your Dream Iftar setup with AI'''
    elif listofproducts == "Ramadan Campaign! (Arabic)": choicetext = '''تخيل وأبدع!  
    إعداد إفطار أحلامك باستخدام الذكاء الاصطناعي'''
    else: choicetext = '''30 days. 30 inspirational  
    Recipes for Iftar with AI'''
    st.markdown(choicetext)

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
        image_base64 = base64.b64encode(image_bytes_adengappa).decode('utf-8')
        client = OpenAI()
        adengappa_response = client.chat.completions.create(
              model="gpt-4o-mini",
              messages=[
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "text",
                      "text": "Generate a 150 word indian story based on the image provided, which can be recited to my kid",
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
        st.markdown(adengappa_response.choices[0].message.content)
        
# back to school page
elif listofproducts=="Back to school!":
    st.title("Back to school campaign!")
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
elif listofproducts == "Ramadan Campaign!":
    st.title("Ramadan Campaign!")
    st.caption("Sample Prompt: Create an image of an iftar setup which has traditional dishes and the surrounding is also decked up for Ramadan festivities!")
    ramadan_prompttext = st.chat_input("Create your own iftar/sehri setup for this Ramadan using AI")
    
    if (ramadan_prompttext is not None):
        if (("Iftar" in ramadan_prompttext)|("iftar" in ramadan_prompttext)|("iftaar" in ramadan_prompttext) | ("Iftaar" in ramadan_prompttext) | ("sehri" in ramadan_prompttext) | ("Sehri" in ramadan_prompttext)):
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
            st.write("The prompt should contain the word 'iftar','iftaar' or 'sehri' as the campaign is about 'Ramadan Festivities'")

# ramadan iftaar table - arabic
elif listofproducts == "Ramadan Campaign! (Arabic)":
    st.title("الحملة الرمضانية!")
    st.caption("نموذج موجه: قم بإنشاء صورة لإعداد إفطار يحتوي على أطباق تقليدية ويتم أيضًا تزيين المحيط احتفالًا بشهر رمضان!")
    ramadan_prompttext = st.chat_input("قم بإنشاء إعدادات الإفطار/السحور الخاصة بك لشهر رمضان هذا العام باستخدام الذكاء الاصطناعي")
    if (ramadan_prompttext is not None):
        st.caption("موجهك: " + ramadan_prompttext)
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
    st.title("Create your recipe with AI!")
    img_file_buffer_recipe = st.file_uploader("Upload a picture of a food item!",type=['png','jpg','jpeg'],accept_multiple_files=False)
    if img_file_buffer_recipe is not None:
        image_bytes_recipe = img_file_buffer_recipe.getvalue()
        recipe_image_base64 = base64.b64encode(image_bytes_recipe).decode('utf-8')
        client = OpenAI()
        recipe_response = client.chat.completions.create(
              model="gpt-4o-mini",
              messages=[
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "text",
                      "text": "Create a detailed middle eastern recipe basis the food item name mentioned in the provided image",
                    },
                    {
                      "type": "image_url",
                      "image_url": {
                        "url":  f"data:image/jpeg;base64,{recipe_image_base64}"
                      },
                    },
                  ],
                }
              ],
            )
        st.image(image_bytes_recipe)
        st.markdown(recipe_response.choices[0].message.content)
        if len(recipe_response.choices[0].message.content)>0:
            recipe_prompt = "Create a photo of the food item that is described here: "+recipe_response.choices[0].message.content
            st.subheader("Here is a photo of the recipe as well!")
            client = OpenAI()
            recipe_response = client.images.generate(
                model="dall-e-3",
                prompt=recipe_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
                )
            recipe_image_url = recipe_response.data[0].url
            st.image(recipe_image_url)
