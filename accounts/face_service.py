import boto3
from django.conf import settings

rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REKOGNITION_REGION
)

def register_face(image_bytes):
    response = rekognition.index_faces(
        CollectionId=settings.AWS_REKOGNITION_COLLECTION,
        Image={'Bytes': image_bytes},
        DetectionAttributes=[]
    )
    if response['FaceRecords']:
        return response['FaceRecords'][0]['Face']['FaceId']
    return None

def verify_face(image_bytes):
    response = rekognition.search_faces_by_image(
        CollectionId=settings.AWS_REKOGNITION_COLLECTION,
        Image={'Bytes': image_bytes},
        FaceMatchThreshold=90,
        MaxFaces=1
    )
    matches = response.get('FaceMatches', [])
    if matches:
        return matches[0]['Face']['FaceId']
    return None
