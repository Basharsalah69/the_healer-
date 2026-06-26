from django.shortcuts import render,redirect
from.models import Person,Assements
from .form import interoForm,RegistrationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User,Group
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail

# Create your views here.
def sign_up(request):       
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
           user = form.save()
           Person.objects.create(
        user=user,
        date_of_birth=form.cleaned_data["date_of_birth"],
        gender=form.cleaned_data["gender"]
    )
           patien_group,created = Group.objects.get_or_create(name="Patients")
           user.groups.add(patien_group)
           login(request,user)
           return redirect("show")
        else:
            print(form.errors)   
    else:
        form=RegistrationForm()
    return render(request,"registration/sign_up.html",{"form":form})     
@login_required(login_url='/login/')
def music_therapy(request):
    return render(request,"scales/help_music.html")   
    
def phq9_scorring(request):
    if request.method=="POST":
        scor_1= int(request.POST.get("q1"))
        scor_2=int(request.POST.get("q2"))
        scor_3=int(request.POST.get("q3"))
        scor_4=int(request.POST.get("q4"))
        scor_5=int(request.POST.get("q5"))
        scor_6=int(request.POST.get("q6"))
        scor_7=int(request.POST.get("q7"))
        scor_8=int(request.POST.get("q8"))
        scor_9=int(request.POST.get("q9"))
        total_score=scor_1+scor_2+scor_3+scor_4+scor_5+scor_6+scor_7+scor_8+scor_9
        return total_score
def gad_scorring(request):
    if request.method=="POST":
        scor_1= int(request.POST.get("q_1"))
        scor_2=int(request.POST.get("q_2"))
        scor_3=int(request.POST.get("q_3"))
        scor_4=int(request.POST.get("q_4"))
        scor_5=int(request.POST.get("q_5"))
        scor_6=int(request.POST.get("q_6"))
        scor_7=int(request.POST.get("q_7"))
        total_score2=scor_1+scor_2+scor_3+scor_4+scor_5+scor_6+scor_7
        return total_score2
    
@login_required(login_url="/login/")        
def show(request):
    
    one_week_ago = timezone.now() - timedelta(days=7)
    submitted = Assements.objects.filter(user=request.user,complete_at__gte=one_week_ago).exists()
    if submitted:
        return render(request,"scales/end.html") 
    else:
        redirect("show")
    
    return render(request, "scales/main.html")
    
    
# 
@login_required(login_url='/login/')
def phq9(request):
   
    if request.method == "POST":
        total_score = phq9_scorring(request)
        data= Assements.objects.create(user=request.user, score_phq9=total_score)
        request.session["data_id"] = data.id
        

        

      

        return redirect("gad7")

    return render(request, "scales/phq9.html")
@login_required(login_url='/login/')
def gad7(request):
     
      if request.method=="POST":
   
        total_score=gad_scorring(request)
        data_id = request.session.get("data_id")

        if not data_id:
            return redirect("phq9")

        data = Assements.objects.get(id=data_id)
        data.score_gad7 = total_score
        data.save()
        if data.score_gad7 and data.score_phq9 >=20:
             return redirect("music")  
            
        
        
        
        return render(request,"scales/end.html")
      return render(request,'scales/gad7.html')
def is_doctor(user):
     return user.groups.filter(name="Doctors").exists()
     
      
@login_required(login_url="/login/")
@user_passes_test(is_doctor, login_url="/login/")
def doc_dash(request):

    search = request.GET.get("search")

    assessment = Assements.objects.all()

    if search:
        assessment = assessment.filter(
            user__username__icontains=search
        )

    return render(
        request,
        "scales/doctor_dashboard.html",
        {"assessment": assessment,"search": search}
    )
    


        
