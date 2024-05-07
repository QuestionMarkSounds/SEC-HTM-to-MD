from streamlit_oauth import OAuth2Component

def oauth_button(oauth2component, redirect_uri, platform="google", use_container_width=True):
    if platform == "google":
        return oauth2component.authorize_button(
            name="Continue with Google",
            icon="https://www.google.com.tw/favicon.ico",
            redirect_uri=redirect_uri,
            scope="openid email profile",
            key="google",
            extras_params={"prompt": "consent", "access_type": "offline"},
            use_container_width=use_container_width,
            pkce='S256',
        )
    elif platform == "microsoft":
        return oauth2component.authorize_button(
            name="Continue with Microsoft",
            icon="https://learn.microsoft.com/en-us/entra/identity-platform/media/howto-add-branding-in-apps/ms-symbollockup_mssymbol_19.png",
            redirect_uri=redirect_uri,
            scope="User.ReadBasic.All",
            key="microsof2",
            extras_params={"prompt": "consent", "access_type": "offline"},
            use_container_width=use_container_width,
            pkce='S256',
        )
    else:
        raise ValueError(f"Platform {platform} is not supported")