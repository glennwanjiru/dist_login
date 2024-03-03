import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, db

# Initialize Firebase Admin SDK
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")  # Replace with your service account key
firebase_admin.initialize_app(cred, {'databaseURL': 'https://your-firebase-project.firebaseio.com'})

# Streamlit app for contact management
def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success("Login successful!")
            return user['idToken']
        except Exception as e:
            st.error(f"Login failed: {e}")

def reset_password():
    st.subheader("Forgot Password")
    email = st.text_input("Enter your email")
    reset_button = st.button("Send Reset Password Email")

    if reset_button:
        try:
            auth.send_password_reset_email(email)
            st.success("Reset password email sent. Check your inbox.")
        except Exception as e:
            st.error(f"Failed to send reset password email: {e}")

def save_contact_details(token, mobile_number, email, address, registration_number):
    uid = auth.verify_id_token(token)['uid']
    ref = db.reference(f'/contacts/{uid}')  # Adjust the path to your database structure
    ref.set({
        'mobile_number': mobile_number,
        'email': email,
        'address': address,
        'registration_number': registration_number
    })

def search_contact(registration_number):
    ref = db.reference('/contacts')  # Adjust the path to your database structure
    contact_data = ref.order_by_child('registration_number').equal_to(registration_number).get()

    if contact_data:
        contact = next(iter(contact_data.values()))
        st.write(f"Mobile Number: {contact.get('mobile_number')}")
        st.write(f"Email: {contact.get('email')}")
        st.write(f"Address: {contact.get('address')}")
        st.write(f"Registration Number: {contact.get('registration_number')}")
    else:
        st.warning("Contact not found.")
        

# Streamlit UI
st.title("Contact Management App")

# User Authentication
token = login()  # Use the token for authenticated requests

# Password Reset
reset_password()

# Contact Details Form
st.subheader("Enter Contact Details")
mobile_number = st.text_input("Mobile Number")
email = st.text_input("Email")
address = st.text_input("Address")
registration_number = st.text_input("Registration Number")
save_button = st.button("Save Contact Details")

if save_button:
    save_contact_details(token, mobile_number, email, address, registration_number)

# Search Contact
st.subheader("Search Contact")
search_registration_number = st.text_input("Enter Registration Number:")
search_button = st.button("Search Contact")

if search_button:
    search_contact(search_registration_number)
