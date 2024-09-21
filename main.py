import streamlit as st

# Function to initialize account data in session state if not already present
def init_session_state():
    if 'accounts' not in st.session_state:
        st.session_state['accounts'] = {}  # Simulate an empty account database
    if 'logged_in_user' not in st.session_state:
        st.session_state['logged_in_user'] = None  # Keep track of the logged-in user

# Function to create an account
def create_account(username, password):
    if username in st.session_state['accounts']:
        st.error("Error: Account with this username already exists!")
        return
    
    if len(password) < 6:
        st.error("Error: Password must be at least 6 characters long.")
        return

    # Create a new account with initial balance 0
    st.session_state['accounts'][username] = {"password": password, "balance": 0}
    st.success(f"Account created successfully for {username}!")

# Function to log into an account
def login(username, password):
    if username not in st.session_state['accounts']:
        st.error("Error: Account does not exist.")
        return None
    
    if password == st.session_state['accounts'][username]["password"]:
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
    st.session_state['accounts'][username]["balance"] += amount
    st.success(f"Successfully deposited ${amount:.2f}. Current balance: ${st.session_state['accounts'][username]['balance']:.2f}")

# Function to withdraw money
def withdraw(username, amount):
    if amount <= 0:
        st.error("Error: Withdrawal amount must be positive.")
        return
    if amount > st.session_state['accounts'][username]["balance"]:
        st.error("Error: Insufficient balance.")
        return
    st.session_state['accounts'][username]["balance"] -= amount
    st.success(f"Successfully withdrew ${amount:.2f}. Current balance: ${st.session_state['accounts'][username]['balance']:.2f}")

# Function to check account balance
def check_balance(username):
    st.info(f"Current balance: ${st.session_state['accounts'][username]['balance']:.2f}")

# Function to transfer money to another account
def transfer(username, recipient, amount):
    if recipient not in st.session_state['accounts']:
        st.error("Error: Recipient account does not exist.")
        return
    if amount <= 0:
        st.error("Error: Transfer amount must be positive.")
        return
    if amount > st.session_state['accounts'][username]["balance"]:
        st.error("Error: Insufficient balance for transfer.")
        return
    st.session_state['accounts'][username]["balance"] -= amount
    st.session_state['accounts'][recipient]["balance"] += amount
    st.success(f"Successfully transferred ${amount:.2f} to {recipient}. Current balance: ${st.session_state['accounts'][username]['balance']:.2f}")

# Streamlit app interface
st.title("Simple Banking System")

# Initialize session state if not already initialized
init_session_state()

# Create account section
if st.sidebar.button("Create Account"):
    st.sidebar.subheader("Create a new account")
    new_username = st.sidebar.text_input("Enter a username")
    new_password = st.sidebar.text_input("Create a password", type="password")
    if st.sidebar.button("Submit"):
        create_account(new_username, new_password)

# Log in section
if not st.session_state['logged_in_user']:
    st.sidebar.subheader("Log in")
    username = st.sidebar.text_input("Enter your username")
    password = st.sidebar.text_input("Enter your password", type="password")
    if st.sidebar.button("Log In"):
        logged_in_user = login(username, password)
        if logged_in_user:
            st.session_state['logged_in_user'] = logged_in_user

# Banking menu after login
if st.session_state['logged_in_user']:
    st.subheader(f"Welcome, {st.session_state['logged_in_user']}")

    action = st.selectbox("Choose an action", ["Deposit Money", "Withdraw Money", "Check Balance", "Transfer Money", "Log Out"])

    if action == "Deposit Money":
        deposit_amount = st.number_input("Enter amount to deposit", min_value=0.0, step=1.0)
        if st.button("Deposit"):
            deposit(st.session_state['logged_in_user'], deposit_amount)
    
    elif action == "Withdraw Money":
        withdraw_amount = st.number_input("Enter amount to withdraw", min_value=0.0, step=1.0)
        if st.button("Withdraw"):
            withdraw(st.session_state['logged_in_user'], withdraw_amount)
    
    elif action == "Check Balance":
        check_balance(st.session_state['logged_in_user'])
    
    elif action == "Transfer Money":
        recipient = st.text_input("Enter the recipient's username")
        transfer_amount = st.number_input("Enter amount to transfer", min_value=0.0, step=1.0)
        if st.button("Transfer"):
            transfer(st.session_state['logged_in_user'], recipient, transfer_amount)

    elif action == "Log Out":
        st.session_state['logged_in_user'] = None
        st.success("Logged out successfully.")
