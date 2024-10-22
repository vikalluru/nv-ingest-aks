
#Script for uploading files to Azure Blob storage
from azure.storage.blob import BlobServiceClient
import os
from tqdm import tqdm

# Define your connection string and container
connection_string = "DefaultEndpointsProtocol=https;AccountName=nimdemosa;AccountKey=RsOn4N5EmhpGLp7GbSo6ZZLcWouTarX9N/b1/QuWPVShCV5h7m6M5V4P3Cpzn6hU5X/gzCEl3z3q+AStUbJgag==;EndpointSuffix=core.windows.net"
container_name = "pmcoa-pdf-dataset"
local_path = "/mnt/c/Users/srella/Downloads/test_check/"

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Create the container if it doesn't exist
container_client = blob_service_client.get_container_client(container_name)

directory_path = "nvidia_earnings/"

# Get the list of PDF files
pdf_files = [f for f in os.listdir(local_path) if f.endswith(".pdf")]

# Upload PDFs to the container with a progress bar
for filename in tqdm(pdf_files, desc="Uploading PDFs", unit="file"):
    blob_client = container_client.get_blob_client(directory_path + filename)
    file_path = os.path.join(local_path, filename)

    # Upload the file
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
print("All files uploaded.")