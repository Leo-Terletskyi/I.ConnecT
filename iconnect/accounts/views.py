from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import get_user_model
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views import generic

from posts.forms import PostCreateForm, PostUpdateForm
from posts.models import Post
from .forms import LoginForm, UserRegisterForm, UserUpdateForm, UserPasswordChangeForm

User = get_user_model()


class UserRegisterView(generic.CreateView):
    template_name = 'accounts/auth/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('sign_in')


class LoginView(generic.FormView):
    template_name = 'accounts/auth/login.html'
    form_class = LoginForm
    
    def form_valid(self, form):
        data = form.cleaned_data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect('user_acc', pk=user.id)
            else:
                return HttpResponse('Your account is not active')
        return HttpResponse(f'User with username <h1>{username}</h1> does not exists')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('sign_in')


class UserAccDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'accounts/user_acc.html'
    model = User
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super(UserAccDetailView, self).get_context_data()
        context['current_user_posts'] = Post.objects.filter(author_id=self.kwargs.get('pk'), is_archive=False)
        context['post_create_form'] = PostCreateForm()
        return context


class UpdateUserProfileView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_profile_settings.html'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy("user_acc", kwargs={'pk': self.request.user.id})


class UserPostsListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'posts/post_archive.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user, is_archive=True)


class UsersSearchListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'accounts/users_search.html'
    context_object_name = 'users_search'
    
    def get_queryset(self):
        search_text = self.request.GET.get('query')
        if not search_text:
            return self.model.objects.filter(is_active=True)
        q = self.model.objects.filter(
            Q(first_name__icontains=search_text) |
            Q(last_name__icontains=search_text) |
            Q(username__icontains=search_text)
        )
        return q


class FollowUser(LoginRequiredMixin, generic.View):
    def get(self, request, user_pk):
        from_user = request.user
        to_user = get_object_or_404(User, pk=user_pk)
        if from_user not in to_user.followers.all():
            messages.add_message(request, messages.SUCCESS, message=f'you have successfully subscribed ({to_user})')
            to_user.followers.add(from_user)
        previous_page = request.META.get('HTTP_REFERER')
        return redirect(previous_page)


class UnfollowUser(LoginRequiredMixin, generic.View):
    def get(self, request, user_pk):
        from_user = request.user
        to_user = get_object_or_404(User, pk=user_pk)
        if from_user in to_user.followers.all():
            messages.add_message(request, messages.SUCCESS, message=f'you have successfully unsubscribed ({to_user})')
            to_user.followers.remove(from_user)
        previous_page = request.META.get('HTTP_REFERER')
        return redirect(previous_page)


class FollowingListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'accounts/following.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        user = get_object_or_404(User, id=user_pk)
        return user.following.all()


class FollowersListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'accounts/followers.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        user = get_object_or_404(User, id=user_pk)
        return user.followers.all()
