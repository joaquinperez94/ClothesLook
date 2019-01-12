# -*- encoding: utf-8 -*-
from django import forms
from clothesLookApp.models import Clothing
from dataclasses import fields

class registrerClote(forms.ModelForm):
    class Meta:
        model = Clothing
        
        fields = [
            'name',
            'photo',
            'size',
            'brand',
            'link',
            'category',
            ]
        
        labels = {
            'name': 'Name',
            'photo': 'Photo',
            'size': 'Size',
            'brand': 'Brand',
            'link': 'Link',
            'category': 'Category',
            }
        
        widgets = {
             'name': forms.TextInput(attrs={'class':'form-control'}),
            'photo': forms.TextInput(attrs={'class':'form-control'}),
            'size': forms.TextInput(attrs={'class':'form-control'}),
            'brand': forms.TextInput(attrs={'class':'form-control'}),
            'link': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            }
