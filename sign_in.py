import streamlit as st
from streamlit_google_auth import Authenticate

# ... (set up your credentials and other variables)
secret_credentials_path="./client_secret.json"
cookie_name="GOOG_Auth"
cookie_key="aZ456Jf77"
cookie_expiry_days=7

authenticator = Authenticate(

    secret_credentials_path=secret_credentials_path,
    cookie_name=cookie_name,
    cookie_key=cookie_key,
    cookie_expiry_days=cookie_expiry_days,
    redirect_uri="https://finelem.streamlit.app/"
)

authenticator.login()

if st.session_state['connected']:
    st.image(st.session_state['user_info'].get('picture'))
    st.write('Hello, '+ st.session_state['user_info'].get('name'))
    st.write('Your email is '+ st.session_state['user_info'].get('email'))
    if st.button('Log out'):
        authenticator.logout(cookie_name)