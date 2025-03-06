import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_deepseek

st.title("AI Web Scraper")

# Input for URL
url = st.text_input("Enter the URL")

if st.button("Scrape Site"):
    if not url:
        st.error("Please enter a valid URL.")
    else:
        st.write("Scraping the website...")
        
        try:
            # Scrape the website
            result = scrape_website(url)
            body_content, links, img_links = extract_body_content(result)
            clean_content = clean_body_content(body_content)

            # Store the cleaned content in session state
            st.session_state.dom_content = clean_content

            # Display the cleaned content
            with st.expander("View textual content"):
                st.text_area("Text Content", clean_content, height=300)
        except Exception as e:
            st.error(f"An error occurred while scraping: {e}")

# Parse the content if it exists in session state
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if not parse_description:
            st.error("Please enter a description of what you want to parse.")
        else:
            st.write("Parsing the content...")

            try:
                # Split the content into chunks
                dom_chunks = split_dom_content(st.session_state.dom_content)
                # Parse the content with DeepSeek
                parsed_result = parse_with_deepseek(dom_chunks, parse_description)
                st.write("Parsed Result:")
                st.write(parsed_result)
            except Exception as e:
                st.error(f"An error occurred while parsing: {e}")