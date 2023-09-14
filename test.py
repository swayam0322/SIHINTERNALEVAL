import os
from fastapi import FastAPI
from pydantic import BaseModel
import boto3
import botocore

app = FastAPI()

class inputParameters(BaseModel):
    amplification_factor: int
    fl: float
    fh: float
    fs: float
    n_filter_tap: int
    filter_type: str
    temporal : bool

def upload_file_to_s3(file_name,bucket,object_name):
    print("Uploading video to S3...")
    s3 = boto3.client('s3',aws_access_key_id='AKIAVAHZBIOLFULVDWVC',aws_secret_access_key='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')

    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        s3.upload_file(file_name, bucket, object_name)
        print(f"File '{file_name}' uploaded to S3 bucket '{bucket}' as '{object_name}'")
        return True
    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")
        return False

def download_video_from_s3(bucket_name,key, download_path):
    print("Downloading video from S3...")
    s3 = boto3.resource('s3',aws_access_key_id='AKIAVAHZBIOLFULVDWVC',aws_secret_access_key='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')
    try:
        s3.Bucket(bucket_name).download_file(key, download_path)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

@app.post("/upload/")
async def get(json: inputParameters):
    BUCKET_NAME = "skillissuevid"
    object = "v2.mp4"
    download_video_from_s3(BUCKET_NAME,object,object)
    # command = (
    #     f"python3 main.py --config_file=configs/o3f_hmhm2_bg_qnoise_mix4_nl_n_t_ds3.conf --phase=run_temporal --vid_dir=data/vids/{json.video} --out_dir=data/output/{json.video} --amplification_factor={json.ampFact} --fl={json.fl} --fh={json.fh} --fs={json.fs} --n_filter_tap={json.n_tap} --filter_type={json.filter_type}"
    # )
    # os.system(command)
    upload_file_to_s3(object,BUCKET_NAME,object)
    return {"link": f"https://d175wanlbunlv0.cloudfront.net/{object}"}

if __name__ == '__main__':
    print("Starting server...")
    os.system("uvicorn test:app --host 0.0.0.0 --port 8000")

