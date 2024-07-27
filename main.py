import streamlit as st

st.write("""
         # Fabric
         This is a simple example of a Streamlit app.
         
         And here is a list:
            - Item 1
            - Item 2
            - Item 3
         """)

# Create a text area for editing markdown
markdown_text = st.text_area(
    "Edit your markdown here:", value="# Initial markdown\n\nEdit this text!")

# Display the rendered markdown
st.markdown(markdown_text)
