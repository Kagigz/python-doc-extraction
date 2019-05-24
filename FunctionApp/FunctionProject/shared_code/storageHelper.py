from azure.storage.blob import BlockBlobService, PublicAccess

# Initializes Blob Storage Service
def InitializeBlobService(config):
    service = BlockBlobService(account_name=config['ACCOUNTNAME'], account_key=config['KEY'])
    return service

# Uploads file to Blob Storage
def uploadFile(config,service,filename,f):
    try:
        service.create_blob_from_path(config['CONTAINER'], filename, f)
        print("File uploaded to blob storage.")
    except Exception as e:
        print(e)

# Gets file from Blob Storage and stores it locally
def getFile(config,service,filename,path):
    try:
        service.get_blob_to_path(config['CONTAINER'], filename, path)
        print("File retrieved from blob storage.")
    except Exception as e:
        print(e)
