from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.views import SignupView
from django.contrib.auth.decorators import login_required
from .models import Post, Group
from .forms import PostForm
from django.contrib.auth.views import LoginView as AuthLoginView
from django.core.paginator import Paginator
from django.contrib.auth.models import User


class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(post_type__in=['news', 'article'])  # Отфильтровать и новости и статьи

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context['paginator']
        current_page = self.request.GET.get('page', 1)
        news = paginator.get_page(current_page)

        start_range = max(news.number - 5, 1)
        end_range = min(news.number + 4, paginator.num_pages)

        context['news'] = news
        context['paginator'] = paginator
        context['start_range'] = start_range
        context['end_range'] = end_range
        context['current_page'] = news.number
        context['news_count'] = Post.objects.filter(post_type='news').count()
        context['article_count'] = Post.objects.filter(post_type='article').count()
        context['is_common_user'] = not self.request.user.groups.filter(name='authors').exists()
        return context



class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'


class SearchView(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        return Post.objects.all()


class SearchResultView(ListView):
    model = Post
    template_name = 'news/search_results.html'
    context_object_name = 'search_results'
    paginate_by = 10

    def get_queryset(self):
        query_title = self.request.GET.get('title')
        query_author = self.request.GET.get('author')
        query_date = self.request.GET.get('date')

        queryset = Post.objects.all()

        if query_title:
            queryset = queryset.filter(title__icontains=query_title)

        if query_author:
            queryset = queryset.filter(author__username__icontains=query_author)

        if query_date:
            queryset = queryset.filter(created_at__gte=query_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_results = context['search_results']

        paginator = Paginator(search_results, self.paginate_by)
        current_page = self.request.GET.get('page', 1)
        search_results = paginator.get_page(current_page)

        start_range = max(search_results.number - 5, 1)
        end_range = min(search_results.number + 4, paginator.num_pages)

        context['search_results'] = search_results
        context['paginator'] = paginator
        context['start_range'] = start_range
        context['end_range'] = end_range
        context['current_page'] = search_results.number

        return context


class CustomSignupView(SignupView):
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account_login')


class LoginView(AuthLoginView):
    template_name = 'account/login.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'user_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class NewsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    template_name = 'news/news_create.html'
    form_class = PostForm
    success_url = reverse_lazy('news:news_list')

    def form_valid(self, form):
        print(form.instance.post_type)
        form.instance.author = self.request.user
        form.instance.post_type = 'news'
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()


class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    template_name = 'news/article_create.html'
    form_class = PostForm
    success_url = reverse_lazy('news:news_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = 'article'
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()


class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'news/news_edit.html'
    form_class = PostForm
    context_object_name = 'news'
    success_url = reverse_lazy('news:news_list')

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()


class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('news:news_list')

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'news/article_edit.html'
    form_class = PostForm
    context_object_name = 'news'
    success_url = reverse_lazy('news:news_list')

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('news:news_list')

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()


@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    user.groups.add(author_group)
    return redirect('news:news_list')


def access_denied(request):
    return render(request, 'news/access_denied.html')
