import aspose.pdf as ap

input_html = "index.html"
output_pdf = "output.pdf"

# create HtmlLoadOptions object
options = ap.HtmlLoadOptions()

# load file
document = ap.Document(input_html, options)

# convert HTML to PDF
document.save(output_pdf)