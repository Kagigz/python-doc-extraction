import logging
import io
import os
import json
import azure.functions as func
from . import docx_extractor
from . import pptx_extractor
from . import processText
from ..shared_code import storageHelper
from ..shared_code import config

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Doc extraction started')

    try:
        payload = req.get_json()
        filename = payload.get('filename')
    except:
        filename = ''
        logging.info('No file name was provided.')

    print(filename)

    try:
        service = storageHelper.InitializeBlobService(config.blobConfig)
        logging.info('Blob service initialized.')
    except:
        service = None
        logging.info('Blob service initialization failed.')
    

    extractedDoc = None

    if(service != None and filename != ''):

        directory = 'files'
        try:
            os.mkdir(directory)
        except:
            pass
        
        path = os.path.join(directory,filename)
        storageHelper.getFile(config.blobConfig,service,filename,path)
        splitname = filename.split('.')
        extension = splitname[len(splitname)-1]

        if(extension == 'docx'):
            extractedDoc = docx_extractor.extract_docx(path)
        elif(extension == 'pptx'):
            extractedDoc = pptx_extractor.extract_pptx(path)
 
        logging.info('Done.')

    else:
        logging.info('There was a problem retrieving the file.')

    if(extractedDoc != None):
        processedText = processText.processDoc(extractedDoc)
        return func.HttpResponse(
            json.dumps([ {
                'title': processedText['title'], 
                'author':processedText['author'],
                'date': str(processedText['date']),
                'language':processedText['lang'],
                'modDate':str(processedText['modDate']),
                'text': processedText['text'],
                'allText': processedText['allText'],
                'freqWords':processedText['freqWords']
            } ]),
            status_code=200
        )
    else:
        return func.HttpResponse(
                json.dumps([ {
                'title': '', 
                'author':'',
                'date': '',
                'text': '',
                'allText': '',
                'freqWords':''
            } ]),
            status_code=200
        )
