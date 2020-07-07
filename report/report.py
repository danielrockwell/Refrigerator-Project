'''The report script creates a PDF report of both
    openGrpah and tempGraph images with formatting.

    This code is from fpdf documentation:
    https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html'''
from fpdf import FPDF
from datetime import date,timedelta

yesterday = date.today() - timedelta(days=1)
weekAgo = date.today() - timedelta(days=7)

class PDF(FPDF):
    # Creates the PDF Header
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(20)
        self.cell(30, 10, f'Refrigerator Statistics for the Week of {weekAgo.strftime("%m/%d/%Y")} - {yesterday.strftime("%m/%d/%Y")}')
        self.ln(10)

    # Creates the PDF Footer
    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 8)
        self.cell(0,10,*NAME*)
        self.ln(3)
        self.cell(0, 10, *COURSE*)
        self.ln(3)
        self.cell(0, 10, *DESCRIPTION*)


pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Times', '', 12)
pdf.cell(3)

# Inserts both graph png images in the PDF
pdf.image(f"images/openGraph_{date.today().strftime('%Y_%m_%d')}.png",w=190,h=127)
pdf.image(f"images/tempGraph_{date.today().strftime('%Y_%m_%d')}.png",w=190,h=127)

# Saves PDF into the reports directory
pdf.output(f'reports/refrigeratordash_{date.today().strftime("%Y_%m_%d")}.pdf', 'F')
