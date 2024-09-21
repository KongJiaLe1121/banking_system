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
def create_account():
    st.subheader("Create Account")
    username = st.text_input("Enter a username:")
    password = st.text_input("Create a password:", type='password')
    
    if st.button("Create Account"):
        if username in accounts:
            st.error("Error: Account with this username already exists!")
        elif len(password) < 6:
            st.error("Error: Password must be at least 6 characters long.")
        else:
            accounts[username] = {"password": password, "balance": 0}
            save_accounts(accounts)
            st.success(f"Account created successfully for {username}!")

# Function to log into an account
def login():
    st.subheader("Log In")
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type='password')

    if st.button("Log In"):
        if username not in accounts:
            st.error("Error: Account does not exist.")
            return None
        if password == accounts[username]["password"]:
            st.success(f"Login successful! Welcome, {username}.")
            return username
        else:
            st.error("Error: Incorrect username or password.")
            return None

# Function to deposit money
def deposit(username):
    st.subheader("Deposit Money")
    amount = st.number_input("Enter amount to deposit:", min_value=0.01)
    
    if st.button("Deposit"):
        accounts[username]["balance"] += amount
        save_accounts(accounts)
        st.success(f"Successfully deposited ${amount:.2f}. Current balance: ${accounts[username]['balance']:.2f}")

# Function to withdraw money
def withdraw(username):
    st.subheader("Withdraw Money")
    amount = st.number_input("Enter amount to withdraw:", min_value=0.01)

    if st.button("Withdraw"):
        if amount > accounts[username]["balance"]:
            st.error("Error: Insufficient balance.")
        else:
            accounts[username]["balance"] -= amount
            save_accounts(accounts)
            st.success(f"Successfully withdrew ${amount:.2f}. Current balance: ${accounts[username]['balance']:.2f}")

# Function to check account balance
def check_balance(username):
    st.subheader("Check Balance")
    st.write(f"Current balance: ${accounts[username]['balance']:.2f}")

# Function to transfer money to another account
def transfer(username):
    st.subheader("Transfer Money")
    recipient = st.text_input("Enter the username of the recipient:")
    amount = st.number_input("Enter amount to transfer:", min_value=0.01)

    if st.button("Transfer"):
        if recipient not in accounts:
            st.error("Error: Recipient account does not exist.")
        elif amount > accounts[username]["balance"]:
            st.error("Error: Insufficient balance for transfer.")
        else:
            accounts[username]["balance"] -= amount
            accounts[recipient]["balance"] += amount
            save_accounts(accounts)
            st.success(f"Successfully transferred ${amount:.2f} to {recipient}. Current balance: ${accounts[username]['balance']:.2f}")

# Main function to display the banking system interface
def banking_system():
    st.title("Simple Banking System")
    
    menu_choice = st.sidebar.selectbox("Select an option", ["Create Account", "Log In", "Exit"])
    
    if menu_choice == "Create Account":
        create_account()
    elif menu_choice == "Log In":
        user = login()
        if user:
            sub_menu_choice = st.selectbox("Select an action", ["Deposit Money", "Withdraw Money", "Check Balance", "Transfer Money", "Log Out"])
            if sub_menu_choice == "Deposit Money":
                deposit(user)
            elif sub_menu_choice == "Withdraw Money":
                withdraw(user)
            elif sub_menu_choice == "Check Balance":
                check_balance(user)
            elif sub_menu_choice == "Transfer Money":
                transfer(user)
            elif sub_menu_choice == "Log Out":
                st.info("Logged out.")
    elif menu_choice == "Exit":
        st.info("Exiting system. Goodbye!")

# Run the banking system
if __name__ == "__main__":
    banking_system()
