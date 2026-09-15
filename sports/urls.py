from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register_user, name="register"),

    path("login/", views.login_user, name="login"),

    path("logout/", views.logout_user, name="logout"),

    path("events/", views.events, name="events"),

    path(
        "events/<int:event_id>/",
        views.event_detail,
        name="event_detail"
    ),

    path(
        "register-event/<int:event_id>/",
        views.register_event,
        name="register_event"
    ),

    path("dashboard/", views.dashboard, name="dashboard"),
]