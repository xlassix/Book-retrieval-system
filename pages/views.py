from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import get_user_model, authenticate
from django.contrib import messages


class Dashboard_view(View):
    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'dash_active': 'active'})

    def post(self, request, *args, **kwargs):
        form=None
        if form.is_valid():
            if form.register:
                email,username,password,extra_data=form.get_data()
                User = get_user_model()
                User.objects.create_user(email=email,username=username, password=password,**extra_data)
                return HttpResponseRedirect('')
            else:
                data=form.get_data()
                user = authenticate(username=data['username'], password=data['password'])
                if user is not None:
                    return HttpResponseRedirect('/home')
                else:
                    form.add_error('password', "invalid credentials")
        return render(request, self.template_name, {'form': form,'dash_active': 'active'})
class Profile_view(View):
    template_name = 'pages/profile.html'
    form_class=None
    form_update=None
    form_update_mail=None
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form_update= self.form_update()
        form_update_mail= self.form_update_mail()
        return render(request, self.template_name, {'user_active': 'active',"form":form,'form_update':form_update,'form_update_mail':form_update_mail})

    def post(self, request, *args, **kwargs):
        if "password" in request.POST:
            form = self.form_class(request.POST)
            form_update= self.form_update()
            form_update_mail=self.form_update_mail()
            if form.is_valid():
                data=form.get_data()
                if form.change_password:
                    if (request.user.check_password(data['password'])):
                        request.user.set_password(data["password1"])
                        request.user.save()
                        messages.add_message(
                            request, messages.SUCCESS, 'Profile details updated.',
                            fail_silently=True,
                        )
                    else:
                        form.add_error('password', "password incorrect")
        elif "email" in request.POST:
            form_update_mail=self.form_update_mail(request.POST)
            form=self.form_class()
            form_update=self.form_update()
            if form_update_mail.is_valid():
                data=form_update_mail.get_data()
                request.user.update_mail(data["email"])
                messages.add_message(
                    request, messages.SUCCESS, 'Profile details updated.',
                    fail_silently=True,
                )
        elif "first_name" in request.POST:
            form_update_mail=self.form_update_mail()
            form=self.form_class()
            form_update=self.form_update(request.POST)
            if form_update.is_valid():
                data=form_update.get_data()
                request.user.update_names(data["first_name"],data['last_name'])
                messages.add_message(
                    request, messages.SUCCESS, 'Profile details updated.',
                    fail_silently=True,
                )
        else:
            messages.add_message(
                request, messages.ERROR, 'An Error occurred',
                fail_silently=True,
            )
        return render(request, self.template_name, {'user_active': 'active',"form":form,'form_update':form_update,'form_update_mail':form_update_mail})

