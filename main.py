import streamlit as st
import classes as cl

st.set_page_config(layout="wide", page_title='Beyond Death',
                   initial_sidebar_state='collapsed')


if __name__ == "__main__":
    st.title('Upload a recorded video!')
    file = cl.Upload()
    view_uploaded = cl.ViewUploaded()
