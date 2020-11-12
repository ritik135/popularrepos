from django.urls import path

from . import views

urlpatterns = [
    path('get-popular-repos/', views.PopularContribCommitListView.as_view(), name='get_contrib_and_commit_list'),
]