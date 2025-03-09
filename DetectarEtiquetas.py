import json
import boto3

def lambda_handler(event, context):
    # Inicializar los clientes S3 y Rekognition
    s3_client = boto3.client('s3')
    rekognition_client = boto3.client('rekognition')
    
    # Obtener el bucket y el nombre del archivo de la imagen del evento
    bucket = event['body']['bucket_name']
    image_name = event['body']['image_name']
    
    # Llamar a Rekognition para detectar etiquetas en la imagen
    response = rekognition_client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': image_name
            }
        },
        MaxLabels=10,  # Puedes ajustar el número máximo de etiquetas que deseas detectar
        MinConfidence=80  # Puedes ajustar el umbral de confianza mínima
    )
    
    # Guardar en json las etiquetas detectadas (también puedes almacenarlas en S3, DynamoDB, etc.)
    lista = []
    for label in response['Labels']:
        etiqueta = {
            'nombre': label['Name'],
            'porcentaje_confianza': label['Confidence']
        }
        lista.append(etiqueta)
    
    return {
        'statusCode': 200,
        'etiquetas': lista
    }
