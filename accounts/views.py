from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import FormView,UpdateView,TemplateView, DetailView,ListView,RedirectView,RedirectView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from .forms import UserSignupForm,EditeProfileForm
from django.contrib import messages
from accounts.models import UserProfile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from accounts.models import Follow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.


class UserSignupView(FormView):
    template_name ='accounts/signup.html'
    form_class = UserSignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user=form.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link =f"http://127.0.0.1:8000/accounts/active/{uid}/{token}"
        email_subject = "Confirm your Email"
        email_body =render_to_string('accounts/confirm_email.html',{'confirm_link':confirm_link})
        email = EmailMultiAlternatives(email_subject,"",to =[user.email])
        email.attach_alternative(email_body,'text/html')
        email.send()
        messages.success(self.request, 'account create Successfully')
        return super().form_valid(form)
    

def Activate(request,uid64,token):
    try:
        uid =urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user =None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self,form):
        messages.success(self.request,"Login successfully")
        return super().form_valid(form)
    

class EditProfileView(LoginRequiredMixin,UpdateView):
    model = UserProfile
    form_class = EditeProfileForm
    template_name = 'accounts/edite_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        user = self.request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile
    

class ProfileView(LoginRequiredMixin,DetailView):
    model = UserProfile
    template_name = "accounts/profile.html"
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        user = self.request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile
    

class LogoutView(RedirectView):
    url = reverse_lazy('login')
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class UserProfileView(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'accounts/user_profile.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        context['is_following'] = user_profile.account.is_followed_by(self.request.user)
        return context


class FollowView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        following_user = get_object_or_404(User, pk=kwargs['id'])
        follower_user = self.request.user
        already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
        if not already_followed:
            Follow.objects.create(follower=follower_user, following=following_user)
        return reverse_lazy('user_profile', kwargs={'pk': kwargs['id']})

class UnFollowView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        following_user = get_object_or_404(User, pk=kwargs['id'])
        follower_user = self.request.user
        Follow.objects.filter(follower=follower_user, following=following_user).delete()
        return reverse_lazy('user_profile', kwargs={'pk': kwargs['id']})


    


    
    



