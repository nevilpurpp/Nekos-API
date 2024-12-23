from django.urls import path

from oauth2_provider.views import (
    TokenView,
    RevokeTokenView,
    UserInfoView,
    JwksInfoView,
    IntrospectTokenView,
)

from .views import (
    UserView,
    UserRelationshipsView,
    UserAvatarUploadView,
    AuthorizationWithCaptchaView,
    ConnectDiscoveryInfoView,
    UserAdminViewSet,
)

urlpatterns = [
    path("users", UserView.as_view({"get": "list"}), name="user"),
    path(
        "users/@me",
        UserView.as_view({"get": "retrieve", "patch": "update"}),
        name="user-me",
        kwargs={"pk": "@me"},
    ),
    path(
        "users/@me/avatar",
        UserAvatarUploadView.as_view(),
        name="user-avatar",
    ),
    path(
        "users/<uuid:pk>",
        UserView.as_view({"get": "retrieve", "patch": "update"}),
        name="user-detail",
    ),
    path(
        "users/<uuid:pk>/token",
        UserAdminViewSet.as_view({"get": "create_token"}),
        name="user-create-token",
    ),
    path(
        "users/<uuid:pk>/<related_field>",
        UserView.as_view({"get": "retrieve_related"}),
        name="user-related",
    ),
    path(
        "users/<uuid:pk>/relationships/<related_field>",
        UserRelationshipsView.as_view(),
        name="user-relationships",
    ),
    path("auth/signup", UserView.as_view({"post": "signup"})),
    path("auth/authorize", AuthorizationWithCaptchaView.as_view(), name="authorize"),
    path("auth/token", TokenView.as_view(), name="token"),
    path("auth/introspect", IntrospectTokenView.as_view(), name="introspect"),
    path("auth/token/revoke", RevokeTokenView.as_view(), name="revoke-token"),
    path("auth/userinfo", UserInfoView.as_view(), name="user-info"),
    path("auth/.well-known/jwks-info.json", JwksInfoView.as_view(), name="jwks-info"),
    path(
        "auth/.well-known/openid-configuration",
        ConnectDiscoveryInfoView.as_view(),
        name="oidc-connect-discovery-info",
    ),
]
