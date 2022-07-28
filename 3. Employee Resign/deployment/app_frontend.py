import streamlit as st
import requests
from PIL import Image


st.markdown('---')
opener = 'image'
if opener == 'image':
    ## From an Image
    main_image = Image.open('hr.png')
    st.image(main_image)
else:
    ## From a Video
    gif0 = '<div style="width:1080px"><iframe allow="fullscreen" align="center" frameBorder="0" height="720" width="1440"></iframe></div>'
    st.markdown(gif0, unsafe_allow_html=True)
st.markdown('---')

text_des = '<h4 style="font-family:sans-serif; color:#cbd5e7; text-align:left;">This application can be used to predict whether employees will resign or not from the company</h4>'
st.markdown(text_des, unsafe_allow_html=True)

instruction = '<p style="font-family:sans-serif; color:#67b8f8; font-size: 20px;"> Please imput employee data below </p>'
st.markdown(instruction, unsafe_allow_html=True)

Education = st.selectbox("Education Level", ['Bachelors','Masters','PHD'])
JoiningYear = st.selectbox("Joining year", [2012,2013,2014,2015,2016,2017,2018])
City = st.selectbox("City",['Bangalore','Pune','New Delhi'])
PaymentTier = st.selectbox("Payment Tier", [1,2,3])
Age = st.number_input("Age (Years)")
Gender = st.selectbox("Gender", ['Male', 'Female'])
EverBenched = st.selectbox("Ever Benched", ['No', 'Yes'])
ExperienceInCurrentDomain = st.selectbox("Experience (Years)", [0,1,2,3,4,5,6,7])
# inference
data = {'education':Education,
        'join_year':JoiningYear,
        'city':City,
        'payment_tier':PaymentTier,
        'age': Age,
        'gender':Gender,
        'ever_benched':EverBenched,
        'experience':ExperienceInCurrentDomain
        
        }

# URL = "http://127.0.0.1:5000/predict" # sebelum push backend
URL = "https://rio-armiga-backend.herokuapp.com/predict" # setelah push backend

text_style = '<p style="font-family:sans-serif; color:#67b8f8; font-size: 20px;">Employees are predicted to</p>'
st.markdown(text_style, unsafe_allow_html=True)

# komunikasi
if st.button('Predict'):
    r = requests.post(URL, json=data)
    res = r.json()
    if r.status_code == 200:
        st.title(res['result']['class_name'])
    elif r.status_code == 400:
        st.title("ERROR BOSS")
        st.write(res['message'])