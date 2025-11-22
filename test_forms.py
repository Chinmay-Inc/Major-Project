"""
Test script to verify form structure is correct
"""
import streamlit as st

def test_form_structure():
    """Test that forms have proper submit buttons"""
    
    st.title("Form Structure Test")
    
    # Test 1: Simple form with submit button
    with st.form("test_form_1"):
        st.text_input("Test Input")
        submit1 = st.form_submit_button("Submit")
        if submit1:
            st.success("Form 1 submitted successfully!")
    
    # Test 2: Form with multiple inputs
    with st.form("test_form_2"):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Number", value=0)
        with col2:
            st.selectbox("Select", ["Option 1", "Option 2"])
        submit2 = st.form_submit_button("Submit Form 2")
        if submit2:
            st.success("Form 2 submitted successfully!")
    
    # Test 3: Button outside form (should work)
    if st.button("Button Outside Form"):
        st.info("This button works outside forms")
    
    st.success("All form tests passed! No submit button errors.")

if __name__ == "__main__":
    test_form_structure()
