import os
import streamlit as st

from functions import modify_xml_with_llm, displayXML, cleanXML

st.set_page_config(layout="wide")

st.title("XML Bot")

xml_column, chatbot_column = st.columns((0.5, 0.5))
with xml_column:
    st.markdown("Upload XML file")
    uploaded_file = st.file_uploader("UPLOAD", type="xml")
    if uploaded_file:
        original_file_path = f"{os.getcwd()}/data/original/{uploaded_file.name}"
        with open(original_file_path, "wb") as f:
            f.write(uploaded_file.read())
        displayXML(original_file_path)

with chatbot_column:
    st.markdown("CHATBOT")
    query = st.text_input("Question: ")

    if query and uploaded_file:
        try:
            with open(f"{os.getcwd()}/data/original/{uploaded_file.name}", 'rb') as f:
                data = f.read()

            xml_data = data
            updated_xml = modify_xml_with_llm(xml_data, query)
            if updated_xml.parts[0].text == "Please ask a relevant question. \n":
                st.error("Please ask a relevant question.")

            else:
                output_xml = cleanXML(updated_xml)
                print(output_xml)

                updated_file_path = f"{os.getcwd()}/data/updated/{uploaded_file.name}"
                with open(updated_file_path, "wb") as f:
                    f.write(output_xml.encode("utf-8"))

                st.download_button("Download file", output_xml, file_name=f"updated_{uploaded_file.name}")

                displayXML(f"{os.getcwd()}/data/updated/{uploaded_file.name}")

        except Exception as e:
            st.error(f"Error: {e}")

    elif not uploaded_file:
        st.error("Please upload the XML file first.")








