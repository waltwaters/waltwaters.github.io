import fitz  # PyMuPDF
from PIL import Image
import os

def pdf_to_images_side_by_side(pdf_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    num_pages = pdf_document.page_count

    for i in range(0, num_pages, 2):
        # Get the first page
        page1 = pdf_document.load_page(i)
        pix1 = page1.get_pixmap()

        # Create an image from the first page
        img1 = Image.frombytes("RGB", [pix1.width, pix1.height], pix1.samples)

        if i + 1 < num_pages:
            # Get the second page if it exists
            page2 = pdf_document.load_page(i + 1)
            pix2 = page2.get_pixmap()

            # Create an image from the second page
            img2 = Image.frombytes("RGB", [pix2.width, pix2.height], pix2.samples)

            # Create a new image with width = sum of both pages' widths
            combined_img = Image.new("RGB", (img1.width + img2.width, img1.height))
            combined_img.paste(img1, (0, 0))
            combined_img.paste(img2, (img1.width, 0))
        else:
            # If there is no second page, use only the first page
            combined_img = img1

        # Save the combined image
        combined_img.save(f"{output_folder}/page_{i // 2 + 1}.png")

# Example usage
pdf_path = "Walt_awards_6pages_eng copy_compressed.pdf"
output_folder = "output_images"
pdf_to_images_side_by_side(pdf_path, output_folder)