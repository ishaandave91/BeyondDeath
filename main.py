import streamlit as st
import classes as cl

st.set_page_config(layout="wide", page_title='Beyond Death',
                   initial_sidebar_state='collapsed')


def main():
    st.title('Upload a recorded video!')
    print("Uploading starts")
    # if 'file_picker' not in st.session_state:
    file = cl.Upload()
    view_uploaded = cl.ViewUploaded()
    # st.session_state.clear()
    print("Viewssas completed")


if __name__ == "__main__":
    main()