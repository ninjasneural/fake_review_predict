from django.shortcuts import render
from reviewpost.models import Review

from datetime import datetime
import joblib
import re
import numpy as np

# Create your views here.
model = joblib.load(r'C:\Users\athul\Desktop\Review_system\review\static\lr_model.pkl')
vectorization = joblib.load(r'C:\Users\athul\Desktop\Review_system\review\static\TFIDF_vectorization.pkl')


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

        # Make a prediction using the loaded model
        prediction = model.predict(text)[0]

        print('-------------------------------')
        print('Prediction = ', prediction)
        print('-------------------------------')

        obb.status=prediction
        obb.save()
        if prediction==1:
            aa='This review is Fake'
        else:
            aa='This Review is genuine'
        context={
            'kk': aa
        }
        return render(request,'reviewpost/review.html',context)
    return render(request,'reviewpost/review.html')


 # I love this product.

# I bought a blue Levi's shirt.I got this red one. Its ridiculous