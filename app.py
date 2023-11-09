from flask import Flask, request, jsonify
import joblib
import re
import numpy as np

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load(r'C:\Users\hp\Desktop\AIDI\CAPSTONE\results\lr_model.pkl') 
vectorization = joblib.load(r'C:\Users\hp\Desktop\AIDI\CAPSTONE\results\TFIDF_vectorization.pkl') 


def clean_text(text):
    # Remove extra white spaces by replacing multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', text)

    # Trim the text by removing leading and trailing spaces
    cleaned_text = cleaned_text.strip()

    # Convert the text to lowercase
    cleaned_text = cleaned_text.lower()

    return cleaned_text

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['text']
    
    ## text clean
    #text = np.array([clean_text(text)]).reshape(1, -1)
    text = clean_text(text)
    print('-------------------------------')
    print('Input Review = ',text)
    print('-------------------------------')
    text = vectorization.transform([text])
    
    # Make a prediction using the loaded model
    prediction = model.predict(text)[0]
    
    print('-------------------------------')
    print('Prediction = ',prediction)
    print('-------------------------------')

    return jsonify({'prediction': int(prediction)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
