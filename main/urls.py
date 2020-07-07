from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_home_page),
    path("register", views.show_register_page),
    path("signin", views.show_signin_page),
    path("register/user", views.register_user),
    path("signin/user", views.signin_user),
    path("dashboard", views.show_dashboard),
    path("dashboard/admin", views.show_admin_dashboard),
    path("logout", views.logout),
    path("users/new", views.show_add_user_page),
    path("users/new/add", views.add_user),
    path("users/show/<int:user_id>", views.show_user),
    path("dashboard_selector", views.select_dashboard),
    path("users/<int:user_id>/edit", views.edit_user),
    path("update_user/<int:user_id>", views.update_user),
    path("users/<int:user_id>/delete", views.delete_user),
    path("post_message/<int:user_id>", views.post_message),
    path("post_comment/<int:user_id>", views.post_comment),
    path("update_password/<int:user_id>", views.update_password),
]