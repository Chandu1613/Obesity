import streamlit as st # type: ignore
import pandas as pd
import pickle
from xgboost import XGBClassifier # type: ignore # typo: ignore

# When you open pickle file, use this command
with open("xg_obesity_level.pkl",'rb') as file:
    model = pickle.load(file)

st.title("Obesty Level Classification")
st.write("This application classifies Obesity level into Obesity Type III, Obesity Type II, Obesity Type I, Overweight Level II, Overweight Level I, Normal Weight, Insufficient Weight using RandomForest")
st.subheader("Enter Your Information")

gender = st.selectbox("Gender",["Male", "Female"])
age = st.number_input("Age", min_value=0, max_value=100)
height = st.number_input("Height (cm)",min_value=0,max_value=200)
weight = st.number_input("Weight (kg)", min_value=0,max_value=150)
family_history = st.selectbox('Family History with Overweight',["Yes","No"])
favc = st.selectbox('Do you eat high caloric food frequently?',["Yes","No"])
fcvc = st.number_input('Give the rating of 1-3 for eating vegetables in your meals.',min_value=1, max_value=3)
ncp = st.number_input('How many main meals do you have daily?',min_value=1, max_value=4)
caec = st.number_input('Do you eat any food between meals?',min_value=1, max_value=3)
smoke = st.selectbox("Do you smoke?",["Yes", "No"])
ch2o = st.number_input('How much water do you drink daily?',min_value=1, max_value=3)
scc = st.selectbox('Do you monitor the calories you eat daily?',["Yes", "No"])
faf = st.selectbox('How often do you have physical activity?',['Regular','Sometimes','No'])
tue = st.selectbox('How much time do you use technological devices such as cell phone, videogames, television, computer and others?',['Low','Moderate','High'])
bmi = st.number_input("Enter your Body Mass Index value",min_value=12,max_value=55)
calc = st.selectbox('How often do you drink alcohol?',['Yes','No','Frequently'])

input_data = pd.DataFrame({'Gender': [1 if gender=='Male' else 0],'Age':[age],'Height':[height],'Weight':[weight],
                           'family_history_with_overweight': [1 if family_history=='Yes' else 0],
                           'FAVC':[1 if favc=='Yes' else 0],
                           'FCVC':[fcvc],'NCP':[ncp],'CAEC':[caec],
                           'SMOKE':[1 if smoke=='Yes' else 0],
                           'CH2O':[ch2o],
                           'SCC':[1 if scc=='Yes' else 0],
                           'FAF':[2 if faf=='Regular' else(1 if faf=='Sometimes' else 0)],
                           'TUE':[2 if tue=='High' else(1 if tue=='Moderate' else 0)],
                           'CALC':[1 if calc=='Yes' else(0 if calc=='No' else 2)],'BMI':[bmi]
                           })

expected_oder = ['Gender', 'Age', 'Height', 'Weight',
       'family_history_with_overweight', 'FAVC', 'FCVC', 'NCP', 'CAEC',
       'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC', 'BMI']

input_data = input_data.reindex(columns=expected_oder)

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
    6: 'Obesity_Type_III'
}
    result = label_mapping.get(predicted_label, "Unknown")
    st.write(f'The predicted test result is : **{result}**')


# Add background image using custom CSS
def add_background(image_url):
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("{'https://www.heart.org/-/media/Images/News/2022/January-2022/0112BHObesityBrain_SC.jpg?sc_lang=en'}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Main app
add_background("https://www.heart.org/-/media/Images/News/2022/January-2022/0112BHObesityBrain_SC.jpg?sc_lang=en")  # Replace with your image URL


