import docx

doc = docx.Document("doc.docx")
text=""
for paragraph in doc.paragraphs:
    text += paragraph.text

print(text)
