import streamlit as st
import pandas as pd
from joblib import load
from utils import Transformer

def validate_data(dict_respostas):
	if answers_dict['years_working'] != 0 and answers_dict['years_unemployed'] != 0:
		st.warning('Employed/unemployed data incompatible.')
		return False
	return True

def denied_validation(answers_dict):
	model = load('objects/model.joblib')
	features = load('objects/features.joblib')

	if answers_dict['years_working'] > 0:
		answers_dict['years_working'] = answers_dict['years_working'] * -1 
	
	answers = []
	for column in features:
		answers.append(answers_dict[column])

	df_new_client = pd.DataFrame(data = [answers], columns = features)

	denied = model.predict(df_new_client)[0]

	return denied

st.image("img/bytebank_logo.png")
st.write("# Credit Scoring Simulator")

expander_1 = st.beta_expander("Personal Information")

expander_2 = st.beta_expander("Work Information")

expander_3 = st.beta_expander("Family Information")

answers_dict = {}
categories_list = load("objects/categories_list.joblib")

with expander_1:
    col1_form, col2_form = st.beta_columns(2)

    answers_dict['age'] = col1_form.slider('What is your age?', help = 'The slider can be moved using the arrow keys.', min_value = 0, max_value = 100, step = 1)

    answers_dict['education_type'] = col1_form.selectbox('What is your educational level?', categories_list['education_type'])

    answers_dict['marital_status'] = col1_form.selectbox('What is your marital status?', categories_list['marital_status'])

    answers_dict['own_car'] = 1 if col2_form.selectbox('Do you own a car?', ['Yes', 'No']) == 'Yes' else 0

    answers_dict['own_phone'] = 1 if col2_form.selectbox('Do you own a phone? (not mobile)', ['Yes', 'No']) == 'Yes' else 0

    answers_dict['own_email'] = 1 if col2_form.selectbox('Do you have an e-mail address?', ['Yes', 'No']) == 'Yes' else 0

with expander_2:

    col3_form, col4_form = st.beta_columns(2)

    answers_dict['occupation_type'] = col3_form.selectbox('What is your job type?', categories_list['occupation_type'])

    answers_dict['income_type'] = col3_form.selectbox('What is your income type?', categories_list['income_type'])

    answers_dict['own_workphone'] = 1 if col3_form.selectbox('Do you have a work phone?', ['Yes', 'No']) == 'Yes' else 0

    answers_dict['annual_income'] = col3_form.slider('What is your monthly salary?', help = 'The slider can be moved using the arrow keys.', min_value = 0, max_value = 35000, step = 500) * 12

    answers_dict['years_working'] = col4_form.slider('How long have you been working (in years)?', help = 'The slider can be moved using the arrow keys.', min_value = 0, max_value = 50, step = 1)

    answers_dict['years_unemployed'] = col4_form.slider('How long have you been unemployed (in years)?', help = 'The slider can be moved using the arrow keys.', min_value = 0, max_value = 50, step = 1)




    

with expander_3:

    col4_form, col5_form = st.beta_columns(2)

    answers_dict['housing_type'] = col4_form.selectbox('What is your housing type?', categories_list['housing_type'])

    answers_dict['own_property'] = 1 if col4_form.selectbox('Do you own property?', ['Yes', 'No']) == 'Yes' else 0

    answers_dict['family_size'] = col5_form.slider('What is your family size?', help = 'The slider can be moved using the arrow keys.', min_value = 1, max_value = 20, step = 1)

    answers_dict['children_count'] = col5_form.slider('How many children do you have?', help = 'The slider can be moved using the arrow keys.', min_value = 0, max_value = 20, step = 1)

if st.button('Evaluate Credit') and validate_data(answers_dict):
	if denied_validation(answers_dict):
		st.error('Credit Denied.')
	else:
		st.success('Credit Approved.')
