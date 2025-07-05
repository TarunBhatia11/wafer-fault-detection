from wsgiref import simple_server
from flask import Flask, request, render_template, jsonify
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction
import json

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']
            print ("path: ", path)

            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path,json_predictions = pred.predictionFromModel()

            return Response(" Prediction File created at "  +str(path) +'and few of the predictions are '+str(json.loads(json_predictions) ))
        elif request.form is not None:
            path = request.form['filepath']

            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path,json_predictions = pred.predictionFromModel()

            return Response("Prediction File created at " + str(path) + 'and Few of the predictions are \n' + str(
                json.loads(json_predictions)))

        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():

    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']

            train_valObj = train_validation(path) #object initialization

            train_valObj.train_validation()#calling the training_validation function


            trainModelObj = trainModel() #object initialization
            trainModelObj.trainingModel() #training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")

port = int(os.getenv("PORT",2809))
if __name__ == "__main__":
    host = '0.0.0.0'
    #port = 2809
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
    app.run(debug=True)


# from flask import Flask, request, jsonify, Response
# import os
# from prediction_Validation_Insertion import pred_validation
# from predictFromModel import prediction
# from training_Validation_Insertion import train_validation
# from trainingModel import trainModel
# from flask_cors import CORS, cross_origin

# app = Flask(__name__)
# CORS(app)

# @app.route("/predict", methods=['POST'])
# @cross_origin()
# def predict_route():
#     try:
#         data = request.json
#         file_path = data.get('Prediction_Batch_files')
        
#         if file_path:
#             pred_val = pred_validation(file_path)  # Object initialization
#             pred_val.prediction_validation()  # Call validation

#             pred = prediction(file_path)  # Prediction initialization
#             path, json_predictions = pred.predictionFromModel()  # Get predictions
            
#             return jsonify({"path": path, "predictions": json_predictions})
#         else:
#             return Response("File path not provided", status=400)
    
#     except Exception as e:
#         return Response(f"Error occurred: {e}", status=500)

# @app.route("/train", methods=['POST'])
# @cross_origin()
# def train_route():
#     try:
#         data = request.json
#         folder_path = data.get('Prediction_Batch_files')
        
#         if folder_path:
#             train_val = train_validation(folder_path)  # Validation initialization
#             train_val.train_validation()  # Validation call

#             train_model = trainModel()  # Training initialization
#             train_model.trainingModel()  # Training call
            
#             return Response("Training successful!", status=200)
#         else:
#             return Response("Folder path not provided", status=400)
    
#     except Exception as e:
#         return Response(f"Error occurred: {e}", status=500)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=2809)



# import streamlit as st
# import os
# import pandas as pd
# from prediction_Validation_Insertion import pred_validation
# from predictFromModel import prediction
# from training_Validation_Insertion import train_validation
# from trainingModel import trainModel

# # Setting page title and layout
# st.set_page_config(page_title="Wafer Fault Detection", layout="centered")

# # Title
# st.title("Wafer Fault Detection")

# # File upload for custom predictions
# st.subheader("Custom File Prediction")
# uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
# uploaded_df = pd.read_csv(uploaded_file)
# st.write("Uploaded File Preview:")
# st.dataframe(uploaded_df.head())


# if uploaded_file is not None:
#     st.write("File uploaded successfully. Processing...")
    
#     # Save the uploaded file temporarily
#     temp_dir = "temp_files"
#     os.makedirs(temp_dir, exist_ok=True)  # Create temp directory if it doesn't exist
#     temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    
#     # with open(temp_file_path, "wb") as f:
#     #     f.write(uploaded_file.getbuffer())
    
#     try:
#         # Validate and predict
#         # pred_val = pred_validation(temp_file_path)
#         # pred_val.prediction_validation()  # Validation step

#         # pred = prediction(temp_file_path)
#         # path, json_predictions = pred.predictionFromModel()  # Predict from model
        
#         # # Display the results
#         # st.success("Prediction successful!")
#         # st.write(f"Processed file saved at: {path}")
#         # st.json(json_predictions)
#         if temp_file_path:
#             pred_val = pred_validation(temp_file_path)  # Object initialization
#             pred_val.prediction_validation()  # Call validation

#             pred = prediction(temp_file_path)  # Prediction initialization
#             path, json_predictions = pred.predictionFromModel()  # Get predictions
            
#             # # Display the results
#             st.success("Prediction successful!")
#             st.write(f"Processed file saved at: {path}")
#             st.json(json_predictions)
            
#         else:
#             st.write("File Not found")
#     except Exception as e:
#         st.error(f"An error occurred during prediction: {e}")

# # Training Section
# st.subheader("Training the Model")

# if st.button("Start Training"):
#     try:
#         folder_path = "Training_Batch_files"
        
#         if not os.path.isdir(folder_path):
#             st.error("Training batch files directory does not exist!")
#         else:
#             train_val = train_validation(folder_path)
#             train_val.train_validation()  # Validation step

#             train_model = trainModel()
#             train_model.trainingModel()  # Train the model
            
#             st.success("Training completed successfully!")
#     except Exception as e:
#         st.error(f"An error occurred during training: {e}")

# # Results display section
# st.subheader("Detecting Defective Wafers Manually")
# static_dir = os.path.join("static", "css")  # Directory for wafer images
# col1, col2, col3 = st.columns(3)

# # Display wafer images with captions
# with col1:
#     st.image(os.path.join(static_dir, "img1.jpg"), caption="Wafer Image 1", use_column_width=True)
# with col2:
#     st.image(os.path.join(static_dir, "img2.jpg"), caption="Wafer Image 2", use_column_width=True)
# with col3:
#     st.image(os.path.join(static_dir, "img3.jpg"), caption="Wafer Image 3", use_column_width=True)

