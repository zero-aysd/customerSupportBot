import markdown2
from weasyprint import HTML

def convert_md_to_pdf(md_path: str, pdf_path: str):
    # Read markdown content
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Convert markdown to HTML
    html_text = markdown2.markdown(md_text, extras=["fenced-code-blocks", "tables"])

    # Convert HTML to PDF using WeasyPrint
    HTML(string=html_text).write_pdf(pdf_path)

if __name__ == '__main__':
    convert_md_to_pdf('PROJECT_DOCUMENTATION.md', 'PROJECT_DOCUMENTATION.pdf')