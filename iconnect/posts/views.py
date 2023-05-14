from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import PostCreateForm
from .models import Post


class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'accounts/user_acc.html'
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('user_acc', kwargs={'pk': self.request.user.id})
    
    