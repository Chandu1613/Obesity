import streamlit as st 
import pandas as pd
import pickle
from xgboost import XGBClassifier # type: ignore # typo: ignore

# When you open pickle file, use this command
with open("xg_obesity_level.pkl",'rb') as file:
    model = pickle.load(file)

st.title("Obesty Level Classification")
st.write("This application uses XGBoost to categorise obesity levels into Type III, Type II, Type I, Overweight Level II, Overweight Level I, Normal Weight, and Insufficient Weight.")
st.subheader("Enter Your Information")

# User inputs
gender = st.selectbox("Gender",["Male", "Female"])
age = st.number_input("Age", min_value=0, max_value=100)
height = st.number_input("Height (cm)",min_value=0,max_value=200)
weight = st.number_input("Weight (kg)", min_value=0,max_value=150)

# Calculate BMI dynamically
if height > 0 and weight > 0:
    bmi = round(weight / ((height / 100) ** 2), 2)
    st.write(f"**Your calculated BMI is:** {bmi}")
else:
    bmi = None
    st.write("Please enter valid height and weight to calculate BMI.")

# Remaining inputs
family_history = st.selectbox('Do you have any family history of being overweight?',["Yes","No"])
favc = st.selectbox('Do you eat high caloric food frequently?',["Yes","No"])
fcvc = st.number_input('Rate the amount of veggies you include in your meals on a scale of 1 to 3.',min_value=1, max_value=3)
ncp = st.number_input('On a scale of 1 to 4, indicate how many main meals you eat each day.',min_value=1, max_value=4)
caec = st.number_input('Rate if you eat anything in between meals on a scale of 1 to 3.',min_value=1, max_value=3)
smoke = st.selectbox("Do you smoke?",["Yes", "No"])
ch2o = st.number_input('How much water do you drink daily? (1-3 liters)',min_value=1, max_value=3)
scc = st.selectbox('Do you monitor the calories you eat daily?',["Yes", "No"])
faf = st.selectbox('How frequently do you engage in physical activity?',['Yes','No','Frequently'])
tue = st.selectbox('How much often do you use Electronic devices such as cell phone, videogames, television, computer and others?',['Low','Moderate','High'])
calc = st.selectbox('How often do you drink alcohol?',['Yes','No','Frequently'])


# Prepare input data for prediction

input_data = pd.DataFrame({'Gender': [1 if gender=='Male' else 0],'Age':[age],'Height':[height],'Weight':[weight],
                           'family_history_with_overweight': [1 if family_history=='Yes' else 0],
                           'FAVC':[1 if favc=='Yes' else 0],
                           'FCVC':[fcvc],'NCP':[ncp],'CAEC':[caec],
                           'SMOKE':[1 if smoke=='Yes' else 0],
                           'CH2O':[ch2o],
                           'SCC':[1 if scc=='Yes' else 0],
                           'FAF':[2 if faf=='Yes' else(1 if faf=='Frequently' else 0)],
                           'TUE':[2 if tue=='High' else(1 if tue=='Moderate' else 0)],
                           'CALC':[1 if calc=='Yes' else(0 if calc=='No' else 2)],
                           'BMI':[bmi]
                           })


expected_order = ['Gender', 'Age', 'Height', 'Weight','family_history_with_overweight',
                 'FAVC', 'FCVC', 'NCP', 'CAEC','SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC','BMI']

input_data = input_data.reindex(columns=expected_order)

if st.button("Predict"):
    prediction = model.predict(input_data)
    predicted_label = prediction[0] 
    label_mapping = {
    0: 'Insufficient_Weight',
    1: 'Normal_Weight',
    2: 'Overweight_Level_I',
    3: 'Overweight_Level_II',
    4: 'Obesity_Type_I',
    5: 'Obesity_Type_II',
    6: 'Obesity_Type_III'}

    result = label_mapping.get(predicted_label, "Unknown")
    st.write(f'The predicted test result is : **{result}**')
else:
    st.write("Please provide height and weight to calculate BMI before predicting.")







