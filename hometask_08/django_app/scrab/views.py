 
from django.utils import timezone
from .models import User, Rating, Coins
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Max
from .forms import SearchForm, UserForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

 
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
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        #profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid()  :
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

    else:
        user_form = UserForm()

    return render(request,
                  'scrab/register.html',
                  {'user_form': user_form,
                   
                   'registered': registered
                  })


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
    queryset = Coins.objects.all()
    serializer_class = CoinSerializer

class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    latest = Rating.objects.latest('pub_date')
    queryset = Rating.objects.filter(pub_date = latest.pub_date)

    
    #queryset = Rating.objects.all().order_by('-pub_date')[:5]
    serializer_class = RatingSerializer



 
