from django.shortcuts import render, redirect
from django.views import View
from app.forms import LoginForm, RegistrationForm
from app.models import Bestdeal
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from  django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Profile , Address
from .forms import ProfileEditForm, PasswordReset, AddressEditForm
User = get_user_model()


# Create your views here.
class RegisterView(View):
    def get(self, request):
        context = {'register': True}
        return render(request, 'login.html', context)
    def post(self, request):
        #next_url = request.POST.get('next')
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=True)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            '''if User.objects.filter(email=email):
                return render(request, 'login.html', {'errors': 'The user exists please Login'})
            else:
                User.objects.create(username=first_name, first_name=first_name, last_name=last_name,
                                    password=password, email=email)'''
            return render(request, 'registration_success.html')
        else:
            print('invalid')
            return render(request, 'login.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        next_url = request.POST.get('next')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                if next_url:
                    return redirect(next_url)
                else:
                    return HttpResponseRedirect (reverse('home'))
            else:
                return render(request, 'login.html',
                             {'login_errors':'Invalid email or password','errors':'invalid email or password'})
        else:
            return render(request, 'login.html',{'login_form':login_form})   
        
class PassordResetView(View):
    def get(self, request):
        return render(request, 'forgot_password.html')
    
class ChangePasswordView(View):
    def get(self, request ,*args, **kwargs):
        return render(request, 'change_password.html')
    def post(self, request,*args,**kwargs):
        form = PasswordReset(request.POST)
        if form.is_valid():
           user= authenticate(request,username = request.user.username, 
                         password = form.cleaned_data['old_password'])
           if user is not None:             
              user.set_password(form.cleaned_data['new_password'])
              user.save()
              return redirect(reverse('profile',args=[request.user.username]))  
           else:
               return render(request, 'change_password.html',{'password_error':'Incorrect email','form':form})

        else:
            return render(request, 'change_password.html',{'form':form})            
class EmailConfirmation(View):
    def post(self, request):
        return redirect('login.html')

class LogoutView(View):
    def get(self, request, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('home'))

@method_decorator(login_required,name='dispatch')
class UserProfileView(View):
    def get(self,request, username,*args, **kwargs):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user.id)
            address = Address.objects.filter(user = request.user.id).first()
            return render(request, 'base_user_profile.html',{'profile':profile, 'address':address})    
        else:
            return HttpResponseRedirect(reverse('home'))


@method_decorator(login_required,name='dispatch')
class UserAdressesView(View):
    def get(self,request, username,*args, **kwargs):
        addresses = Address.objects.filter(user=request.user.id)
        profile = Profile.objects.get(user = request.user.id)
        return render(request, 'address.html',{'addresses':addresses,'profile':profile})

    def post(self, request,*args , **kwargs):
        form = ProfileEditForm(request.POST)
        profile = Profile.objects.get(user = request.user.id)
        if form.is_valid():
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.email = form.cleaned_data['email']
            profile.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'username':request.user.username}))
        else:
            return render(request, 'edit_profile.html',{'profile':profile,'form':form}) 
    

@method_decorator(login_required,name='dispatch')
class UserAdressAddView(View):
    def get(self,request, username,*args, **kwargs):
        profile = Profile.objects.get(user = request.user.id)
        return render(request, 'address_edit.html',{'profile':profile, 'add':True})
    def post(self, request,*args , **kwargs):
        form = AddressEditForm(request.POST)
        if form.is_valid():
            address = Address()
            address.user = request.user
            address.full_name = form.cleaned_data['full_name']
            address.county = form.cleaned_data['county']
            address.phone_no = form.cleaned_data['phone_no']
            address.address = form.cleaned_data['address']
            address.save()   
            return HttpResponseRedirect(reverse('addresses', kwargs={'username':request.user.username}))
        else:
            return render(request, 'address_edit.html',{'address':address,'form':form, 'add':True}) 
    


@method_decorator(login_required,name='dispatch')
class UserHistoryView(View):
    def get(self,request, username,*args, **kwargs):
        user = User.objects.get(username=request.user)
        profile = Profile.objects.get(user=user.id)
        return render(request, 'profile.html',{'profile':profile})

@method_decorator(login_required,name='dispatch')
class ProfileEditView(View):
    def get(self,request, username,*args, **kwargs):
        profile = Profile.objects.get(user=request.user.id)
        return render(request, 'edit_profile.html',{'profile':profile})                        

    def post(self, request,*args , **kwargs):
        form = ProfileEditForm(request.POST)
        profile = Profile.objects.get(user = request.user.id)
        if form.is_valid():
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.email = form.cleaned_data['email']
            profile.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'username':request.user.username}))
        else:
            return render(request, 'edit_profile.html',{'profile':profile,'form':form}) 

@method_decorator(login_required,name='dispatch')
class AddressEditView(View):
    def get(self,request,id,*args, **kwargs):
        address = Address.objects.filter(id=id).first()
        profile = Profile.objects.get(user = request.user.id)
        return render(request, 'address_edit.html',{'address':address,'profile':profile})                        
    def post(self, request,id,*args , **kwargs):
        address = Address.objects.get(id=id)
        if request.POST.get('delete'):
            address.delete()
            return HttpResponseRedirect(reverse('addresses', kwargs={'username':request.user.username}))
        form = AddressEditForm(request.POST)
        if form.is_valid():
            address.full_name = form.cleaned_data['full_name']
            address.county = form.cleaned_data['county']
            address.phone_no = form.cleaned_data['phone_no']
            address.address = form.cleaned_data['address']
            address.save()   
            return HttpResponseRedirect(reverse('addresses', kwargs={'username':request.user.username}))
        else:
            return render(request, 'address_edit.html',{'address':address,'form':form}) 
