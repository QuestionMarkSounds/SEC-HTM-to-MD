import streamlit as st

from streamlit_supabase_auth import login_form, logout_button
from dotenv import load_dotenv
import os
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

def main():
    st.title("Component Gallery")
    st.header("Login with Supabase Auth")
    session = login_form(url=url,
                         apiKey=key,
                         providers=["azure", "google"]
                        )
    st.write(session)
    if not session:
        return
    st.query_params.page=["success"]
    with st.sidebar:
        st.write(f"Welcome {session['user']['email']}")
        logout_button()


if __name__ == "__main__":
    main()