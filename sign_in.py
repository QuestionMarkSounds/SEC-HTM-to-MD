import streamlit as st
from streamlit_oauth import OAuth2Component
import streamlit.components.v1 as components
import os
import base64
import json
from dotenv import load_dotenv
from streamlit_msal import Msal
from msal import PublicClientApplication
from oauth_button import oauth_button

load_dotenv()

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/dist")


# create an OAuth2Component instance
GOOG_CLIENT_ID = os.environ.get("CLIENT_ID")
GOOG_CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

MSAL_CLIENT_ID = os.getenv("MSAL_CLIENT_ID")
MSAL_CLIENT_SECRET = os.getenv("MSAL_CLIENT_SECRET") or None
MSAL_AUTHORITY = "https://Marksdocenkooutlook.onmicrosoft.com/"+os.getenv("MSAL_TENANT_ID")

GOOG_AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOG_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOG_REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"

auth_data = None
msal_result = None
    
if "auth" not in st.session_state:
    msal_tenant = os.environ.get("MSAL_TENANT_ID")
    msal_oauth2 = OAuth2Component(client_id="7bd5f9ba-68c4-4dcc-ac20-d762f49fb814", authorize_endpoint=f"https://login.microsoftonline.com/{msal_tenant}/oauth2/v2.0/authorize?", token_endpoint=f"https://login.microsoftonline.com/{msal_tenant}/oauth2/v2.0/token?")
    msal_result = oauth_button(msal_oauth2, platform="microsoft", use_container_width=True)
    
    # msal_result = msal_oauth2.authorize_button(
    #     name="2Continue with Microsoft",
    #     icon="https://learn.microsoft.com/en-us/entra/identity-platform/media/howto-add-branding-in-apps/ms-symbollockup_mssymbol_19.png",
    #     redirect_uri="http://localhost:8501",
    #     scope="User.ReadBasic.All",
    #     key="microsoft2",
    #     extras_params={"prompt": "consent", "access_type": "offline"},
    #     use_container_width=True,
    #     pkce='S256',
    # )


    if msal_result:
        id_token = msal_result["token"]["access_token"]
        # verify the signature is an optional step for security
        payload = id_token.split(".")[1]
        # add padding to the payload if needed
        payload += "=" * (-len(payload) % 4)
        payload = json.loads(base64.b64decode(payload))
        # print(payload)
        st.session_state["auth"] = payload["email"]
        st.session_state["user_name"] = payload["name"]
        st.session_state["token"] = msal_result
        st.switch_page("pages/embeddings.py")

    goog_oauth2 = OAuth2Component(GOOG_CLIENT_ID, GOOG_CLIENT_SECRET, GOOG_AUTHORIZE_ENDPOINT, GOOG_TOKEN_ENDPOINT, GOOG_TOKEN_ENDPOINT, GOOG_REVOKE_ENDPOINT)
    goog_result = oauth_button(goog_oauth2, platform="google", use_container_width=True)
    
    # goog_result = goog_oauth2.authorize_button(
    #     name="Continue with Google",
    #     icon="https://www.google.com.tw/favicon.ico",
    #     redirect_uri="http://localhost:8502",
    #     scope="openid email profile",
    #     key="google",
    #     extras_params={"prompt": "consent", "access_type": "offline"},
    #     use_container_width=True,
    #     pkce='S256',
    # )

    if goog_result:
        result = goog_result
        st.write(result)
        # decode the id_token jwt and get the user's email address
        id_token = result["token"]["id_token"]
        # verify the signature is an optional step for security
        payload = id_token.split(".")[1]
        # add padding to the payload if needed
        payload += "=" * (-len(payload) % 4)
        payload = json.loads(base64.b64decode(payload))
        print(payload)
        email = payload["email"]
        st.session_state["auth"] = email
        st.session_state["user_name"] = payload["name"]
        st.session_state["token"] = result["token"]
        
        st.rerun()

else:
    
    # st.write("You are logged in!")
    # st.write(st.session_state["auth"])
    # st.write(st.session_state["token"])
    st.switch_page("pages/embeddings.py")

