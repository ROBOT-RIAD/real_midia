from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import CreateView,RedirectView
from django.urls import reverse_lazy
from .models import Posts,Like
from .forms import PostForm
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.

class PostCreateView(LoginRequiredMixin,CreateView):
    model =Posts
    form_class =PostForm
    template_name = 'posts/post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class LikeView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Posts, pk=kwargs['id'])
        user = self.request.user
        already_liked = Like.objects.filter(post=post, user=user)
        if not already_liked:
            Like.objects.create(post=post, user=user)
        return reverse_lazy('home')

class UnlikeView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Posts, pk=kwargs['id'])
        user = self.request.user
        Like.objects.filter(post=post, user=user).delete()
        return reverse_lazy('home')


    


    

    
