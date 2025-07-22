from django import forms
from .models import SmartHomeProduct
from .models import Property

class SmartHomeProductForm(forms.ModelForm):
    class Meta:
        model = SmartHomeProduct
        fields = ['name', 'image', 'price', 'category']


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'mobile', 'address', 'price', 'image' , 'url']
