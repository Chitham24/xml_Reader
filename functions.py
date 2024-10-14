import os
import google.generativeai as genai
import streamlit as st
import xml.dom.minidom

from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def modify_xml_with_llm(xml_content, instruction):

    prompt = f"""
    Here is an XML file:
    {xml_content}
    Instruction: {instruction}
    Provide the updated XML only.
    Do not provide any their output.
    If instruction is irrelevant to the XML
    file. Reply with "Please ask a relevant question".
    """

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            temperature=0.2,
        ),
    )

    return response.candidates[0].content if response.candidates else "No output from LLM"


def cleanXML(xml_file):
    output_xml = xml_file.parts[0].text
    cleaned_output = output_xml.strip().split('\n', 1)[1].rsplit('\n', 1)[0]

    return cleaned_output


def displayXML(file):

    with open(file, 'rb') as f:
        xml_content = f.read()

    # Parse and pretty-print the XML content
    parsed_xml = xml.dom.minidom.parseString(xml_content)
    pretty_xml_as_string = parsed_xml.toprettyxml()

    st.code(pretty_xml_as_string, language="xml")