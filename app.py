import gradio as gr
from gradio_pdf import PDF
from extract_multimodal_data import extracted_multimodal_data
from highlight_extracted_data import get_text_coordinates, base64_to_image, highlight_text
from list_azure_directories_blobs import display_predefined_files_from_azure, bytes_to_pdf, fetch_predefined_files
import time
from azure.storage.blob import BlobServiceClient

css = "styles.css"

def run_analysis(file, highlight):
    text, table_chart, image_base64_list,image_content_location, json_data, time_taken_for_processing = extracted_multimodal_data(file)
    start_time = time.time()
    coordinates = get_text_coordinates(file, text)

    #Convert base64 to PIL images
    images = [base64_to_image(base64_str) for base64_str in image_base64_list]
    if highlight:
        highlighted_pdf_path = highlight_text(file, coordinates, image_content_location)
        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) 
        elapsed_time_ms_rounded_highlighted = round(elapsed_time_ms, 2) 
    else:
        highlighted_pdf_path = file
        elapsed_time_ms_rounded_highlighted = 0

    cost= time_taken_for_processing * 0.0011 * 5
    tooltip_content = f"""
    <span class="tooltip">
         Cost Calculation (running on 5 A100's):<br>
        - Cost per A100 GPU: $4 for 3600(s)<br>
        - Cost per second:$4/3600 = $0.0011<br>
        - Total time processed: {time_taken_for_processing:.2f} (s) <br>
        - Total cost: {time_taken_for_processing} (s) * 0.0011 * 5 = ${cost:.2f}
    </span>
"""
    cost_with_tooltip = f"""<span class="cost">**Cost for extracting:** ${cost:.2f}  {tooltip_content} </span>"""
    
    return highlighted_pdf_path, text, table_chart, images, json_data, f"**Time taken for extracting:** {time_taken_for_processing:.2f} (s)", f"**Time taken for highlighting:** {elapsed_time_ms_rounded_highlighted:.2f} (s)", cost_with_tooltip

with gr.Blocks(css = css) as demo:
    gr.Markdown("""<div style="font-size: 36px; font-weight: bold; color: #76B900; text-align: center; margin-bottom: 20px;"> NVIDIA-INGEST: MULTI-MODAL DATA EXTRACTION</div>""")
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload PDF File", elem_id="small-file-input", interactive=True)
            gr.Markdown("""<div style="font-size: 24px; text-align: center;"> Select a Earning Report </div>""")
            amazon_blob_data, apple_blob_data, google_blob_data, meta_blob_data, netflix_blob_data, nvidia_blob_data = fetch_predefined_files()
            predefined_files = {
                    "Amazon Earnings": amazon_blob_data,
                    "Apple Earnings": apple_blob_data,
                    "Google Earnings": google_blob_data,
                    "Meta Earnings":meta_blob_data,
                    "Netflix Earnings": netflix_blob_data,
                    "NVIDIA Earnings": nvidia_blob_data
                }
        
            predefined_buttons = []
            btn_actions = []
            for file_name, blob_data in predefined_files.items():
                btn = gr.Button(file_name, variant="secondary")
                predefined_buttons.append(btn)
                 # Store click action for later
                btn_actions.append((btn, blob_data))

        with gr.Column(scale=4):
            bt_analysis = gr.Button("Run analysis")
            with gr.Row():
                time_taken_for_processing = gr.Markdown()
                cost_processing = gr.Markdown()
            time_taken_for_highlighting = gr.Markdown()
            bounding_box_toggle = gr.Checkbox(label="Highlight Extracted Data")
            pdf_viewer = PDF(label="Extract Multimodal Data",  interactive=True, elem_id="pdf_viewer")


        with gr.Column(scale=4):
            with gr.Tab("Content"):
                text_content = gr.Textbox(label="Text", value="")
                table_chart_content = gr.Textbox(label="Tables", value="")
                image_gallery = gr.Gallery(label="Charts & Image",elem_id="gallery",columns=[3], rows=[1], object_fit="contain", height="auto")
            with gr.Tab("Result"):
                json_display = gr.JSON()
        
   
        # Link the file input to the pdf_viewer
        file_input.change(lambda file: file.name if file else None, inputs=file_input, outputs=pdf_viewer)

        for btn, blob_data in btn_actions:
            btn.click(lambda blob_data=blob_data: bytes_to_pdf(blob_data), inputs=None, outputs=pdf_viewer)

        
        bt_analysis.click(run_analysis, inputs = [pdf_viewer, bounding_box_toggle], outputs =[pdf_viewer, text_content, table_chart_content, image_gallery, json_display, time_taken_for_processing, time_taken_for_highlighting, cost_processing])
       

demo.launch(share=True)
