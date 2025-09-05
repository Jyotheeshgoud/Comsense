import streamlit as st
from comments import fetch_comments
from twitter_comments import (
    initialize_twitter_client_v2,
    extract_tweet_id_from_url,
    fetch_tweet_replies,
    load_replies_in_format,
    summarize_replies,
    categorize_replies
)
from utils import get_summary
import base64
from transformers import pipeline
import re
import tweepy



# Set page configuration
st.set_page_config(page_title="YouTube Comment Analyzer", layout="wide")

# Add custom CSS for styling
def add_custom_styles():
    custom_css = r"""
    <style>
        /* General styling */
        .stApp {{
            font-family: Arial, sans-serif;
        }}
       body, html {
    background-color: black;
    margin: 0;
    padding: 0;
    width: 100%;
}
.container {
  width: 100%;
  margin: 0;
  padding: 0;
}
        .nav-links {
            display: flex;
            justify-content: space-evenly;
            align-items: center;
            margin-top:45px;
            padding: 15px 0;
            background: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 100;
            color: white;
        }

        .nav-links a {
            color: white;
            text-decoration: none;
            font-size: 1.2rem;
            padding: 10px 15px;
            transition: background-color 0.3s;
        }

        .nav-links a:hover {
            background-color: #575757;
            border-radius: 5px;
        }

        .banner {
            position: relative; /* Make sure the content sits on top of the video */
            height: 100vh;
            width: 100% ;
            overflow: hidden; /* Ensure the video fills the area */
            left:0;
            right : 0;
        }

        #background-video {
            position: absolute; /* Position the video behind the content */
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover; /* Make the video cover the full screen */
        }

        .content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            text-align: center;
            z-index: 1;  /* Ensures the text stays on top of the video */
        }

        .content h1 {
            font-size: 2rem; /* Adjust size of the heading */
            color: white;
        }

        .content p {
            font-size: 1.5rem; /* Adjust size of the heading */
            color: white;
        }

        

        /* Contact form */
        .contact-form {
            margin: 0 auto;
            width: 60%;
            padding: 20px;
            border-radius: 10px;
        }

       footer {
    display: flex;
    justify-content: center; /* Center the content inside the footer */
    align-items: center;
    padding: 15px 0;
    background: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
    position: auto; /* Positioning it relative to the screen */
    bottom: 0;
    left: 0;
    width: 100%; /* Make it span the full width of the screen */
    color: white;
    z-index: 100;
    margin-top: 35px; /* Adjust the spacing above the footer */
}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

add_custom_styles()

# Header navigation
st.markdown(
    """
    <div class="nav-links">
        <a href="#home">Home</a>
        <a href="#comments">Comments</a>
        <a href="#about-us">About</a>
        <a href="#contact-us">Contact</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Function to encode video to Base64
def video_to_base64(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode()

# Encode the video
video_base64 = video_to_base64("static/bg.mp4")

# Sections
st.markdown('<a name="home"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown(
        f"""
        <div class="banner">
            <video autoplay muted loop id="background-video">
                 <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <div class="content">
                <h1>ComSense</h1>
                <p>Transforming Comments into Clarity, Empowering Insights for Smarter Decisions.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )




# Custom CSS for styling
st.markdown(
    """
    <style>
        /* General Page Styling */
        body {
            margin: 0;
            padding: 0;
        }
        .container {
            width: 100%;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: start;
        }
        
        .left-section {
            width: 48%;
        }
        .right-section {
            width: 48%;
        }
        .stButton button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton button:hover {
            background: #45a049;
        }
        .stTextInput > div {
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .spinner-container {
            text-align: center;
            font-size: 18px;
            margin-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page styling for 100% height and width
st.markdown(
    """
    <style>
        body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #121212;
        }

        .styled-button {
            background-color: #1e1e1e; /* Dark background */
            color: white !important; /* White text color */
            padding: 10px 20px; /* Padding around the text */
            text-align: center; /* Center the text */
            display: inline-block; /* Inline display */
            font-size: 16px; /* Font size */
            margin: 10px; /* Margin around the button */
            border: 1px solid white; /* Thin white border */
            border-radius: 8px; /* Rounded corners */
            cursor: pointer; /* Pointer cursor on hover */
            text-decoration: none !important; /* Remove underline from link */
            transition: background-color 0.3s, transform 0.2s; /* Smooth transition for background color and scale */
        }

        .styled-button:hover {
            background-color: #333; /* Darker shade on hover */
            transform: scale(1.05); /* Slight scale effect on hover */
        }

        h1, p {
            color: white; /* White text for heading and paragraph */
        }

        h1 {
            font-size: 40px; /* Big heading */
            margin-bottom: 20px; /* Space below the heading */
        }

        p {
            font-size: 20px; /* Paragraph size */
            margin-bottom: 40px; /* Space below the paragraph */
        }

        .buttons-container {
            display: flex;
            justify-content: center;
            align-items: center; /* Center align items vertically */
            gap: 20px; /* Space between buttons */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Anchor link for the comments section
st.markdown('<a name="comments"></a>', unsafe_allow_html=True)

# Heading and paragraph
st.markdown(
    """
    <h1 style='text-align: center;'>Comments Analysis</h1>
    <p style='text-align: center;'>Select a platform to view and analyze comments.</p>
    """,
    unsafe_allow_html=True,
)

# Center buttons in the viewport
st.markdown(
    """
    <div class="buttons-container">
        <a href="#youtube" class="styled-button">YouTube</a>
        <a href="#twitter" class="styled-button">Twitter</a>
    </div>
    """,
    unsafe_allow_html=True,
)




st.markdown('<a name="youtube"></a>', unsafe_allow_html=True)
# Header and Instructions
st.title("YouTube Comment Analyzer")
st.write(
    "Use this tool to generate summaries from comments under any YouTube video. "
    "The tool uses **Google Gemini** paired with **LangChain** to generate the summaries."
)

# Main container with two sections
left, right = st.columns(2)

# Left Section - Input Form
with left:
    st.markdown("<div class='left-section'>", unsafe_allow_html=True)
    st.header("Input Section")
    form = st.form("template_form")
    url_input = form.text_input(
        "Enter YouTube video URL",
        placeholder="Paste your YouTube video link here...",
        value="",
    )
    submit = form.form_submit_button("Get Summary")
    st.markdown("</div>", unsafe_allow_html=True)

# Placeholder for Right Section - Output
with right:
    st.markdown("<div class='right-section'>", unsafe_allow_html=True)
    st.header("Summary Section")
    if submit and url_input:
        with st.spinner("Fetching Summary..."):
            # Get Comments from YouTube API - INPUT
            text = fetch_comments(url_input)
            
            if text:  # Proceed only if comments are fetched
                # Tokenization and Summarization - MAIN CODE
                final_summary = get_summary(text)
                
                # Display the output on Streamlit - OUTPUT
                st.markdown(
                    f"<p style='font-size:18px; line-height:1.6;'>{final_summary}</p>",
                    unsafe_allow_html=True,
                )
            else:
                st.error("Unable to fetch comments. Please check the video or try again.")
    else:
        st.info("Submit a YouTube URL to display the summary.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<a name="twitter"></a>', unsafe_allow_html=True)
# Twitter API credentials
api_key = st.secrets["TWITTER_API_KEY"]
api_key_secret = st.secrets["TWITTER_API_KEY_SECRET"]
access_token = st.secrets["TWITTER_ACCESS_TOKEN"]
access_token_secret = st.secrets["TWITTER_ACCESS_TOKEN_SECRET"]
bearer_token = st.secrets["TWITTER_BEARER_TOKEN"]

# Initialize Twitter API client
def initialize_twitter_api():
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_key_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    return client

# Main UI for Twitter
st.title("Twitter Comments Analyzer")
st.write(
    "Use this tool to fetch and summarize comments under a specific tweet. "
    "Provide a tweet URL to begin."
)

# Create two columns for the layout
left, right = st.columns(2)

# Left Section - Input Form
with left:
    st.markdown("<div class='left-section'>", unsafe_allow_html=True)
    st.header("Input Section")
    # Wrap input fields in a form for Twitter
    with st.form("twitter_form"):
        tweet_url = st.text_input(
            "Enter Tweet URL",
            placeholder="Paste the tweet URL here...",
            value=""
        )
        max_results = st.slider("Number of Comments to fetch", 1, 100, 10)
        submit_tweet = st.form_submit_button("Get Summary")
    st.markdown("</div>", unsafe_allow_html=True)

# Right Section - Output for Twitter
with right:
    st.markdown("<div class='right-section'>", unsafe_allow_html=True)
    st.header("Summary Section")
    if submit_tweet and tweet_url:
        with st.spinner("Fetching comments and summarizing..."):
            # Extract Tweet ID
            tweet_id = extract_tweet_id_from_url(tweet_url)
            if tweet_id:
                # Initialize Twitter client and fetch comments
                client = initialize_twitter_api()
                comments = fetch_tweet_replies(client, tweet_id, max_replies=max_results)
                if comments:
                    # Aggregate and summarize replies
                    formatted_replies = load_replies_in_format(comments)
                    summary = summarize_replies(comments)
                    
                    st.write("### Summary of Comments")
                    if summary:
                        st.write(summary)
                else:
                    st.error("No comments found or an error occurred.")
            else:
                st.error("Invalid tweet URL. Please check and try again.")
    else:
        st.info("Submit a Twitter URL to display the summary.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<a name="facebook"></a>', unsafe_allow_html=True)


# Header and Instructions


# Instagram Comments Section (This is just a placeholder for now)

st.markdown('<a name="about-us"></a>', unsafe_allow_html=True)

with st.container():
    st.header("About Us")

    # Add CSS for styling
    st.markdown(
        """
        <style>
           /* Container for the about cards */
.about-cards-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 20px;
    padding: 20px;
}

/* Styling for individual cards */
.about-card {
    background-color: #f4f4f4;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    width: 300px;  /* Default width (for larger screens) */
    transition: transform 0.3s ease-in-out;
}

/* Hover effect for cards */
.about-card:hover {
    transform: translateY(-10px);
}

/* Responsive Design */
@media screen and (max-width: 1200px) {
    .about-card {
        width: 45%; /* 2 cards per row on medium screens */
    }
}

@media screen and (max-width: 768px) {
    .about-card {
        width: 100%; /* 1 card per row on smaller screens */
    }
}

@media screen and (max-width: 480px) {
    .about-cards-container {
        flex-direction: column; /* Stack cards vertically on very small screens */
        align-items: center;
    }
    .about-card {
        width: 90%; /* Cards take up most of the width on small screens */
    }
}

        </style>
        """,
        unsafe_allow_html=True,
    )
import base64
import streamlit as st

# Function to encode image to Base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encode the image
img_base64 = image_to_base64("static/image.png")
img2_base64 = image_to_base64("static/image2.jpg")
img3_base64 = image_to_base64("static/image3.png")

# Streamlit "About Us" Section
st.markdown('<a name="about-us"></a>', unsafe_allow_html=True)
with st.container():

    # Add CSS for styling and responsiveness
    st.markdown(
        f"""
        <style>
            /* Container for the cards */
            .cards-container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                gap: 20px;
                margin-top: 20px;
                padding: 10px;
            }}

            /* Styling for individual cards */
            .card {{
                background-color: #000000; /* Black background */
                border: 1px solid #ffffff; /* Thin white border */
                border-radius: 10px;
                width: 100%; /* Default width for smaller screens */
                text-align: center;
                padding: 20px;
                box-sizing: border-box;
                transition: transform 0.3s ease-in-out;
            }}

            /* Hover effect for cards */
            .card:hover {{
                transform: translateY(-10px);
            }}

            /* Styling for card images */
            .card img {{
                width: 100%;
                height: auto;
                border-radius: 10px 10px 0 0;
            }}

            /* Styling for card headings */
            .card h3 {{
                font-size: 20px;
                color: #ffffff; /* White text for contrast */
                margin: 15px 0 10px;
            }}

            /* Styling for card paragraphs */
            .card p {{
                font-size: 14px;
                color: #cccccc; /* Light grey for description */
                line-height: 1.5;
            }}

            /* Responsive Design */
            @media (min-width: 768px) {{
                .card {{
                    width: 45%; /* 2 cards per row on medium screens */
                }}
            }}

            @media (min-width: 1024px) {{
                .card {{
                    width: 30%; /* 3 cards per row on larger screens */
                }}
            }}
        </style>

        <div class="cards-container">
            <div class="card">
                <img src="data:image/png;base64,{img_base64}" alt="Feature 1">
                <h3>Efficient Data Analysis</h3>
                <p>ComSense excels at analyzing comments from platforms like YouTube and Twitter to extract valuable insights. Using advanced natural language processing and sentiment analysis, it identifies key trends, opinions, and sentiments in user comments. Whether it's feedback on a video or a tweet, ComSense helps you gain meaningful insights and make informed decisions effortlessly.</p>
            </div>
            <div class="card">
                <img src="data:image/jpeg;base64,{img2_base64}" alt="Feature 2">
                <h3>User-Friendly Design</h3>
                <p>ComSense offers a user-friendly interface designed for everyone, from beginners to experts. Its intuitive layout ensures a smooth and efficient experience, making comment analysis accessible and straightforward for all users.</p>
            </div>
            <div class="card">
                <img src="data:image/png;base64,{img3_base64}" alt="Feature 3">
                <h3>AI-Powered Summaries</h3>
                <p>Leverage the power of cutting-edge AI with ComSense. It intelligently condenses lengthy comment threads into clear and concise insights. Whether you're analyzing opinions from tweets or video comments, ComSense provides meaningful summaries in seconds, saving you time and effort.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )




import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

st.markdown('<a name="contact-us"></a>', unsafe_allow_html=True)

def send_email(name, sender_email, message):
    try:
        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email_address = "chettimchettyhemasri@gmail.com"  
        sender_email_password = "xmvb syyz audm kuzh"  

        # Recipient email
        recipient_email = "chettimchettyhemasri@gmail.com"

        # Email content
        subject = f"New Contact Form Submission from {name}"
        body = f"""
        You have received a new message from the contact form:
        
        Name: {name}
        Email: {sender_email}
        Message:
        {message}
        """

        # Create email
        msg = MIMEMultipart()
        msg["From"] = sender_email_address
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email_address, sender_email_password)
        server.sendmail(sender_email_address, recipient_email, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# Contact Form
with st.container():
    st.header("Contact Us")
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")

    if st.button("Send Message"):
        if name and email and message:
            # Call the send_email function
            if send_email(name, email, message):
                st.success("Your message has been sent successfully!")
            else:
                st.error("Failed to send your message. Please try again later.")
        else:
            st.warning("Please fill out all fields before sending.")

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <footer>
        <p> &copy; 2024. All rights reserved. @ComSense</p>

    </footer>
    """,
    unsafe_allow_html=True,
)
