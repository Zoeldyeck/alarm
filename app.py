import streamlit as st
tab1, tab2 = st.tabs(["Form", "Data Visualization"])
with tab1:
    st.header("Input Form")
    name = st.text_input("Enter your name:")
    age = st.number_input("Enter your age:", min_value=1, max_value=100)
    submit = st.button("Submit")
    if submit:
        st.write(f"Hello, {name}! You are {age} years old.")
with tab2:
    st.header("Sample Data Visualization")
    st.line_chart([1, 2, 3, 4, 5])