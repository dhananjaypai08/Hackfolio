from django.shortcuts import render, redirect
from hackapp.models import User, Hackathon
from hackapp.serializers import UserSerializer, HackathonSerializer
from hashlib import sha256
import requests
from datetime import datetime, date

UPDATE = 0

def login(request):
    if request.session.get('user_id'): return redirect(home)
    msg = {}
    if request.method == 'POST':
        name, email, password = request.POST.get('username'), request.POST.get('email'), request.POST.get('password')
        sha_password = sha256(password.encode()).hexdigest()
        users = User.objects.filter(name=name, email=email)
        for user in users:
            if user.password == sha_password:
                request.session['user_id'] = user.id
                return redirect(home)
        msg['status'] = 0
    return render(request, 'login.html', msg)

def register(request):
    if request.session.get('user_id'): return redirect(home)
    msg = {}
    if request.method == 'POST':
        name, email, password = request.POST.get('username'), request.POST.get('email'), request.POST.get('password')
        if User.objects.filter(email=email):
            msg['status'] = 2
        else:
            sha_password = sha256(password.encode()).hexdigest()
            try:
                user = User(name=name, email=email, password=sha_password)
                user.save()
                msg['status'] = 1
                
            except:
                msg['status'] = 0
    return render(request, 'register.html', msg)

def logout(request):
    if request.session.get('user_id'):
        del request.session['user_id']
    return redirect(home)

def home(request):
    msg = {}
    data = requests.get('http://127.0.0.1:8000/api/list/')
    msg['hackathons'] = data.json()
    if request.session.get('user_id'):
        msg['userdata'] = UserSerializer(User.objects.get(id=request.session.get('user_id'))).data
        return render(request, 'authhome.html', msg)
    return render(request, 'unauthhome.html', msg)

def hackathon(request, id):
    msg = {}
    hack = Hackathon.objects.get(id=id)
    serializer = HackathonSerializer(hack)
    data = serializer.data
    created = data['created'].split('T')
    created = created[0]+" "+created[1][:5]
    created = datetime.strptime(created, '%Y-%m-%d %H:%M')
    now = datetime.now()
    dateTimedifference = now-created
    differencehours = int(dateTimedifference.total_seconds() / 3600)
    if differencehours > 24:
        data['created'] = str(differencehours%24)+"days"
    else:
        data['created'] = str(differencehours)+"mins"
    msg['data'] = data
    return render(request, 'hackathonprofile.html', msg)

def user(request, id):
    msg = {}
    usr = User.objects.get(id=id)
    serializer = UserSerializer(usr)
    data = serializer.data
    msg['user'] = data
    hackathons = Hackathon.objects.filter(user=usr)
    hackserializer = HackathonSerializer(hackathons, many=True)
    msg['hackathons'] = hackserializer.data
    return render(request, 'userprofile.html', msg) 

def add(request):
    msg = {}
    if not request.session.get('user_id'): return redirect(home)
    if request.method == 'POST':
        title, description, start_datetime, end_datetime, submission, reward_prize = request.POST.get('title'), request.POST.get('description'), request.POST.get('start_datetime'), request.POST.get('end_datetime'), request.POST.get('submission'), int(request.POST.get('reward'))
        print(title, description, start_datetime, end_datetime, submission, reward_prize)
        bg_img, hackathon_img = request.FILES.get('bg_img'), request.FILES.get('hackathon_img')
        start_date, start_time = start_datetime.split('T')
        start_datetime = start_date+" "+start_time 
        end_date, end_time = end_datetime.split('T')
        end_datetime = end_date+" "+end_time
        user = User.objects.get(id=request.session.get('user_id'))
        try:
            hackathon = Hackathon(title=title, description=description, bg_img=bg_img, 
                                  hackathon_img=hackathon_img, submission=submission, 
                                  start_datetime=start_datetime, end_datetime=end_datetime, reward_prize=reward_prize, user=user)
            hackathon.save()
            msg['status'] = 1
        except:
            msg['status'] = 0
        
    return render(request, 'add.html', msg)

def deletehack(request,id):
    if not request.session.get('user_id'): return redirect(home)
    hack = Hackathon.objects.get(id=id)
    hack.delete()
    return redirect(home)

def update(request, id):
    if not request.session.get('user_id'): return redirect(home)
    msg = {}
    if request.method == 'POST':
        title, description, start_datetime, end_datetime, submission, reward_prize = request.POST.get('title'), request.POST.get('description'), request.POST.get('start_datetime'), request.POST.get('end_datetime'), request.POST.get('submission'), int(request.POST.get('reward'))
        bg_img, hackathon_img = request.FILES.get('bg_img'), request.FILES.get('hackathon_img')
        hackathon = Hackathon.objects.get(id=id)
        if not bg_img: bg_img = hackathon.bg_img
        if not hackathon_img: hackathon_img = hackathon.hackathon_img
        user = User.objects.get(id=request.session.get('user_id'))
        try:
            hackathon.title = title
            hackathon.description = description
            hackathon.start_datetime = start_datetime
            hackathon.end_datetime = end_datetime
            hackathon.submission = submission
            hackathon.reward_prize = reward_prize
            hackathon.bg_img = bg_img
            hackathon.hackathon_img = hackathon_img
            hackathon.save()
            msg['status'] = 1
        except:
            msg['status'] = 0
    hackathon = Hackathon.objects.get(id=id)
    serializer = HackathonSerializer(hackathon)
    msg['data'] = serializer.data
    return render(request, 'update.html', msg)