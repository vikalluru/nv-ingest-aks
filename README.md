# Running NVIDIA Ingest-Multimodal Data Extraction on Azure Kubernetes Service(AKS) 
This project demonstrates how to deploy NVIDIA Ingest on AKS and test the service with either predefined annual earnings PDFs, or by uploading your own PDF file.
## Deploying NVIDIA Ingest on AKS
- Follow the 'prerequisites' and 'create AKS' sections from the [nim-deploy repository](https://github.com/NVIDIA/nim-deploy/tree/main/cloud-service-providers/azure/aks)
- Note that before creating AKS, you should check the number of nodes required in the [values.yaml](https://github.com/NVIDIA/nv-ingest/blob/main/helm/values.yaml) file of the Helm chart in nv-ingest 
- Follow the steps [here](https://github.com/NVIDIA/nv-ingest/tree/main/helm) to create the namespace and run the Helm install command by providing the correct NGC_API_KEY.
- Once the Helm install command is completed and you see all the services up and running, similar to the screenshot below, your nv-ingest microservice has been deployed successfully.
  ![nv-ingest-service-on-aks](https://github.com/user-attachments/assets/88f6d85d-5ac0-4b86-a9bf-9752172b8944)
- To access the service, first install the nv-ingest client by following the instructions [here](https://github.com/NVIDIA/nv-ingest/tree/main/client)
- After successfully installing the nv-ingest client, run the following CLI command to test multimodal PDF extraction, or you can also run it using the Python client based on the example [here](https://github.com/NVIDIA/nv-ingest/blob/main/client/client_examples/examples/python_client_usage.ipynb). 
```
  nv-ingest-cli \
        --doc /path/to/your/unique.pdf \
        --output_directory ./path/to/your/output_foler \
        --task='extract:{"document_type": "pdf", "extract_text": true, "extract_images": true, "extract_tables": true}' \
        --client_host=localhost \
        --client_port=6379
```
- Edit the nv-ingest-redis-master service to change its type to LoadBalancer in order to access the service from outside the AKS cluster.
    - Use kubectl edit svc ``` nv-ingest-redis-master``` and change type from ‘ClusterIP’ to ‘LoadBalancer’

### Testing NVIDIA Ingest with Your PDF File
The demo app allows you to upload your PDF file and run an analysis, or you can use one of the predefined earnings files to do analysis.

![demo_GUI](https://github.com/user-attachments/assets/dec7fbfb-4589-4a68-8d26-d34762a04d4d)

There are three key functionalities in the demo application:
- You can upload a custom PDF file or use one of the earnings reports fetched from Azure Blob Storage.
- Run the analysis to see the time and cost taken for extraction, as well as the time taken to highlight the extracted text in the PDF.
- The extracted multimodal data will be displayed in the ‘Content’ section, while the response will be shown in JSON format in the ‘Results’ section.

Below are the steps to run the demo application, along with more key steps explained later:
- Clone the repository.
- Install the necessary packages listed in requirements.txt.
- Install the nv-ingest client by following the instructions [here](https://github.com/NVIDIA/nv-ingest/tree/main/client).
- Run ```‘python3 app.py’```.

### PDF Files from Azure Blob Storage
The predefined earnings files are retrieved from Azure Blob Storage. Following are the steps to upload and retrieve files from Azure Blob Storage for any of your use cases:
- Install Azure Blob Storage using the following command
    ``` pip install azure-storage-blob```
- Define your connection string, container name and create the container if it doesn’t exist
  ```
    connection_string = ""
    container_name = ""
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
  ```
- Upload PDFs/blob to the container
  ```
    blob_client = container_client.get_blob_client(‘your_blob file_name’)
    with open("./sample.txt", "rb") as data:
        blob.upload_blob(data)
  ```
- Download PDF”s/blob from the container
  ``` 
    with open(‘filename_to_save’, "wb") as f:
        data= container_client.get_blob_client("your_blob_file_name").download_blob().readall()
        f.write(data)
  ```

### Time and Cost Analysis

After uploading or selecting the PDF file, you have two options: you can either select ‘Highlight Extracted Data’ or click on ‘Run Analysis’ without selecting the checkbox.
You can see screenshots for both options, along with helpful insights such as the time taken and cost for extracting multimodal data.

The nv-ingest service is running on five A100 GPUs, and the cost is calculated as follows:
```
- Cost per A100 GPU = $4 for 3600(s)
- Cost per second:$4/3600 = $0.0011
- Total cost = time_taken_for_processing (s) * 0.0011 * 5
```
**Without selecting 'Highlight Extracted Data' checkbox**
![without_selecting_checkbox](https://github.com/user-attachments/assets/80ba97b5-822c-4679-8eee-161594a36994)

**With selecting 'Highlight Extracted Data' checkbox**
![with_selecting_checkbox](https://github.com/user-attachments/assets/319eaaef-0523-47b7-a21b-8cff75c2df27)

You can view the extracted text, tables, charts, and images separately in the ‘Content’ tab, along with the response in JSON format in the ‘Result’ section.

