# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from tinder.models import upload_foto
from tinder.models import rating
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
        other_users_photos = upload_foto.objects.values('foto', 'id').filter(~Q(user_id = current_user.id)).order_by('?').first()
        return render_to_response(
            'photo_content.html',
            { 'other_users_photos': other_users_photos },
           context_instance=RequestContext(request)
        )

class Like_photo():
    def post(self, request):
        current_user = request.user
        insert_like = rating(user_id=current_user,foto_id=1)
        insert_like.save()
class List(View):
    def get(self, request):
        form = PhotoForm() # A empty, unbound form
        current_user = request.user
        photos = upload_foto.objects.filter(user_id = current_user.id).values()
        # Render list page with the documents and the form
        return render_to_response(
            'my_photos.html',
            {'photos': photos, 'form': form },
            context_instance=RequestContext(request)
        )
    def post(self, request):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = upload_foto(foto = request.FILES['foto'])
            newdoc.user_id = request.user.id
            newdoc.save()
            # Redirect to the document list after POST
            return redirect('/my_photos')