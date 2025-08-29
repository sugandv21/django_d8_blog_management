from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Post


def home(request):
    return render(request, "blog/layout/home.html")


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/layout/user_posts.html" 
    context_object_name = "posts"
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')


class PostListView(ListView):
    model = Post
    template_name = "blog/layout/post_list.html"
    context_object_name = "posts"
    ordering = ['-created_at']


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/layout/post_detail.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/layout/post_form.html"
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully! 🎉")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/layout/post_form.html"
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post updated successfully! ✏️")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/layout/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created. Please log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "blog/layout/signup.html", {"form": form})
