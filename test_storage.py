import os
from google.cloud import storage

def upload_directory_to_gcs(bucket_name, local_directory):
    """
    Uploads a local directory to a GCS bucket.

    Args:
        bucket_name (str): Name of the GCS bucket.
        local_directory (str): Path to the local directory.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for root, _, files in os.walk(local_directory):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_directory)
            blob = bucket.blob(relative_path)
            blob.upload_from_filename(local_path)
            print(f'Uploaded {local_path} to gs://{bucket_name}/{relative_path}')

# Usage
upload_directory_to_gcs('flux-dev-cr-models', './models/')
