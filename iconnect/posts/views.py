from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import PostCreateForm, PostUpdateForm, PostCommentForm
from .models import Post, PostComment


User = get_user_model()


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


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user.id == post.author.id:
        post.delete()
    return redirect('user_acc', pk=request.user.id)


class FollowingPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'posts/following_posts.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.filter(author__in=self.request.user.following.all(), is_archive=False)
    
    def get_context_data(self, **kwargs):
        context = super(FollowingPostListView, self).get_context_data()
        context['post_comment_form'] = PostCommentForm()
        return context


@login_required
def like_post(request, post_pk):
    post = get_object_or_404(Post, id=post_pk)
    user = request.user
    all_likes = post.likes.all()
    if user not in all_likes:
        post.likes.add(user)
        post.save()
    else:
        post.likes.remove(user)
        post.save()
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)


class PostCommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = PostComment
    form_class = PostCommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        post_id = self.kwargs.get('post_id')
        comment.post = get_object_or_404(Post, id=post_id)
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        previous_page = self.request.META.get('HTTP_REFERER')
        if previous_page.endswith('/posts/feed/'):
            return reverse_lazy('feed')
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        post_author_id = post.author.id
        return reverse_lazy('user_acc', kwargs={'pk': post_author_id})


@login_required
def delete_post_comment(request, pk):
    comment = get_object_or_404(PostComment, id=pk)
    if request.user.id == comment.author.id:
        comment.delete()
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)