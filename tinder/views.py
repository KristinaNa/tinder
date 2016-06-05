# -*- coding: utf-8 -*-
import time
from cloudinary.templatetags import cloudinary
from django.contrib.sites import requests
from django.shortcuts import render_to_response
from django.template import RequestContext
from tinder.models import *
from tinder.forms import PhotoForm
from django.views.generic.edit import FormView
from .forms import UserCreationForm
from .forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.models import User
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.utils.dateformat import format
import os
from django.contrib.auth.decorators import login_required


def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "register.html"
    def form_valid(self, form):
        form.save()
        #get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password1']
        #authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)



class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/history"
    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

class Photos(View):
    # template_name = "photos.html"
    def get(self, request):
        return render_to_response(
            'photos.html',
           context_instance=RequestContext(request)
        )
    def post(self, request):
        current_user = request.user
        photo_id = request.POST.get('photo_id')
        like = request.POST.get('like')

        if like == 'true' and photo_id is not None:
            insert_like = Rating(user_id=current_user.id,photo_id= photo_id)
            insert_like.save()

        rated_photos = ValuesQuerySetToDict(Rating.objects.filter(user_id = current_user.id).values_list('photo_id', flat=True))
        if photo_id is not None: rated_photos.append(photo_id)

        all_photos = Photo.objects.values('photo','id').filter(~Q(user_id = current_user.id)).exclude(id__in=rated_photos).order_by('?').first()

        return render_to_response(
            'photo_content.html',
            { 'other_users_photos': all_photos },
           context_instance=RequestContext(request)
        )

class List(View):
    def get(self, request):
        form = PhotoForm() # A empty, unbound form
        current_user = request.user
        photos = Photo.objects.filter(user_id = current_user.id)
        # Render list page with the documents and the form
        photo_id = request.POST.get('photo_id')
        photo_rating = Rating.objects.filter(photo_id = photo_id).count()

        return render_to_response(
            'my_photos.html',
            {'photos': photos, 'form': form, 'photo_rating': photo_rating },
            context_instance=RequestContext(request)
        )
    def post(self, request):
        form = PhotoForm(request.POST, request.FILES)
        timestamp_string = str(time.time())
        file=request.FILES['foto'].name
        file=os.path.splitext(file)[0]
        file_name=timestamp_string+"_"+file

        if form.is_valid():
            cloudinary.uploader.upload(request.FILES['foto'], public_id = file_name )
            p = Photo(user_id=request.user.id, photo=file_name)
            p.save()

            # Redirect to the document list after POST
            return redirect('/my_photos')

class History(View):
    def get(self, request):
        rated_photos = Rating.objects.select_related('user', 'photo', 'rating').values('user__username', 'photo__photo', 'created_at').order_by('-created_at')

        return render_to_response(
            'history.html',
            {'rated_photos': rated_photos},
            context_instance=RequestContext(request)
        )

class Main(View):
    def get(self, request):

        if request.user.is_authenticated():
            return redirect('/history')
        else:
            return render_to_response(
                'main.html',
                context_instance=RequestContext(request)
            )