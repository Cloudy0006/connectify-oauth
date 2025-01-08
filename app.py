import streamlit as st
import base64
import threading
import time

# Add this class after the existing imports


    # Rest of the existing code remains the same


# Set page configuration
st.set_page_config(
    page_title="Connectify",
    page_icon=":globe_with_meridians:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #E6F2F0 !important;
    }
    .title {
        font-family: 'Georgia', serif;
        background: linear-gradient(45deg, #1A5F7A, #159895, #57C5B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 90px;
        font-weight: bold;
        margin-top: 50px;
    }
    .subtitle {
        font-family: 'Arial', sans-serif;
        color: #2C3E50;
        text-align: center;
        font-size: 38px;
        margin-top: 10px;
        animation: colorRotate 5s linear infinite;
    }
    @keyframes colorRotate {
        0% { color: #1A5F7A; }
        25% { color: #159895; }
        50% { color: #57C5B6; }
        75% { color: #2C3E50; }
        100% { color: #1A5F7A; }
    }
    .explore-btn {
        display: block;
        background: linear-gradient(45deg, #1A5F7A, #159895, #57C5B6);
        background-size: 200% auto;
        color: white !important;
        text-align: center;
        padding: 25px 60px;
        margin: 50px auto;
        border-radius: 60px;
        font-size: 36px;
        width: 500px;
        cursor: pointer;
        transition: all 0.5s ease;
        box-shadow: 0 15px 25px rgba(0,0,0,0.2);
        border: none;
        outline: none;
        animation: gradientAnimation 3s ease infinite;
    }
    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .explore-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 20px 35px rgba(0,0,0,0.3);
    }
    .credential-guide {
        background-color: #F0F4F8;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

class SubtitleManager:
    def __init__(self, subtitles):
        self.subtitles = subtitles
        self.current_index = 0
        self.placeholder = st.empty()

    def display_subtitle(self):
        subtitle = self.subtitles[self.current_index]
        self.placeholder.markdown(f'<div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)
        self.current_index = (self.current_index + 1) % len(self.subtitles)

class OAuthCredentialsGuide:
    @staticmethod
    def display_credentials_guide():
        st.markdown('<div class="credential-guide">', unsafe_allow_html=True)
        
        st.markdown("## 🔐 Instagram OAuth Credentials Guide")
        
        # Credential Acquisition Steps
        st.markdown("### How to Obtain Instagram OAuth Credentials")
        
        steps = [
            "1. Visit [Facebook Developers Portal](https://developers.facebook.com/)",
            "2. Create/Log in to a Facebook Developer Account",
            "3. Click 'Create App' in the dashboard",
            "4. Select 'Business' or 'Consumer' app type",
            "5. Configure Instagram Basic Display",
            "6. Navigate to App Settings > Basic"
        ]
        
        for step in steps:
            st.markdown(step)
        
        # Detailed Credential Information
        st.markdown("### Credential Details")
        
        credential_details = {
            "Client ID": "Unique identifier for your Instagram app",
            "Client Secret": "Confidential key for authentication",
            "Redirect URI": "Authorized callback URL after authentication"
        }
        
        for key, description in credential_details.items():
            st.markdown(f"- **{key}**: {description}")
        
        # Warning and Best Practices
        st.warning(""" 
        ⚠️ Important Security Notes:
        - Keep Client Secret confidential
        - Use secure, HTTPS redirect URIs
        - Regularly rotate credentials
        """)
        
        # Additional Resources
        st.markdown("### Additional Resources")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.link_button("Instagram API Docs", "https://developers.facebook.com/docs/instagram-api/")
        
        with col2:
            st.link_button("OAuth Guide", "https://oauth.net/2/")
        
        with col3:
            st.link_button("Facebook Developers", "https://developers.facebook.com/")
        
        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def credentials_form():
        with st.form("instagram_oauth_credentials"):
            st.header("Instagram OAuth Credentials")
            
            # Credential Input Fields
            client_id = st.text_input("Client ID", 
                help="Your Instagram App's unique Client ID")
            client_secret = st.text_input("Client Secret", 
                type="password", 
                help="Confidential key for authentication")
            redirect_uri = st.text_input("Redirect URI", 
                help="Authorized callback URL")
            
            # Submit Button
            submit_button = st.form_submit_button("Generate Authorization URL")
            
            # Validation and URL Generation
            if submit_button:
                if all([client_id, client_secret, redirect_uri]):
                    # Generate Authorization URL
                    base_url = "https://api.instagram.com/oauth/authorize"
                    auth_url = f"{base_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope=user_profile,user_media&response_type=code"
                    
                    st.success("Authorization URL Generated!")
                    st.markdown(f"[Click to Authenticate]({auth_url})")
                else:
                    st.error("Please fill in all credential fields")

# Function to get base64 encoded logo
def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

# Logo display function
def display_logo(logo_path):
    logo_base64 = get_base64_of_image(logo_path)
    if logo_base64:
        st.markdown(f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_base64}" width="100">
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Logo not found")

def main():
    # Subtitles for Connectify
    subtitles = [
        "....Connecting the World, One Degree at a Time",
        "....Uncover Hidden Connections",
        "....Your Network, Your Opportunity",
        "....Six Degrees of Infinite Possibilities"
    ]

    # Initialize session state for page navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'

    # Welcome Screen
    if st.session_state.page == 'welcome':
        # Title
        st.markdown('<div class="title">Welcome to Connectify</div>', unsafe_allow_html=True)

        # Display Logo (Add the logo path here)
        logo_path = r"C:\Users\prajesh\OneDrive - Findability Sciences\Desktop\connetify.png"  # Update this with the actual path
        display_logo(logo_path)

        # Subtitle Management
        subtitle_manager = SubtitleManager(subtitles)
        subtitle_manager.display_subtitle()

        # Explore Now Button
        col1, col2, col3 = st.columns([2,3,2])
        with col2:
            if st.button("Explore Now →", key="explore_btn", use_container_width=True):
                st.session_state.page = 'oauth'
                st.rerun()

    # OAuth Credentials Screen
    elif st.session_state.page == 'oauth':
        st.markdown('<div class="title">OAuth Credentials</div>', unsafe_allow_html=True)
        
        # Credentials Form
        OAuthCredentialsGuide.credentials_form()
        
        # Credentials Guide
        OAuthCredentialsGuide.display_credentials_guide()

        # Back to Welcome Button
        if st.button("Back to Welcome"):
            st.session_state.page = 'welcome'
            st.rerun()

if __name__ == "__main__":
    main()
