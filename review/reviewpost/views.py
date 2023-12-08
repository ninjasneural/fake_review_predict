from django.shortcuts import render
from reviewpost.models import Review

from datetime import datetime
import joblib
import re
import torch
import torch.nn as nn
import numpy as np

# Create your views here.
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

# model = joblib.load(r'C:\Users\athul\Desktop\Review_system\review\static\lr_model.pkl')
# vectorization = joblib.load(r'C:\Users\athul\Desktop\Review_system\review\static\TFIDF_vectorization.pkl')

vectorization = joblib.load(r'C:\Users\athul\Desktop\Review_system\review\static\TFIDF_vectorization_v1.pkl')

# Load the saved model state dictionary
model.load_state_dict(
    torch.load(r'C:\Users\athul\Desktop\Review_system\review\static\SNN_model_state.pth', map_location=torch.device('cpu')))

def clean_text(text):
    # Remove extra white spaces by replacing multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', text)

    # Trim the text by removing leading and trailing spaces
    cleaned_text = cleaned_text.strip()

    # Convert the text to lowercase
    cleaned_text = cleaned_text.lower()

    return cleaned_text


def review(request):
    ss=request.session["u_id"]
    if request.method=='POST':
        obb=Review()
        obb.review=request.POST.get('review')
        obb.user_id=ss
        obb.date=datetime.today()

        text = clean_text(obb.review)
        print('-------------------------------')
        print('Input Review = ', text)
        print('-------------------------------')
        text = vectorization.transform([text])
        text = torch.tensor(text.toarray(), dtype=torch.float32)

        # Make a prediction using the loaded model
        prediction = model(text)[0]

        print('-------------------------------')
        print('Prediction = ', prediction)
        print('-------------------------------')


        if prediction<.5:
            aa='This review is Fake'
        else:
            aa='This Review is genuine'
        obb.status = aa
        obb.save()
        context={
            'kk': aa
        }
        return render(request,'reviewpost/review.html',context)
    return render(request,'reviewpost/review.html')


 # I love this product.

# I bought a blue Levi's shirt.I got this red one. Its ridiculous



def history(request):
    ss=request.session["u_id"]
    obb=Review.objects.filter(user_id=ss)
    context={
        'kk':obb
    }
    return render(request,'reviewpost/viewhistory.html',context)