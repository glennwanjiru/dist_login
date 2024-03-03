import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Firebase Configuration
cred = credentials.Certificate("dist-login-firebase-adminsdk-h4oww-d1a46098a9.json")

if not firebase_admin._apps:
    firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Authentication Functions
def login():
    st.subheader("Login") 
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success("Login successful")
            st.session_state['user_id'] = user['localId']  # Store user ID in session state
        except Exception as e:
            st.error("Invalid credentials or an error occurred")

def create_account():
    st.subheader("Create New Account")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if new_password == confirm_password:
            try:
                user = auth.create_user(email=new_email, password=new_password)
                st.success("Account created successfully. You can now log in.")
                st.session_state['user_id'] = user.uid  # Store user ID in session state
            except Exception as e:
                st.error(f"Error creating account. {e}")
        else:
            st.error("Passwords do not match.")

# Placeholder functions - replace these with your actual implementations
def register_contact():
    st.write("Register Contact")

def search_contact():
    st.write("Search Contact")

def forgot_password():
    st.write("Forgot Password")

# Main App Structure
def main():
    st.title("Contact Management Application")

    if 'user_id' in st.session_state:  # Check if logged in
        st.write("Forgot password?", onclick=forgot_password)  # Placeholder
        register_contact()
        search_contact()
    else:
        choice = st.sidebar.selectbox("Login or Signup", ["Login", "Create Account"])

        if choice == "Login":
            login()
        else:
            create_account()

if __name__ == "__main__":
    main()
