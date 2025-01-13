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
import pandas as pd
import re

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
    listofproducts = st.selectbox("Choose a product for demo:",("-","Adengappa kadhaigal!","Back to school!","Ramadan Campaign!","Ramadan Campaign! (Arabic)","Create your Ramadan recipe!","Spice up your dream moment!","Receipt Verification"),)
    if listofproducts == "-": choicetext = ""
    elif listofproducts == "Adengappa kadhaigal!": choicetext = "Scan your household item , turn them into stories and become your Kid's favourite Storyteller!"
    elif listofproducts == "Back to school!": choicetext = '''IMAGINE & CREATE!  
    The Perfect School with AI'''
    elif listofproducts == "Ramadan Campaign!": choicetext = '''IMAGINE & CREATE!  
    Your Dream Iftar setup with AI'''
    elif listofproducts == "Ramadan Campaign! (Arabic)": choicetext = '''تخيل وأبدع!  
    إعداد إفطار أحلامك باستخدام الذكاء الاصطناعي'''
    elif listofproducts == "Spice up your dream moment!": choicetext = '''IMAGINE & CREATE!  
    Your Dream Moment with AI'''
    elif listofproducts == "Receipt Verification": choicetext = "Handling hundreds of receipts manually, Put AI to work!"
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

# dream moment
elif listofproducts == "Spice up your dream moment!":
    st.title("Spice-up Campaign!")
    st.caption("Sample Prompt: Create a moment in space enjoying lays chips")
    spiceup_prompttext = st.chat_input("Using AI, create your dream moment where you want to enjoy a packet of lays")
    
    if (spiceup_prompttext is not None):
        if (("lays" in spiceup_prompttext)|("Lays" in spiceup_prompttext)):
            st.caption("Your Prompt: " + spiceup_prompttext)
            client = OpenAI()
            spiceup_response = client.images.generate(
                model="dall-e-3",
                prompt=spiceup_prompttext,
                size="1024x1024",
                quality="standard",
                n=1,
                )
            image_url = spiceup_response.data[0].url
            st.image(image_url)
        else:
            st.write("The prompt should contain the word 'lays'or 'Lays' as the campaign is regarding the same!")
            
# receipt verification
elif listofproducts == "Receipt Verification":
    st.title("AI Receipt Verification")
    st.subheader("Input",divider="gray")
    # Receiving Input
    countryoptions = st.selectbox("Enter the country:", ('KSA','Kuwait'))
    invoice_files = st.file_uploader("Upload your receipts", type=['png','jpg','jpeg'], accept_multiple_files=True)
    if (invoice_files is not None):
        st.subheader("Output", divider="gray")
        invdf = pd.DataFrame(columns=['File Name','Product Found','Date of Invoice','Total Amount for Product','Second Iteration'])
        count = 0
        for fileval in invoice_files:
            st.write('Processing - ',fileval.name)
            image_bytes_invoice = fileval.getvalue()
            image_base64 = base64.b64encode(image_bytes_invoice).decode('utf-8')
            invdf.loc[count,'File Name'] = fileval.name
            client = OpenAI()
            
            # Extracting
            response = client.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {
                        "role":"user",
                        "content":[
                            {
                                "type":"text",
                                "text": "From the invoice/bill extract date of invoice(if it is not available, the output in the mentioned format should just be None. The year cannot be greater than 2024 or 2025. Understand the extracted date with this context as well), check if the product 'persil' or 'prsl' is found (yes/no) response (note: it could be in arabic as well in this way: برسيل . Consider only english if oth are present), if it is present then extract only total amount of all 'persil' or 'prsl' products without any currency denomination. The output representation has to always be in the following format (including commas and colons): 'Product Found: Only Yes/No, Date of Invoice: (in DD-MM-YYYY format), Total amount for product:'",
                            },
                            {
                                "type":"image_url",
                                "image_url":{"url": f"data:image/jpeg;base64,{image_base64}"},
                            },
                        ],
                    }
                ],
                temperature=0.5,
            )
            response_text = response.choices[0].message.content
            invdf.loc[count,'Product Found'] = response_text.split(',')[0].split(':')[1].strip()
            invdf.loc[count,'Date of Invoice'] = response_text.split(',')[1].split(':')[1].strip()
            invdf.loc[count,'Total Amount for Product'] = response_text.split(',')[2].split(':')[1].strip()
            
            # Second Extraction - to counter amount mismatches
            checkresponse = client.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {
                        "role":"user",
                        "content":[
                            {
                                "type":"text",
                                "text": "Print the amount corresponding to persil or prsl products (it can be in arabic as well in this way: برسيل . Consider only english if both are present) without any currency denomination. Don't total the amounts, just the raw values would suffice. Also a thing to note: don't get confused with unit price and the final purchase price. For e.g., let's say 27.95 is the unit price but since two units were purchased the final purchase will be 55.90. The required value in such cases is 55.90. This has to be considered say if both 27.95 and 55.90. If both the prices are not given and let's say the no. of items purchased is 2, then the provided price is already the price for 2 items. You need not again multiply with 2.",
                            },
                            {
                                "type":"image_url",
                                "image_url":{"url": f"data:image/jpeg;base64,{image_base64}"},
                            },
                        ],
                    }
                ],
                temperature=0.5,
            )
            checkresponse_text = checkresponse.choices[0].message.content
            invdf.loc[count,'Second Iteration'] = checkresponse_text
            count+=1
    
        # Processing the combined dataset
        invdf['Total Amount for Product'] = invdf['Total Amount for Product'].apply(lambda x: re.sub(r'[^0-9.]','',x).strip('.'))
        invdf['Total Amount for Product'] = pd.to_numeric(invdf['Total Amount for Product'])
        
        # Creating another second iteration column
        invdf['Second Iteration1'] = invdf['Second Iteration'].apply(lambda x: sum(float(num) for num in re.findall(r'\d+\.\d+',x)))
        invdf['Second Iteration1'] = pd.to_numeric(invdf['Second Iteration1'])
        
        for row in range(0,invdf.shape[0]):
            if invdf.loc[row,'Total Amount for Product'] != invdf.loc[row,'Second Iteration1']:
                invdf.loc[row,'Total Amount for Product'] = invdf.loc[row,'Second Iteration1']
                   
        # Selecting only the required columns
        finalinvfdf = invdf[['File Name','Product Found','Date of Invoice','Total Amount for Product']]
        # Implementing conditions:
        for rowitem in range(0,finalinvfdf.shape[0]):
            if (countryoptions=='KSA') & (finalinvfdf['Total Amount for Product']>60) & (finalinvfdf['Product Found']=='Yes'):
                finalinvfdf.loc[rowitem,'Validity'] = 'Valid'
            elif (countryoptions=='Kuwait') & (finalinvfdf['Total Amount for Product']>5) & (finalinvfdf['Product Found']=='Yes'):
                finalinvfdf.loc[rowitem,'Validity'] = 'Valid'
            else:
                finalinvfdf.loc[rowitem,'Validity'] = 'Invalid'
        # Showing the output
        if finalinvfdf.shape[0]>0:
            #st.dataframe(invdf)
            st.dataframe(finalinvfdf)
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
