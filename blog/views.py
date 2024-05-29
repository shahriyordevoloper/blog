
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
# from django.db.models import Count
from rest_framework import generics
from .models import *
from .serializers import *
# from .filters import LastMonthFilterBackend
# from django.utils import timezone
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status


class Most_views(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.order_by('-views').filter(is_active=True)

# class Most_mount(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = ParentSerializer

#     def get_queryset(self,month):
#         return Post.objects.order_by('-views').filter(date__month=month)
    

# class Most_mount(generics.ListAPIView):
#     end_date = datetime.now().replace(day=1)
#     start_date = end_date - timedelta(days=30)
#     queryset = Post.objects.all().filter(date__gte=start_date, date__lt=end_date)
#     # queryset = Post.objects.all()
#     serializer_class = BookSerializer
#     print(end_date , start_date , '*********')

class Most_mount(generics.ListAPIView):

    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    # filter_backends = [LastMonthFilterBackend]
    
    def get_queryset(self):
        end_date = datetime.now().replace(day=1)
        start_date = end_date - timedelta(days=30)
        print(start_date , end_date , '*********')
        return Post.objects.all().filter(date__gt=now() - timedelta(days=1)).order_by('-views').filter(is_active=True)

class Explanation(generics.ListAPIView):

    serializer_class = PostSerializer
    
    def get_queryset(self):

        return Post.objects.all().filter(is_active=True,explanation=True).order_by('-views')


class Post_add(generics.ListCreateAPIView):

    queryset = Post.objects.all()
    serializer_class = AddSerializer
    

class ParentDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = ParentSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
# Home page
@login_required(login_url='login')
def index(request):
    end_date = datetime.now().replace(day=1)
    start_date = end_date - timedelta(days=30)

    data = Post.objects.all().filter(is_active=True).order_by('-views')
    if request.GET.get('by') != None:
        cat = Category.objects.get(id=request.GET.get('by'))
        data = Post.objects.all().filter(is_active=True,category=cat).order_by('-views')

    context = {
        'post':data,
        'cat':Category.objects.all()
    }

    return render(request, 'index.html', context=context)

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')


