from django.contrib.auth.models import User, Group 
from .models import Coins, Rating
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CoinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coins
        fields = ('name', 'symbol')

class RatingSerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.SerializerMethodField('get_symbol_name')
    symbol = serializers.SerializerMethodField('get_symbol_symbol')

    def get_symbol_name(self, model):
        return model.name_coin.name

    def get_symbol_symbol(self, model):
        return model.name_coin.symbol

    # name_coin = CoinSerializer()

    class Meta:
        model = Rating
        fields = ('rating', 'name', 'symbol', 'market_cap', 'price', 'supply', 'volume', 'h1', 'h24', 'd7', 'pub_date')

 
    
