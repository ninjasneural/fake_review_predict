from flask import Flask, request, jsonify
import joblib
import re
import numpy as np
import torch
import torch.nn as nn

app = Flask(__name__)

class SequentialModel(nn.Module):
    def __init__(self, input_dim):
        super(SequentialModel, self).__init__()
        self.seq_model = nn.Sequential(
            nn.Linear(input_dim, 128, bias=False),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, inputs):

        return self.seq_model(inputs)

# Instantiate the model
model = SequentialModel(input_dim=512)


# Load the pre-trained model
# model = joblib.load(r'C:\Users\hp\Desktop\AIDI\CAPSTONE\results\SNN_model_v1.pkl') 
# model = torch.load(r'C:\Users\hp\Desktop\AIDI\CAPSTONE\results\SNN_model_v1.pkl')
vectorization = joblib.load(r'C:\Users\hp\Desktop\AIDI\CAPSTONE\results\TFIDF_vectorization_v1.pkl') 

# Load the saved model state dictionary
model.load_state_dict(torch.load(r'C:\Users\hp\Desktop\AIDI\CAPSTONE\results\SNN_model_state.pth', map_location=torch.device('cpu')))

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
    text = torch.tensor(text, dtype=torch.float32)
    
    # Make a prediction using the loaded model
    prediction = model.predict(text)[0]
    
    print('-------------------------------')
    print('Prediction = ',prediction)
    print('-------------------------------')

    return jsonify({'prediction': int(prediction)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
