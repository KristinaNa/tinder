# -*- coding: utf-8 -*-
from django import forms

class PhotoForm(forms.Form):
    foto = forms.FileField(
        label='Select a file'
    )