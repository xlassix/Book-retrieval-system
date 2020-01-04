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
        return render(request, self.template_name, {'form': form})
class Profile_view(View):
    template_name = 'pages/profile.html'
    form_class=None
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'user_active': 'active',"form":form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form)
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
            else:
                data=form.get_data()
                user = authenticate(username=data['username'], password=data['password'])
                if user is not None:
                    return redirect('/home')
                else:
                    form.add_error('password', "invalid credentials")
        return render(request, self.template_name, {'form': form})

