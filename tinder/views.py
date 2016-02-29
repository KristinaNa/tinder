# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from tinder.models import *
from tinder.forms import PhotoForm
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.models import User


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "register.html"
    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"
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

        if photo_id:
           # photo_id = request.POST.get('photo_id')
            insert_like = Rating(user_id=current_user.id,photo_id= photo_id)
            insert_like.save()

        rated_photos = Rating.objects.values_list('photo_id', flat=True).filter(user_id = current_user.id)
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
        if form.is_valid():
            newdoc = Photo(photo = request.FILES['foto'])
            newdoc.user_id = request.user.id
            newdoc.save()
            # Redirect to the document list after POST
            return redirect('/my_photos')

class History(View):
    def get(self, request):
        rated_photos = Rating.objects.select_related('user', 'photo', 'rating').values('user__username', 'photo__photo', 'created_at')

        return render_to_response(
            'history.html',
            {'rated_photos': rated_photos},
            context_instance=RequestContext(request)
        )
