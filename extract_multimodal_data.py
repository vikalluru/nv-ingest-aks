from nv_ingest_client.client import NvIngestClient
from nv_ingest_client.primitives import JobSpec
from nv_ingest_client.primitives.tasks import ExtractTask
from nv_ingest_client.primitives.tasks import SplitTask
from nv_ingest_client.util.file_processing.extract import extract_file_content
# from azure.storage.blob import BlobServiceClient
from langchain_core.documents import Document
import json

import logging, time
import os


def process_pdf_file(file_path):
    logger = logging.getLogger("nv_ingest_client")
    client = NvIngestClient(message_client_hostname="localhost", message_client_port=6379)
    
    start_time = time.time()

    file_name = file_path
    file_content, file_type = extract_file_content(file_name) 
    

    job_spec = JobSpec(
    document_type=file_type,
    payload=file_content,
    source_id=file_name,
    source_name=file_name,
    extended_options={"tracing_options": {"trace": True, "ts_send": time.time_ns()}},
)

    extract_task = ExtractTask(
        document_type=file_type,
        extract_text=True,
        extract_images=True,
        extract_tables=True,
    )
    
    
    job_spec.add_task(extract_task)
    job_id = client.add_job(job_spec)
    
    client.submit_job(job_id, "morpheus_task_queue")
    result = client.fetch_job_result(job_id, timeout=60)

    #Compute the time taken to process each PDF file
    end_time = time.time()
    elapsed_time_ms = (end_time - start_time) 
    elapsed_time_ms_rounded = round(elapsed_time_ms, 2) 

    return result, elapsed_time_ms_rounded

# check the length of the resulted list and check the type always to see how to extract the content on a single 
def extracted_multimodal_data(filepath):
    result, time_taken =process_pdf_file(filepath)
    text_content = []
    # chart_content = []
    # table_content = []
    table_chart_content=[]
    image_content = []
    image_content_location_by_page ={}
    # text_content_location= []
    # table_locations ={}
    contenttext = ""

    # print(result)
    for element in result[0]:  
        if element['document_type'] == 'text':
            text_content.append(Document(element['metadata']['content']))
            contenttext = contenttext + Document(element['metadata']['content']).page_content 
            # text_content_location.append(element['metadata']['text_metadata']['text_location'])
        elif element['document_type'] == 'structured':
            # page_number = element['metadata']['content_metadata']['hierarchy']['page']
            # table_locations[page_number] = []
            # table_locations[page_number].append(element['metadata']['table_metadata']['table_location'])
            table_chart_content.append(Document(element['metadata']['table_metadata']['table_content']))
                # table_chart_content.append("SEP_TOKEN")
        elif element['document_type'] == 'image':
            image_content.append(Document(element['metadata']['content']).page_content)
            # print(element['metadata']['image_metadata'])
            page_number = element['metadata']['content_metadata']['hierarchy']['page']
            image_content_location_by_page[page_number] = []
            image_content_location_by_page[page_number].append(element['metadata']['image_metadata']['image_location'])
    json_data = json.dumps(result)


    # Update the tabs with the generated content
    return contenttext, table_chart_content, image_content, image_content_location_by_page, json_data, time_taken
