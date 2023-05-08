# Creating a simple OCR and translation tool
# Made by: Luis Carlos Manrique Ruiz

# conda: own environment
# Generating requirements: pip freeze > requirements.txt


# %%
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt
from textblob import TextBlob
import io
import os
import glob
import streamlit as st
import base64

# import cv2
# import argparse


class FileDownloader(object):
    def __init__(self, data, filename):
        super(FileDownloader, self).__init__()
        self.data = data
        self.filename = filename

    def download(self):
        b64 = base64.b64encode(self.data.encode()).decode()
        filename_split = filename.split("/")[-1]
        newfilename = filename_split.replace(".jpg", "_ocr.txt")
        st.markdown("#### Download File from OCR ###")
        href = f'<a href="data:file/{filename};base64,{b64}" download="{newfilename}">Click Here!!</a>'
        st.markdown(href, unsafe_allow_html=True)


def file_selector(folder_path="."):
    filenames = os.listdir(folder_path)
    filenames = [x for x in filenames if any(a in x for a in ["jpg", "png"])]
    selected_filename = st.selectbox("Select a file", filenames)
    return os.path.join(folder_path, selected_filename)


if __name__ == "__main__":
    # Select a file
    st.title("Translating documents from Images")

    option = st.selectbox(
        "Translating from Japanese into: ", ("English", "Chinese", "Spanish")
    )

    if st.checkbox("Select a file in current directory"):
        # st.stop()
        folder_path = "."

        if st.checkbox("Change directory"):
            folder_path = st.text_input("Enter folder path", ".")
        filename = file_selector(folder_path=folder_path)

        st.write("You selected `%s`" % filename)
        image = Image.open(filename)
        st.image(image, caption="Your document")

        start_ocr = st.button("Start OCR")
        start_translation = st.button("Start translation")

        if start_ocr:
            with st.spinner(text="In progress..."):
                gray_image = image.convert("L")
                result_pre = pytesseract.image_to_string(gray_image, lang="Japanese")
                result_final_pre = result_pre.replace(" ", "")
            st.success("Done!")

            st.write(result_final_pre)
            download = FileDownloader(result_final_pre, filename).download()

        if start_translation:
            gray_image = image.convert("L")

            result_pre = pytesseract.image_to_string(gray_image, lang="Japanese")
            result_image_g = result_pre.replace(" ", "")

            tb = TextBlob(result_image_g)
            translated = tb.translate(to="en")
            st.write(translated)
            download = FileDownloader(str(translated), filename).download()
