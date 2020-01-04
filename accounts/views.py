from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import get_user_model, authenticate,login,logout

class Registration_view(View):
    form_class = None
    template_name = 'accounts/account.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.register:
                email,username,password,extra_data=form.get_data()
                User = get_user_model()
                User.objects.create_user(email=email,username=username, password=password,**extra_data)
                return HttpResponseRedirect('/')
            else:
                data=form.get_data()
                user = authenticate(username=data['username'], password=data['password'])
                if user is not None:
                    login(request,user)
                    return redirect('/home',request=request)
                else:
                    form.add_error('password', "invalid credentials")
        return render(request, self.template_name, {'form': form})
def Logout_view(request):
    logout(request)
    return redirect('/')