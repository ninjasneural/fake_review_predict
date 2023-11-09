from django.shortcuts import render
from reviewpost.models import Review
# Create your views here.
def review(request):
    ss=request.session["u_id"]
    if request.method=='POST':
        obb=Review()
        obb.review=request.POST.get('review')
        obb.user_id=ss
        obb.status='Pending'
        obb.save()

        
    return render(request,'reviewpost/review.html')