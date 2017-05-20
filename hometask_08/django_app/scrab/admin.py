from django.contrib import admin

# Register your models here.
from .models import User, Coins, Rating

admin.site.register(User)
admin.site.register(Coins)
admin.site.register(Rating)
