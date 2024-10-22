import fitz  # PyMuPDF
import gradio as gr
from io import BytesIO
import io
import base64
from PIL import Image



def highlight_text(pdf_path, highlights, image_coordinates):
    # Open the original PDF
    pdf_document = fitz.open(pdf_path)

    # Create a new PDF for highlights
    output_path = "highlighted_output.pdf"
    new_pdf_document = fitz.open()
    
    # Process each page in the original PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        new_page = new_pdf_document.new_page(width=page.rect.width, height=page.rect.height)
        
        # Draw the original page
        new_page.show_pdf_page(page.rect, pdf_document, page_num)
        pdf_height = new_page.rect.height

        # Draw text highlights
        for bbox in highlights.get(page_num, []):
            # Highlight with a yellow rectangle
            new_page.draw_rect(bbox, color=(1, 1, 0), width=2)
        

     # Draw image bounding boxes
        if page_num in image_coordinates:
            for img_bbox in image_coordinates[page_num]:
                # Bounding box coordinates: [x0, y0, x1, y1]
                x0, y0, x1, y1 = img_bbox
                adjusted_y0 = pdf_height - y1  # Use y1 for the adjusted bottom
                adjusted_y1 = pdf_height - y0 


                # Draw a red rectangle around the image
                new_page.draw_rect([x0, adjusted_y0, x1, adjusted_y1], color=(1, 0, 0), width=2)

    # Save the highlighted PDF
    new_pdf_document.save(output_path)
    new_pdf_document.close()
    pdf_document.close()
    
    return output_path

    
def get_text_coordinates(pdf_path: str, search_text: str):
    """Search for multi-line text in a PDF and get coordinates for each line."""
    doc = fitz.open(pdf_path)
    text_coordinates = {}
    search_lines = search_text.splitlines()
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text()  # Get all text on the page
    
        # Store coordinates for the current page
        text_coordinates[page_num] = []
    
        for search_line in search_lines:
            # Ensure search text matches exactly
            bbox_list = page.search_for(search_line.strip())
            
            if bbox_list:
                text_coordinates[page_num].extend(bbox_list)
            # else:
            #     print(f"No results for '{search_line}' on page {page_num}")
    # highlight_text(pdf_path, text_coordinates)
    doc.close()

    return text_coordinates



def base64_to_image(base64_str):
    """Convert base64 string to PIL Image."""
    # Remove the base64 prefix if it exists
    if base64_str.startswith('data:image/'):
        base64_str = base64_str.split(',')[1]
    
    # Decode base64 string
    image_data = base64.b64decode(base64_str)
    
    # Create a BytesIO object and load the image
    image = Image.open(io.BytesIO(image_data))
     # Resize image to a reasonable size for display
    image = image.resize((800, 600))  # Adjust size as needed
    return image
