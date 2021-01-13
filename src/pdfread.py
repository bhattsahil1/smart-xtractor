from pdfminer.layout import LAParams, LTTextBox, LTImage, LTFigure
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
import fitz
import io
from PIL import Image
import tabula
import camelot
import sys


file = sys.argv[1]

##Function to extract text
def get_text():
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    with open("text/output.txt", "w") as text_file:
        text_file.write(text)

##Function to extract tables
def get_tables():
    # tables = camelot.read_pdf(file, pages = "1-end")
    # tables.export("tables/output_tables.csv", f = "csv")
    tabula.convert_into(file,"tables/output.csv",output_format='csv',pages='all')


def get_images():
    doc = fitz.open(file)
    img_count = 0
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            img_count+=1
            base_image = doc.extractImage(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # save it to local disk
            image.save(open(f"images/image{img_count}.{image_ext}", "wb"))

# print("Extracting Images...")
# get_images()
print("Extracting Tables...")
get_tables()
# print("Extracting Text...")
# get_text()r