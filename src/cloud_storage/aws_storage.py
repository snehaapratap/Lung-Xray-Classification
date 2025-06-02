# import os
# import sys

# from src.exception.expection import CustomException


# class S3Operation:
#     def sync_folder_to_s3(self, folder: str, bucket_name: str, bucket_folder_name: str) -> None:  # upload
#         try:
#             command: str = (
#                 f"aws s3 sync {folder} s3://{bucket_name}/{bucket_folder_name}/ "
#             )

#             os.system(command)

#         except Exception as e:
#             raise CustomException(e, sys)

#     def sync_folder_from_s3(self, folder: str, bucket_name: str, bucket_folder_name: str) -> None:  # download
#         try:
#             command: str = (
#                 f"aws s3 sync s3://{bucket_name}/{bucket_folder_name}/ {folder} "
#             )

#             os.system(command)

#         except Exception as e:
#             raise CustomException(e, sys)

import os
import sys
from io import StringIO
from typing import List, Union
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.service_resource import Bucket
from src.logger.custom_logging import logging
from src.exception.exception import CustomException


class S3Operation:
    def __init__(self):
        self.s3_client = boto3.client("s3")
        self.s3_resource = boto3.resource("s3")


    def sync_folder_from_s3(
        self, folder: str, bucket_name: str, bucket_folder_name: str
    ) -> None:
        try:
            command: str = (
                f"aws s3 sync s3://{bucket_name}/{bucket_folder_name}/ {folder} "
            )

            os.system(command)

        except Exception as e:
            raise CustomException(e, sys)    

    def upload_file(
        self,
        from_filename: str,
        to_filename: str,
        bucket_name: str,
        remove: bool = True,
    ) -> None:

        """
        Method Name :   upload_file

        Description :   This method uploads the from_filename file to bucket_name bucket with to_filename as bucket filename
        
        Output      :   Folder is created in s3 bucket
        """
        logging.info("Entered the upload_file method of S3Operations class")
        try:
            logging.info(
                f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            self.s3_resource.meta.client.upload_file(
                from_filename, bucket_name, to_filename
            )
            logging.info(
                f"Uploaded {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            if remove is True:
                os.remove(from_filename)
                logging.info(f"Remove is set to {remove}, deleted the file")
            else:
                logging.info(f"Remove is set to {remove}, not deleted the file")
            logging.info("Exited the upload_file method of S3Operations class")

        except Exception as e:
            raise e

            