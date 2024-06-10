from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from posts.models import Posts,Like
from django.contrib.auth.mixins import LoginRequiredMixin



class HomeView(ListView):
    template_name = 'cores/index.html'

    def get_queryset(self):
        username = self.request.GET.get('username', " ")
        return User.objects.filter(username__icontains=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Posts.objects.all()
        context['users'] = self.object_list
        context['posts'] = posts
        context['username'] = self.request.GET.get('username', " ")
        return context
    

# class HomeView(ListView):
#     model = Posts
#     template_name = 'cores/index.html'
#     context_object_name = 'posts'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['liked_posts'] = Like.objects.filter(post__in=context['posts'], user=self.request.user)
#         return context


