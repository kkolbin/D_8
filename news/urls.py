from django.urls import path

from . import views
from .views import (
    NewsListView,
    NewsDetailView,
    SearchView,
    SearchResultView,
    CustomSignupView,
    LoginView,
    NewsCreateView,
    ArticleCreateView,
    NewsUpdateView,
    NewsDeleteView,
    ArticleUpdateView,
    ArticleDeleteView,
    become_author,
    UserUpdateView,
)

app_name = 'news'

urlpatterns = [
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('search/results/', SearchResultView.as_view(), name='search_results'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('become_author/', become_author, name='become_author'),
    path('access_denied/', views.access_denied, name='access_denied'),
    path('profile/update/', UserUpdateView.as_view(), name='profile_update'),
]
