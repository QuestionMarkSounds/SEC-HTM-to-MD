import streamlit as st
from streamlit_oauth import OAuth2Component
import streamlit.components.v1 as components
import os
import base64
import json
from dotenv import load_dotenv
from streamlit_msal import Msal
from oauth_button import oauth_button
from PIL import Image

load_dotenv()
logo = Image.open("fintel2.png")
img = Image.open("my-image.png")

import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/dist")

# create an OAuth2Component instance
GOOG_CLIENT_ID = os.environ.get("CLIENT_ID")
GOOG_CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

MSAL_CLIENT_ID = os.environ.get("MSAL_CLIENT_ID")
MSAL_CLIENT_SECRET = os.environ.get("MSAL2_CLIENT_SECRET") or None
MSAL_AUTHORITY = "https://Marksdocenkooutlook.onmicrosoft.com/"+os.getenv("MSAL_TENANT_ID")

GOOG_AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOG_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOG_REVOKE_ENDPOINT = "https://oauth2.googleapis.com/revoke"

auth_data = None
msal_result = None

st.set_page_config(page_title="FINTEL", page_icon=logo)
import urllib.parse
session = st.runtime.get_instance()._session_mgr.list_active_sessions()[0]
st_base_url = urllib.parse.urlunparse([session.client.request.protocol, session.client.request.host, "", "", "", ""])
print(st_base_url)
if "streamlit.app" in st_base_url:
    st_base_url.replace("http://", "https://")

left_co, cent_co,last_co = st.columns([0.4,0.2,0.4])
with cent_co:
    st.image(logo)
st.markdown("")
st.markdown("")
st.markdown("")

st.session_state["logo"] = logo

if "auth" not in st.session_state:
    msal_tenant = os.environ.get("MSAL_TENANT_ID")
    msal_oauth2 = OAuth2Component(client_id=MSAL_CLIENT_ID, client_secret=MSAL_CLIENT_SECRET, authorize_endpoint=f"https://login.microsoftonline.com/{msal_tenant}/oauth2/v2.0/authorize?", token_endpoint=f"https://login.microsoftonline.com/{msal_tenant}/oauth2/v2.0/token?")
    msal_result = oauth_button(msal_oauth2, redirect_uri=st_base_url, platform="microsoft", use_container_width=True, )

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
    goog_result = oauth_button(goog_oauth2, redirect_uri=st_base_url, platform="google", use_container_width=True)

    if goog_result:
        result = goog_result
        # st.write(result)
        # decode the id_token jwt and get the user's email address
        id_token = result["token"]["id_token"]
        # verify the signature is an optional step for security
        payload = id_token.split(".")[1]
        # add padding to the payload if needed
        payload += "=" * (-len(payload) % 4)
        payload = json.loads(base64.b64decode(payload))
        # print(payload)
        email = payload["email"]
        st.session_state["auth"] = email
        st.session_state["user_name"] = payload["name"]
        st.session_state["token"] = result["token"]
        
        st.rerun()

else:
    
    st.switch_page("pages/embeddings.py")

