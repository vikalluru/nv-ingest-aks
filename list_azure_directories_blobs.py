#Checking the Uploaded data files in azure blob storage
from azure.storage.blob import BlobServiceClient

connection_string = "DefaultEndpointsProtocol=https;AccountName=nimdemosa;AccountKey=RsOn4N5EmhpGLp7GbSo6ZZLcWouTarX9N/b1/QuWPVShCV5h7m6M5V4P3Cpzn6hU5X/gzCEl3z3q+AStUbJgag==;EndpointSuffix=core.windows.net"
container_name = "pmcoa-pdf-dataset"

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

def display_predefined_files_from_azure(container_client, container_name):
    amazon_earnings = container_client.get_blob_client("amazon_earnings/Amazon-Q1-2021-Earnings-Release.pdf")
    apple_earnings= container_client.get_blob_client("apple_earnings/_10-Q-Q2-2021-(As-Filed) (1).pdf")
    google_earnings= container_client.get_blob_client("google_earnings/2021-q3-alphabet-10q.pdf")
    meta_earnings= container_client.get_blob_client("meta_earnings/Meta-Q2-2022-Earnings-Call-Transcript.pdf")
    netflix_earnings=container_client.get_blob_client("netflix_earnings/[FINAL]-Susan-Rice-2FNetflix.pdf")
    nvidia_earnings= container_client.get_blob_client("nvidia_earnings/NVIDIA.pdf")
    return amazon_earnings, apple_earnings, google_earnings, meta_earnings, netflix_earnings, nvidia_earnings

def bytes_to_pdf(pdf_bytes):
    # Save the bytes to a temporary PDF file
    pdf_path = "temp.pdf"
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes.download_blob().readall())
    return pdf_path  # Return the path to the saved PDF

def fetch_predefined_files():
    connection_string = "DefaultEndpointsProtocol=https;AccountName=nimdemosa;AccountKey=RsOn4N5EmhpGLp7GbSo6ZZLcWouTarX9N/b1/QuWPVShCV5h7m6M5V4P3Cpzn6hU5X/gzCEl3z3q+AStUbJgag==;EndpointSuffix=core.windows.net"
    container_name = "pmcoa-pdf-dataset"

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    amazon_blob_data, apple_blob_data, google_blob_data, meta_blob_data, netflix_blob_data, nvidia_blob_data = display_predefined_files_from_azure (container_client, container_name)
    return amazon_blob_data, apple_blob_data, google_blob_data, meta_blob_data, netflix_blob_data, nvidia_blob_data