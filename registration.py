
import streamlit as st
from database import register_user


def show_registration():
    st.title("Create Your Account")

    with st.form("registration_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input(
            "Password (minimum 8 characters)",
            type="password"
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button("Create Account")

        if submitted:
            if password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = register_user(
                    name, email, password
                )

                if success:
                    st.success(message)
                    st.info("You can now go to the Login page.")
                else:
                    st.error(message)
