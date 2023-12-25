import os
import time
import streamlit as st


class Upload:
    def __init__(self):
        self.uploaded_file = st.file_uploader("File uploader")
        if self.uploaded_file is not None:
            file_result = self.save_uploaded_file(self.uploaded_file)

        css = '''
            <style>
                [data-testid='stFileUploader'] {
                    width: max-content;
                }
                [data-testid='stFileUploader'] section {
                    padding: 0;
                    float: left;
                }
                [data-testid='stFileUploader'] section > input + div {
                    display: none;
                }
                [data-testid='stFileUploader'] section + div {
                    float: right;
                    padding-top: 0;
                }

            </style>
            '''

        st.markdown(css, unsafe_allow_html=True)

    def save_uploaded_file(self, uploaded_file):
        try:
            filename = self.uploaded_file.name
            os.makedirs('videos', exist_ok=True)
            with open(os.path.join('videos', self.uploaded_file.name), "wb") as f:
                f.write(self.uploaded_file.getbuffer())
            return st.success("Saved File to videos".format(filename))
        except Exception as e:
            print(e)
            return st.error("An error occurred during file upload.")


class Record:
    pass


class Watch:
    pass


class ViewUploaded:
    pass


class RemoveFiles:
    pass
