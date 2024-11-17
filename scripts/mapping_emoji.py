import boto3
import os
from sqlalchemy import create_engine, text

cdn = os.getenv('S3_CDN')
s3_endpoint_url = os.getenv('S3_ENDPOINT_URL')
s3_key = os.getenv('S3_KEY')
s3_secret = os.getenv('S3_SECRET')
s3_bucket = os.getenv('S3_BUCKET')
prefix_emoji = os.getenv('PREFIX_EMOJI')

s3_client = boto3.client('s3', endpoint_url=s3_endpoint_url, aws_access_key_id=s3_key, aws_secret_access_key=s3_secret)

result = s3_client.list_objects(Bucket=s3_bucket, Prefix=prefix_emoji, Delimiter='/')
keys = {f"{cdn}/{content.get('Key')}" for content in result.get('Contents', {})}

engine = create_engine(os.getenv("DATABASE_URI"), echo=True)

with engine.connect() as conn:
    urls_existing = conn.scalars(text("SELECT url FROM emoji WHERE url in :urls"), {"urls": tuple(keys)}).all()

    for url_existing in urls_existing:
        keys.remove(url_existing)

    for key in keys:
        conn.execute(text("INSERT INTO emoji (url) VALUES (:url)"), {"url": key})

    conn.commit()









