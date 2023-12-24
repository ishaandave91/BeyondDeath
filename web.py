# To do:
# Accepting multiple files: accept_multiple_files (bool) in st.file_uploader

import streamlit as st
import functions
import datetime
from pathlib import Path

st.set_page_config(layout="wide", page_title='Beyond Death',
                   initial_sidebar_state='collapsed')


todos = functions.load_file()


def show_uploaded_files():
    for index, item in enumerate(todos):
        st.write(index + 1, item.strip('.mp4'))


def add_filename(filename):
    if filename not in todos:
        # Add else logic to avoid duplication
        todos.append(filename + '\n')
        functions.write_todos(todos)
    else:
        only_name = Path(filename).stem
        todos.append(only_name + str(datetime.datetime.now().time()) + '.mp4' + '\n')
        functions.write_todos(todos)

    return


def record_video():
    pass


col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Upload Video", type='mp4', key='file_picker')
with col2:
    button1 = st.button('Record', on_click=record_video, key='rec_btn')

if len(todos) > 0:
    st.title('Uploaded List:')

if uploaded_file is not None:
    add_filename(uploaded_file.name)
    show_uploaded_files()
else:
    print("New todos:\n", todos)
