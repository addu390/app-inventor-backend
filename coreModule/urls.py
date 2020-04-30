from django.urls import path

from .apiviews import ApplicationDetail, UserDetail, ApplicationList, ComponentDetail

urlpatterns = [
    path('application/<str:user_id>/<str:app_id>', ApplicationDetail.as_view(), name="app_builder_details"),
    path('application/<str:user_id>', ApplicationList.as_view(), name="app_builder_create"),
    path('application/<str:user_id>/<str:app_id>/<str:component_id>', ComponentDetail.as_view(), name="app_builder_create"),
    path('user/<str:user_id>', UserDetail.as_view(), name="user_create"),
]