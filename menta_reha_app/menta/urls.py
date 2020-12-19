from django.urls import path

from . import views
app_name = 'menta'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('menta-list', views.MentaListView.as_view(), name="menta_list"),
    path('menta-detail/<int:pk>/', views.MentaDetailView.as_view(), name="menta_detail"),
    # URLの逆引き：menta_list.htmlから、urlタグを使い、detail pageに遷移するリンクを生成しているが、それは、「mentaテーブルの主キーを引数に、このurls.pyを使ってURLを生成している」という仕組み
    path('menta-create', views.MentaCreateView.as_view(), name="menta_create"),
    path('menta-update/<int:pk>/', views.MentaUpdateView.as_view(), name="menta_update"),
    path('menta-delete/<int:pk>/', views.MentaDeleteView.as_view(), name="menta_delete"),
]
