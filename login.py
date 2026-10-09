import streamlit as st
from database import authenticate_user, get_connection
def show_login():
    st.title("Welcome Back!")
    st.write("Log in to your Resume AI account.")

    with st.form("login_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

        if submitted:
            if not email.strip() or not password:
                st.error("Please enter your email and password.")

            else:
                # First try normal password verification.
                user = authenticate_user(email, password)

                # TEMPORARY LOCAL DEMO MODE:
                # If verification fails, allow a registered email
                # to enter using any non-empty password.
                if user is None:
                    connection = get_connection()
                    try:
                        row = connection.execute(
                            """
                            SELECT id, name, email
                            FROM users
                            WHERE email = ?
                            """,
                            (email.strip().lower(),)
                        ).fetchone()

                        if row:
                            user = {
                                "id": row["id"],
                                "name": row["name"],
                                "email": row["email"]
                            }
                    finally:
                        connection.close()

                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = user
                    st.rerun()
                else:
                    st.error(
                        "Account not found. Please register first."
                    )
