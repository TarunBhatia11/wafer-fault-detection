# # import streamlit as st

# # # Setting page title and layout
# # st.set_page_config(page_title="Wafer Fault Detection", layout="centered")

# # # Title
# # st.title("Wafer Fault Detection")

# # # File input form
# # st.subheader("Custom File Prediction")
# # with st.form(key="datafetch_form"):
# #     csv_file = st.text_input("Enter absolute file path", "")
# #     submit_button = st.form_submit_button(label="Custom File Predict")

# #     # If the form is submitted
# #     if submit_button:
# #         if csv_file:
# #             # Placeholder for file processing code
# #             st.write(f"Processing custom file at: {csv_file}")
# #         else:
# #             st.warning("Please enter a valid file path.")

# # st.subheader("Or")
# # # Default file prediction button
# # if st.button("Default File Predict"):
# #     default_file_path = "Prediction_Batch_files"
# #     # Placeholder for default file processing code
# #     st.write(f"Processing default file at: {default_file_path}")

# # # Results display section
# # st.subheader("Results")
# # result_placeholder = st.empty()  # This will display the results later

# # # Placeholder for any JSON result or prediction output
# # # result_placeholder.write('Prediction results will appear here.')

# # # Image display
# # st.subheader("Detecting defective wafers manually")
# # col1, col2, col3 = st.columns(3)
# # with col1:
# #     st.image("static\css\img1.jpg", caption="Wafer Image 1", use_column_width=True)
# # with col2:
# #     st.image("static\css\img2.jpg", caption="Wafer Image 2", use_column_width=True)
# # with col3:
# #     st.image("static\css\img3.jpg", caption="Wafer Image 3", use_column_width=True)



# import streamlit as st
# import requests
# import json

# # Setting page title and layout
# st.set_page_config(page_title="Wafer Fault Detection", layout="centered")

# # Title
# st.title("Wafer Fault Detection")

# # Flask API URL
# api_url = "http://localhost:2809"

# # File input form
# st.subheader("Custom File Prediction")
# with st.form(key="datafetch_form"):
#     csv_file = st.text_input("Enter absolute file path", "")
#     submit_button = st.form_submit_button(label="Custom File Predict")

#     # If the form is submitted
#     if submit_button:
#         if csv_file:
#             # Send request to Flask API
#             response = requests.post(f"{api_url}/predict", json={"filepath": csv_file})
#             if response.status_code == 200:
#                 result = response.json()
#                 st.write(f"Processed file at: {result['path']}")
#                 st.json(result['predictions'])
#             else:
#                 st.warning("Failed to process file. Please check the file path.")
#         else:
#             st.warning("Please enter a valid file path.")

# st.subheader("Or")
# # Default file prediction button
# if st.button("Default File Predict"):
#     default_file_path = 'Prediction_Batch_files'
#     # Send request to Flask API
#     response = requests.post(f"{api_url}/predict", json={"filepath": default_file_path})
#     if response.status_code == 200:
#         result = response.json()
#         st.write(f"Processed default file at: {result['path']}")
#         st.json(result['predictions'])
#     else:
#         st.warning("Failed to process default file.")

# # Results display section
# st.subheader("Results")
# result_placeholder = st.empty()  # This will display the results later

# # Display wafer images
# st.subheader("Detecting Defective Wafers Manually")
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.image("static/css/img1.jpg", caption="Wafer Image 1", use_column_width=True)
# with col2:
#     st.image("static/css/img2.jpg", caption="Wafer Image 2", use_column_width=True)
# with col3:
#     st.image("static/css/img3.jpg", caption="Wafer Image 3", use_column_width=True)
import streamlit as st
import requests
import json
import os

# Setting page title and layout
st.set_page_config(page_title="Wafer Fault Detection", layout="centered")

# Title
st.title("Wafer Fault Detection")

# Flask API URL
api_url = "http://localhost:2809"

# File upload form for custom file prediction
st.subheader("Custom File Prediction")
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Save the uploaded file temporarily
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)  # Create temp directory if it doesn't exist
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    
    # Write the file to the temp directory
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Send request to Flask API with the temporary file path
    response = requests.post(f"{api_url}/predict", json={"filepath": temp_file_path})
    if response.status_code == 200:
        result = response.json()
        st.write(f"Processed file at: {result['path']}")
        st.json(result['predictions'])
    else:
        st.warning("Failed to process the uploaded file.")

st.subheader("Or")

# Default file prediction button
if st.button("Default File Predict"):
    # Define the path to the default directory containing batch files
    default_dir = 'Prediction_Batch_files'
    if not os.path.isdir(default_dir):
        st.error("Default directory does not exist!")

        # Select the first CSV file in the directory for prediction
        files = [f for f in os.listdir(default_dir) if f.endswith(".csv")]
        if files:
            default_file_path = os.path.join(default_dir, files[0])
            # Send request to Flask API with the file path
            response = requests.post(f"{api_url}/predict", json={"Prediction_Batch_files": temp_file_path})
            if response.status_code == 200:
                result = response.json()
                st.write(f"Processed default file at: {result['path']}")
                st.json(result['predictions'])
            else:
                st.warning("Failed to process the default file.")
        else:
            st.warning("No CSV files found in the default directory.")
    else:
        st.error("Default directory not found. Please check the path.")

# Results display section
st.subheader("Results")
result_placeholder = st.empty()  # Placeholder for results display

# Display wafer images with correct path handling
st.subheader("Detecting Defective Wafers Manually")
static_dir = os.path.join("static", "css")  # Directory for wafer images
col1, col2, col3 = st.columns(3)

# Display wafer images with captions
with col1:
    st.image(os.path.join(static_dir, "img1.jpg"), caption="Wafer Image 1", use_column_width=True)
with col2:
    st.image(os.path.join(static_dir, "img2.jpg"), caption="Wafer Image 2", use_column_width=True)
with col3:
    st.image(os.path.join(static_dir, "img3.jpg"), caption="Wafer Image 3", use_column_width=True)

