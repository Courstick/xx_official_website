import datetime
import json

from django.conf import settings
from minio import Minio
from minio.datatypes import PostPolicy


class MinioClient(object):
    PART_IMAGE_BUCKET = 'part_image'

    READ_ONLY_POLICY = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::bucket_name/*",
            },
        ],
    }

    def __init__(self, addr, ak, sk):
        self.base_url = f'http://{addr}'
        self.client = Minio(addr, access_key=ak, secret_key=sk, secure=True)

    def create_bucket(self, bucket_name, policy=None):
        if self.check_bucket_exists(bucket_name):
            return
        self.client.make_bucket(bucket_name)
        if policy:
            self.client.set_bucket_policy(bucket_name, policy)

    def check_bucket_exists(self, bucket_name):
        return self.client.bucket_exists(bucket_name=bucket_name)

    def get_temp_download_url(self, object_name, bucket_name=PART_IMAGE_BUCKET, expiry=datetime.timedelta(days=1)):
        return self.client.presigned_get_object(bucket_name, object_name, expires=expiry)

    def get_temp_upload_url(self, object_name, bucket_name=PART_IMAGE_BUCKET, expiry=datetime.timedelta(hours=1)):
        return self.client.presigned_put_object(bucket_name, object_name, expiry)

    def get_post_policy(self, bucket_name=PART_IMAGE_BUCKET, expiry=datetime.timedelta(days=3)):
        # 设置read_only policy
        read_policy = json.dumps(self.READ_ONLY_POLICY).replace('bucket_name', bucket_name)

        self.create_bucket(bucket_name, read_policy)
        policy = PostPolicy(bucket_name, datetime.datetime.utcnow() + expiry)
        policy.add_starts_with_condition("key", '')
        policy.add_content_length_range_condition(1, 500 * 1024 * 1024)
        return self.client.presigned_post_policy(policy)

    def get_upload_form(self, bucket="part_image"):
        formdata = self.get_post_policy()
        formdata['bucket'] = bucket
        return {
            'postUrl': self.base_url,
            'formData': formdata
        }

    def download_excel(self, object_name, file_path, bucket_name=PART_IMAGE_BUCKET):
        return self.client.fget_object(bucket_name, object_name, file_path)


minio_helper = Minio(settings["MINIO_ADDR"], settings["MINIO_AK"], settings["MINIO_SK"])
