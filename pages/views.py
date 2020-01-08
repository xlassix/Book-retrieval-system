from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import get_user_model, authenticate
from django.contrib import messages
from django.http import HttpResponse
from .resources import BooksResource
from .models import Books
import json
from django.db.models import Q
from django.core.paginator import Paginator
from django.core import serializers
class Dashboard_view(View):
    template_name = 'pages/home.html'
    #return super(Api, self).dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        try:
            if request.session['search'].strip()=='':
                raise ValueError
            data=[i for i in serializers.deserialize("json", request.session['data'])]
            self.paginator = Paginator(data, 25)
            page = request.GET.get('page',1)
            pages = self.paginator.get_page(page)
            object_list=Books.objects.filter(pk__in=[i.object.pk for i in pages])
            #print(list(object_list))
            return render(request, self.template_name, {"content_pages":pages,"object_list":list(object_list),'dash_active': 'active',"search":request.session['search']})
        except:
            self.paginator = Paginator(Books.objects.all(), 25)
            page = request.GET.get('page',1)
            pages = self.paginator.get_page(page)
            return render(request, self.template_name, {"object_list":pages,"content_pages":pages,'dash_active': 'active'})

    def post(self, request, *args, **kwargs):
        search=request.POST['search']
        request.session["search"]=search
        if search.strip()=="":
            self.paginator = Paginator(Books.objects.all(), 25)
            page = request.GET.get('page',1)
            pages = self.paginator.get_page(page)
            return render(request, self.template_name, {"object_list":pages,"content_pages":pages,'dash_active': 'active'})
        else:
            self.query=Books.objects.filter(Q(original_title__icontains=search) | Q(title__icontains=search)| Q(original_publication_year__icontains=search)|Q(authors__icontains=search)|Q(isbn__icontains=search)).order_by('-average_rating')
            #object_list =[i for i in self.query]
            self.paginator = Paginator(self.query, 25) # Show 25 contacts per page
            request.session["data"]=serializers.serialize("json", self.query)
            page = request.GET.get('page',1)
            pages = self.paginator.get_page(page)
            return render(request, self.template_name, {"content_pages":pages,"object_list":pages,'dash_active': 'active',"search":request.session['search']})
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



def export(request):
    person_resource = BooksResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books_in_db.csv"'
    return response



from tablib import Dataset

def simple_upload(request):
    if request.method == 'POST':
        book_resource = BooksResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        dataset.load(new_persons.read().decode('utf-8'))
        result = book_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            book_resource.import_data(dataset, dry_run=False)  # Actually import now
    return render(request, 'core/simple_upload.html')



class Management_view(View):
    template_name = 'pages/management.html'

    def get(self, request, *args, **kwargs):
        messages.add_message(
                request, messages.SUCCESS, 'connect to database',
                fail_silently=True,
            )
        return render(request, self.template_name, {'not_active': 'active'})

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        book_resource = BooksResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        dataset.load(new_persons.read().decode('utf-8'))
        result = book_resource.import_data(dataset, dry_run=True,raise_errors=True)  # Test the data import

        if not result.has_errors():
            messages.add_message(
                request, messages.SUCCESS, 'success',
                fail_silently=True,
            )
            book_resource.import_data(dataset, dry_run=False)
            messages.add_message(
                request, messages.SUCCESS, 'success',
                fail_silently=True,
            )
        else:
            messages.error(request,"An error occured") # Actually import now
            messages.add_message(
                request, messages.WARNING, 'invalid',
                fail_silently=True,
            )
        return render(request, self.template_name, {'not_active': 'active'})