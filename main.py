import json
import os
import streamlit as st

# Path to the JSON file acting as a local database
DATABASE_FILE = 'accounts.json'

# Function to load account data from the JSON file
def load_accounts():
    if not os.path.exists(DATABASE_FILE):
        return {}
    
    with open(DATABASE_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            st.error("Error: Database file is corrupted.")
            return {}

# Function to save account data to the JSON file
def save_accounts(accounts):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(accounts, file, indent=4)

# Load accounts at the start of the program
accounts = load_accounts()

# Function to create an account
def create_account(username, password):
    if username in accounts:
        st.error("Error: Account with this username already exists!")
        return
    
    if len(password) < 6:
        st.error("Error: Password must be at least 6 characters long.")
        return

    accounts[username] = {"password": password, "balance": 0}
    save_accounts(accounts)
    st.success(f"Account created successfully for {username}!")

# Function to log into an account
def login(username, password):
    if username not in accounts:
        st.error("Error: Account does not exist.")
        return None
    
    if password == accounts[username]["password"]:
        st.success(f"Login successful! Welcome, {username}.")
        return username
    else:
        st.error("Error: Incorrect password.")
        return None

# Function to deposit money
def deposit(username, amount):
    if amount <= 0:
        st.error("Error: Deposit amount must be positive.")
        return
    accounts[username]["balance"] += amount
    save_accounts(accounts)
    st.success(f"Successfully deposited ${amount:.2f}. Current balance: ${accounts[username]['balance']:.2f}")

# Function to withdraw money
def withdraw(username, amount):
    if amount <= 0:
        st.error("Error: Withdrawal amount must be positive.")
        return
    if amount > accounts[username]["balance"]:
        st.error("Error: Insufficient balance.")
        return
    accounts[username]["balance"] -= amount
    save_accounts(accounts)
    st.success(f"Successfully withdrew ${amount:.2f}. Current balance: ${accounts[username]['balance']:.2f}")

# Function to check account balance
def check_balance(username):
    st.info(f"Current balance: ${accounts[username]['balance']:.2f}")

# Function to transfer money to another account
def transfer(username, recipient, amount):
    if recipient not in accounts:
        st.error("Error: Recipient account does not exist.")
        return
    if amount <= 0:
        st.error("Error: Transfer amount must be positive.")
        return
    if amount > accounts[username]["balance"]:
        st.error("Error: Insufficient balance for transfer.")
        return
    accounts[username]["balance"] -= amount
    accounts[recipient]["balance"] += amount
    save_accounts(accounts)
    st.success(f"Successfully transferred ${amount:.2f} to {recipient}. Current balance: ${accounts[username]['balance']:.2f}")

# Streamlit app interface
st.title("Simple Banking System")

# Create account section
if st.sidebar.button("Create Account"):
    st.sidebar.subheader("Create a new account")
    new_username = st.sidebar.text_input("Enter a username")
    new_password = st.sidebar.text_input("Create a password", type="password")
    if st.sidebar.button("Submit"):
        create_account(new_username, new_password)

# Log in section
if 'logged_in_user' not in st.session_state:
    st.sidebar.subheader("Log in")
    username = st.sidebar.text_input("Enter your username")
    password = st.sidebar.text_input("Enter your password", type="password")
    if st.sidebar.button("Log In"):
        logged_in_user = login(username, password)
        if logged_in_user:
            st.session_state.logged_in_user = logged_in_user

# Banking menu after login
if 'logged_in_user' in st.session_state:
    st.subheader(f"Welcome, {st.session_state.logged_in_user}")

    action = st.selectbox("Choose an action", ["Deposit Money", "Withdraw Money", "Check Balance", "Transfer Money", "Log Out"])

    if action == "Deposit Money":
        deposit_amount = st.number_input("Enter amount to deposit", min_value=0.0, step=1.0)
        if st.button("Deposit"):
            deposit(st.session_state.logged_in_user, deposit_amount)
    
    elif action == "Withdraw Money":
        withdraw_amount = st.number_input("Enter amount to withdraw", min_value=0.0, step=1.0)
        if st.button("Withdraw"):
            withdraw(st.session_state.logged_in_user, withdraw_amount)
    
    elif action == "Check Balance":
        check_balance(st.session_state.logged_in_user)
    
    elif action == "Transfer Money":
        recipient = st.text_input("Enter the recipient's username")
        transfer_amount = st.number_input("Enter amount to transfer", min_value=0.0, step=1.0)
        if st.button("Transfer"):
            transfer(st.session_state.logged_in_user, recipient, transfer_amount)

    elif action == "Log Out":
        st.session_state.pop('logged_in_user')
        st.success("Logged out successfully.")
