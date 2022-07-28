import streamlit as st
import pandas as pd
import requests
import pickle
import json
from PIL import Image


st.markdown('---')
opener = 'image'
if opener == 'image':
    ## From an Image
    main_image = Image.open('2.jpg')
    st.image(main_image)
else:
    ## From a Video
    gif0 = '<div style="width:1080px"><iframe allow="fullscreen" align="center" frameBorder="0" height="720" width="1440"></iframe></div>'
    st.markdown(gif0, unsafe_allow_html=True)
st.markdown('---')

text_des = '<h4 style="font-family:sans-serif; color:#cbd5e7; text-align:left;">This application can be used to predict whether customer will churn or not</h4>'
st.markdown(text_des, unsafe_allow_html=True)

instruction = '<p style="font-family:sans-serif; color:#67b8f8; font-size: 20px;"> Please imput employee data below </p>'
st.markdown(instruction, unsafe_allow_html=True)


Gender = st.selectbox("Gender", ['Male', 'Female'])
SeniorCitizen = st.selectbox("Senior Citizen", [0,1])
Partner = st.selectbox("Partner", ['Yes','No'])
Dependents = st.selectbox("Dependents", ['Yes','No'])
Tenure = st.number_input("tenure (Mounth)")
PhoneService = st.selectbox("Phone Service", ['Yes','No'])
MultipleLines = st.selectbox("Multiple Lines", ['Yes','No','No phone service'])
InternetService = st.selectbox("Internet Service", ['Fiber optic','DSL','No'])
OnlineSecurity = st.selectbox("Online Security", ['Yes','No','No internet service'])
OnlineBackup = st.selectbox("Online Backup", ['Yes','No','No internet service'])
DeviceProtection = st.selectbox("Device Protection", ['Yes','No','No internet service'])
TechSupport = st.selectbox("Tech Support", ['Yes','No','No internet service'])
StreamingTV = st.selectbox("Streaming TV", ['Yes','No','No internet service'])
StreamingMovies = st.selectbox("Streaming Movies", ['Yes','No','No internet service'])
Contract = st.selectbox("Contract", ['Month-to-month','Two year','One year'])
PaperlessBilling = st.selectbox("Paperless Billing", ['Yes','No'])
PaymentMethod = st.selectbox("Payment Method", ['Electronic check','Mailed check','Bank transfer','Credit card'])
MonthlyCharges = st.number_input("Monthly Charges ($)")
TotalCharges = st.number_input("Total Charges ($)")

# inference

data = [Gender , 
    SeniorCitizen, 
    Partner, 
    Dependents,
    Tenure, 
    PhoneService, 
    MultipleLines, 
    InternetService,
    OnlineSecurity, 
    OnlineBackup, 
    DeviceProtection, 
    TechSupport,
    StreamingTV, 
    StreamingMovies, 
    Contract, 
    PaperlessBilling,
    PaymentMethod, 
    MonthlyCharges, 
    TotalCharges]

with open("preprop.pkl", "rb") as f:
    model = pickle.load(f)

columns = ['gender', 'SeniorCitizen', 'Partner', 'Dependents',
       'tenure', 'PhoneService', 'MultipleLines', 'InternetService',
       'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
       'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
       'PaymentMethod', 'MonthlyCharges', 'TotalCharges']

new_data = pd.DataFrame([data], columns = columns)
new_data_enc = model.transform(new_data)
new_data_list = new_data_enc.tolist()

input_data_json = json.dumps({
    'signature_name':'serving_default',
    'instances':new_data_list
})

URL = 'https://ml1-back-rio-armiga.herokuapp.com/v1/models/churn:predict' # setelah push backend


text_style = '<p style="font-family:sans-serif; color:#67b8f8; font-size: 20px;">Will the customer churn?</p>'

st.markdown(text_style, unsafe_allow_html=True)

# komunikasi
if st.button('Predict'):
    r = requests.post(URL, data= input_data_json)
    hasil = r.json()
    res = hasil['predictions'][0]
    for res in hasil['predictions']:
        if res[0] > 0.5:
            st.write('Yes')
        else:
            st.write('No')