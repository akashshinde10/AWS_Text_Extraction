import boto3

#document
s3BucketName = "bucket-name"
documentName = "image-name.jpg"

#read document content if image is stored on local computer
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

#amazon textract client
textract = boto3.client('textract')

#call amazon textract
response = textract.detect_document_text(
    Document = {
        'Bytes': imageBytes
    })

# to obtain the image from s3_bucket use
# {'S3Object':{
    
#     'Bucket':'Bucket_name',
#     'name': 'name_of_iamge'
# }} 
# to obtain the image from local computer use
# {'Bytes' : source_bytes}
#print response

#print the detected text
columns =[]
lines = []
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
       column_found = False
       for index, column in enumerate(columns):
           bbox_left = item["Geometry"]["BoundingBox"]["Left"]
           bbox_right = item["Geometry"]["BoundingBox"]["Left"]  + item["Geometry"]["BoundingBox"]["Width"]
           bbox_centre = item["Geometry"]["BoundingBox"]["Left"]  + item["Geometry"]["BoundingBox"]["Width"]/2
           column_centre = column['left'] + column['right']/2

           if(bbox_centre > column['left'] and bbox_centre < column['right']) or (column_centre > bbox_left and column_centre < bbox_right):
                lines.append([index, item["Text"]])
                column_found=True
                break

       if not column_found:
           columns.append({'left' : item["Geometry"]["BoundingBox"]["Left"], 'right':item["Geometry"]["BoundingBox"]["Left"] + item["Geometry"]["BoundingBox"]["Left"]})
           lines.append([len(columns) - 1 , item["Text"]])

lines.sort(key=lambda x: x[0])
for line in lines:
    print(line[1])
    
        
