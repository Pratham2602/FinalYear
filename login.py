import streamlit as st
import SessionState

# Define a dictionary to store the usernames and passwords
users = {
    'superuser': 'superpass',
    'user1': 'pass1',
    'user2': 'pass2',
    'user3': 'pass3'
}

def login():
    """A function to simulate a login page."""
    # Set page title
    st.set_page_config(page_title='Login Page')

    # Define username and password fields
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    # Create a button to submit credentials
    if st.button('Login'):
        # Check if the credentials are valid
        if username in users and password == users[username]:
            st.success('Logged in as {}'.format(username))
            
            # Save the user login state using SessionState
            session_state = SessionState.get(user=username)

            # Check if superuser is logging in
            if username == 'superuser':
                st.write('Add new user:')
                new_user = st.text_input('')
                new_pass = st.text_input('', type='password')
                if st.button('Add user'):
                    # Add the new user to the dictionary
                    users[new_user] = new_pass
                    st.success('User {} added successfully'.format(new_user))

            # Create a button to go to another page
            if st.button('Go to another page'):
                #Redirect the user to another page using _CodeHasher
                #redirect_code = _CodeHasher().to_bytes('redirect')
                #session_state.redirected = True
                pass
                #st.experimental_set_query_params(__code=redirect_code)

            return True
        else:
            st.error('Invalid username or password')
            return False

# Define another page
def another_page():
    st.write('You have been redirected to another page')

# Main function to run the app
def main():
    # Call the login function
    if not login():
        return
    
    # Check if the user has been redirected
    session_state = SessionState.get(user=None, redirected=False)
    if session_state.redirected:
        another_page()
    else:
        st.write('You are on the main page')

if __name__ == '__main__':
    main()
