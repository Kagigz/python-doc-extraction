import sys
from docx.api import Document

def extract_docx(filename):

    document = Document(filename)
    doc = {}

    # TITLE
    title = ""
    if(document.core_properties.title == ''):
        title = filename.split('.')[0]
    else:
        title = document.core_properties.title
    doc["title"] = title

    # AUTHOR
    author = ""
    if(document.core_properties.author != ''):
        author = document.core_properties.author
    doc["author"] = author

    # DATE
    date = ""
    if(document.core_properties.created != ''):
        date = document.core_properties.created
    doc["date"] = date

    # MODIFIED DATE
    modDate = ""
    if(document.core_properties.modified != ''):
        modDate = document.core_properties.modified
    doc["modDate"] = modDate

    # LANGUAGE
    lang = ""
    if(document.core_properties.language != ''):
        lang = document.core_properties.language
    doc["lang"] = lang


    paragraphs = []

    for p in document.paragraphs:
        if(p.text != '' and p.text != '\n ' and p.text != ' '):
            paragraphs.append(p.text)

    doc["text"] = paragraphs

    return doc
