import boto3

#document
documentName = "image-name.jpg"

#read document content if image is stored on local computer
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

#amazon textract client
textract = boto3.client('textract')

#call amazon textract
response = textract.detect_document_text(Document = {'Bytes': imageBytes})

# to obtain the image from s3_bucket use
# {'S3Object':{
    
#     'Bucket':'Bucket_name',
#     'name': 'name_of_iamge'
# }} 
# to obtain the image from local computer use
# {'Bytes' : source_bytes}

#print response

#print the detected text
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print('\033[94m' + item["Text"] + '\033[0m')