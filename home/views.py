from django.shortcuts import render, redirect
from home.models import Contact
from .models import *
from django.contrib import messages
import stripe
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Course
from django.views.decorators.csrf import csrf_protect

# Create your views here.

def base(request):
    context = {'course' : Course.objects.all()}
    return render(request, context)

def home(request):
    course = Course.objects.all()
    context = {'course': course}

    profile = None  # initialize profile variable with None

    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile is not None:
            request.session['profile'] = profile.is_pro

    context['profile'] = profile  # add profile to context

    return render(request, 'home.html', context)

def about(request):
    # return HttpResponse("Hello, world. You're at the about.(/about)")
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(
                request, "Your message has been successfully sent")
    return render(request, "Contact.html")


def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = Course.objects.none()
    else:
        name = Course.objects.filter(course_name__icontains=query)
        description = Course.objects.filter(course_description__icontains=query)
        # allPostsContent = Course.objects.filter(__icontains=query)
        allPosts = name.union( description)
    if allPosts.count() == 0:
        messages.warning(
            request, "No search results found. Please refine your query.")
    params = {'allPosts': allPosts, 'query': query}
    print(allPosts)
    return render(request, 'search.html', params)


def view_course(request, slug):
    course = Course.objects.filter(slug=slug).first()
    course_modules = CourseModule.objects.filter(course=course)
    link = course.video_link
    if link == None or len(link) == 0:
        context = {'course': course, 'course_modules': course_modules}
        return render(request, 'course.html', context)
    
    link = link[32:]
    link = "https://www.youtube.com/embed/"+link
    
    context = {'course': course, 'course_modules': course_modules, 'link':link}
    return render(request, 'course.html', context)


@login_required(login_url='/login/')
def become_pro(request):
    if request.method == 'POST':
        membership = request.POST.get('membership', 'MONTHLY')
        amount = 1000
        if membership == 'YEARLY':
            amount = 11000
        stripe.api_key = 'sk_test_qu7ivgHp9WRHlHJjs2QHugIA00hKFbC5qc'

        token = request.POST['stripeToken']
        customer = stripe.Customer.create(
            email="gautams1512@gmail.com",
            name=request.user.username,
            source=token
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount * 100,
            currency='inr',
            description="Membership",
        )

        if charge['paid'] == True:
            profile = Profile.objects.filter(user=request.user).first()
            if charge['amount'] == 100000:
                profile.subscription_type = 'M'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(30)
                profile.pro_expiry_date = expiry
                profile.save()

            elif charge['amount'] == 1100000:
                profile.subscription_type = 'Y'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(365)
                profile.pro_expiry_date = expiry
                profile.save()

        return redirect('/charge/')

    return render(request, 'become_pro.html')


def charge(request):
    return render(request, 'charge.html')


def login_attempt(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user is None:
            context = {'message': 'No user found', 'class': 'danger'}
            return render(request, 'login.html', context)
        else:
            user = authenticate(username=username, password=password)
            print(user)
            if user is None:
                context = {'message': 'Invalid credentials', 'class': 'danger'}
                return render(request, 'login.html', context)
            else:
                login(request, user)
                return redirect('home')
    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Check if the username already exists in the database
        if User.objects.filter(username=username).exists():
            context = {'message': 'Username already exists', 'class': 'danger'}
            return render(request, 'register.html', context)

        # Check if the email is already registered
        if email and User.objects.filter(email=email).exists():
            context = {'message': 'Email already registered',
                       'class': 'danger'}
            return render(request, 'register.html', context)

        # Create the new user if the username and email are available
        user = User(username=username, email=email)
        user.set_password(password)
        try:
            user.save()
        except IntegrityError as e:
            context = {'message': 'Error creating user: {}'.format(
                str(e)), 'class': 'danger'}
            return render(request, 'register.html', context)
        context = {'message': 'User created successfully', 'class': 'success'}
        return render(request, 'register.html', context)

    return render(request, 'register.html')


def logout_attempt(request):
    request.session.profile = None
    logout(request)
    return redirect('/')
