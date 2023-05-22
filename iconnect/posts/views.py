from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import PostCreateForm, PostUpdateForm
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
    

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'posts/post_update_form.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs.get('post_pk'), author=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('user_acc', kwargs={'pk': self.request.user.id})


def post_archiving(request, pk):
    post = get_object_or_404(Post, id=pk, author_id=request.user.id)
    if not post.is_archive:
        post.is_archive = True
        post.save()
        return redirect('user_acc', pk=request.user.id)
    post.is_archive = False
    post.save()
    return redirect('post_archive', pk=request.user.id)


def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user.id == post.author.id:
        post.delete()
    return redirect('user_acc', pk=request.user.id)
