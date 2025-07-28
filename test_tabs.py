import streamlit as st

st.set_page_config(page_title="Tab Test", layout="wide")

st.title("🧪 Tab Visibility Test")

# Test basic tabs
st.header("Basic Tab Test")
tab1, tab2, tab3 = st.tabs(["📊 Tab One", "🔍 Tab Two", "⚙️ Tab Three"])

with tab1:
    st.write("This is Tab One content")
    st.success("You can see Tab One!")

with tab2:
    st.write("This is Tab Two content")
    st.info("You can see Tab Two!")

with tab3:
    st.write("This is Tab Three content")
    st.warning("You can see Tab Three!")

# Test with emojis and longer names
st.header("Enhanced Tab Test")
advanced_tab1, advanced_tab2, advanced_tab3 = st.tabs([
    "🎯 Predictions & Analysis", 
    "📊 Portfolio Management", 
    "📈 Advanced Analytics"
])

with advanced_tab1:
    st.write("Advanced Tab 1 content")

with advanced_tab2:
    st.write("Advanced Tab 2 content")

with advanced_tab3:
    st.write("Advanced Tab 3 content")

st.markdown("---")
st.info("If you can see the tab names above, then tabs are working correctly!")