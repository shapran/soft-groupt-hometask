
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Max
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Rating, Coins
from .forms import SearchForm, UserForm

 
from rest_framework import viewsets
from  .serializers import UserSerializer, GroupSerializer, CoinSerializer, RatingSerializer

def index(request):
    ''' Displays all ratings '''
    #coins = Coins.objects.all().prefetch_related('rating')
    ## related_name for model
    ## MEta ordering in model
    
 

    #redirect to login form
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    
    #latest = Rating.objects.latest('pub_date')
    #ratings = Rating.objects.filter(pub_date = latest.pub_date)
    ratings = Rating.objects.all()[:830]


    return render(request, 'scrab/index.html', {'ratings': ratings})

@login_required(login_url="/login/")
def coin_rate(request, coin):
    """Displays separated coin rating"""
    coin_obj = get_object_or_404(Coins, symbol=coin.upper())
    ratings =  Rating.objects.filter(name_coin = coin_obj)
    return render(request, 'scrab/coin_rate.html', {'ratings': ratings})

@login_required(login_url="/login/")
def search(request):
        if request.method == "POST":
            form = SearchForm(request.POST or None)
             

            if request.method == 'POST' and  form.is_valid():
                search = form.cleaned_data['search']
                print(search)
                coin_obj = Coins.objects.filter(symbol__icontains=search)  | Coins.objects.filter(name__icontains=search) 
                 
                ratings = Rating.objects.filter(name_coin__in = coin_obj).order_by('name_coin', '-pub_date')
                return render(request, 'scrab/search.html', {'ratings': ratings})
        else:
            form = SearchForm()
        return redirect('', {})


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user_data = user_form.cleaned_data
            username = user_data['username']
            email = user_data['email']
            password = user_data['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/login/')
            else:
                user_form.add_error(None, 'Looks like a username with that email or password already exists')
                return render(request, 'scrab/register.html', {'form': user_form})

    else:
        user_form = UserForm()
    return render(request, 'scrab/register.html', {'user_form': user_form})


@login_required(login_url="/login/")
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
# If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
            # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
            # The request is not a HTTP POST, so display the login form.
            # This scenario would most likely be a HTTP GET.
    elif request.method == 'GET':
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        
    #else:
        return render(request, 'scrab/login.html', {})





class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CoinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = CoinSerializer

    queryset = Coins.objects.all()

class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = RatingSerializer

    # latest = Rating.objects.latest('pub_date')
    # queryset = Rating.objects.filter(pub_date = latest.pub_date).select_related('name_coin')
    data_set = [symbol.rating_set.all()[0]._db for symbol in Coins.objects.all().prefetch_related('rating_set')]
    queryset = Rating.objects.filter(_db__in=data_set).select_related('name_coin')



 
