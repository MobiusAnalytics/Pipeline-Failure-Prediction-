#%%writefile app.py
 
import pickle
import numpy as np
import streamlit as st
from pathlib import Path
import streamlit_authenticator as stauth


#------ USER AUTHENTICATION-----------

names = ["Mobius DA"]
usernames = ["Mobius_Data_Analytics"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

credentials = {"usernames":{}}
for un, name, pw in zip(usernames, names, hashed_passwords):
    user_dict = {"name":name,"password":pw}
    credentials["usernames"].update({un:user_dict})

authenticator = stauth.Authenticate(credentials,"CorrosionRisk","abc123",cookie_expiry_days=0)

hide_streamlit_style = """<style> #MainMenu {visibility: hidden;}footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

name,authetication_status,username = authenticator.login("LOGIN","main")

if authetication_status == False:
    st.error("Username/Password is incorrect")
if authetication_status == None:
    st.warning("Please enter your Username and Password")

#------ IF USER AUTHENTICATION STATUS IS TRUE  -----------    
    
if authetication_status: 
    # loading the trained model
    pickle_in_1 = open('RF_failure_prediction_model_updated.pickle', 'rb') 
    RF_Failure_Pred_Model = pickle.load(pickle_in_1)
     
    @st.cache()
      
    # defining the function which will make the prediction using the data which the user inputs 
    def prediction(Process_temperature, Rotational_speed, Torque, Tool_wear):   

        pred = RF_Failure_Pred_Model.predict([[Process_temperature, Rotational_speed, Torque, Tool_wear]])
        pred = pred[0]
        target_class = [0,1,2,3,4,5]
        target_label = ['No Failure','Heat Dissipation Failure','Overstrain Failure','Power Failure','Random Failures','Tool Wear Failure']
        output_dict = dict(zip(target_class, target_label))
        output = output_dict.get(pred)    
        return output
          
      
    # this is the main function in which we define our webpage  
    def main():  
        global days,data,Exogenous_features
        authenticator.logout("Logout",'sidebar')
        
        # front end elements of the web page 
        st.sidebar.title("Pipeline Failure Prediction")
        st.sidebar.image("""https://cdn-icons-png.flaticon.com/512/1486/1486232.png""")       
        html_temp = """ 
        <div style ="background-color:LightGray;padding:13px"> 
        <h2 style ="color:black;text-align:center;">Failure Prediction Model</h2> 
        </div> 
        """       
        st.subheader("Enter the values to predict the type of failure")
        Process_temperature = st.number_input("Process_temperature")
        Rotational_speed = st.number_input("Rotational_speed")
        Torque = st.number_input("Torque")
        Tool_wear =  st.number_input("Tool_wear")

       
        result = ""
          
        # when 'Predict' is clicked, make the prediction and store it 
        if st.button("PREDICT"): 
            output= prediction(Process_temperature, Rotational_speed, Torque, Tool_wear) 
            if output=="No Failure":
                st.markdown('<p style="font-family:sans-serif; color:green;text-align:center; font-size: 35px;"><b>{}</b></p>'.format(output),unsafe_allow_html = True)
            else:
                st.markdown('<p style="font-family:sans-serif; color:red;text-align:center; font-size: 35px;"><b>{}</b></p>'.format(output),unsafe_allow_html = True)
            
    if __name__=='__main__': 
        main()