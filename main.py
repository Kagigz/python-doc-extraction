import docx_extractor
import pptx_extractor
import processText

def getDocInfo(filename):
    names = filename.split('.')
    extension = names[len(names)-1]
    extractedDoc = None
    if(extension == 'docx'):
        extractedDoc = docx_extractor.extract_docx(filename)
    elif(extension == 'pptx'):
        extractedDoc = pptx_extractor.extract_pptx(filename)
    return extractedDoc


pptFile = './test.pptx'
wordFile = './test.docx'

ppt = getDocInfo(pptFile)
processedTextPpt = processText.processDoc(ppt)

print('PPT file:')
print(processedTextPpt)

word = getDocInfo(wordFile)
processedTextWord = processText.processDoc(word,20)

print('Word file:')
print(processedTextWord)






