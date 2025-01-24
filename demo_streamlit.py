import streamlit as st

st.title("Input Demo")

name = st.text_input("Enter your name:", "John Doe")
age = st.number_input("Enter your age:", 30)
rating = st.slider("Rate your experience (1-10):", 1, 10, 5)

output_text = f"Name: {name}\nAge: {age}\nRating: {rating}"
st.text_area("Output:", value=output_text, height=100)
