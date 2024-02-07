import fitz
from typing import Union

class PDFTextExtractor(object):
  def __init__(self, pdf_path: str) -> None:
    self.pdf_path = pdf_path
    self.pdf = fitz.open(pdf_path)

  def get_metadata(self) -> dict[str, Union[str, None]]:
    return self.pdf.metadata

  def get_table_of_contents(self) -> list[str]:
    return self.pdf.get_toc()

  # Extract texts
  def extract_single_page_texts(self, page_number: int) -> str:
    page = self.pdf.load_page(page_number)
    return page.get_text()

  def extract_interval_page_texts(self, interval: tuple) -> str:
    texts = ''.join([self.extract_single_page_text(page_number=page_number) for page_number in interval])
    return texts

  def extract_all_page_texts(self):
    texts = ''.join([self.extract_single_page_text(page_number=page_number) for page_number in range(self.pdf.page_count)])
    return texts

  # Extract images
  def extract_single_page_images(self, page_number: int) -> list:
    page = self.pdf.load_page(page_number)
    return page.get_images()

  def extract_interval_page_images(self, interval: tuple) -> list:
    images = [self.extract_single_page_images(page_number=page_number) for page_number in interval]
    return images

  def extract_all_page_images(self):
    images = [self.extract_single_page_images(page_number=page_number) for page_number in range(self.pdf.page_count)]
    return images

  # Extract links
  def extract_single_page_links(self, page_number: int):
    page = self.pdf.load_page(page_number)
    return page.get_links()

  def extract_interval_page_links(self, interval: tuple):
    links = [self.extract_single_page_links(page_number=page_number) for page_number in interval]
    return links
  
  def extract_all_page_links(self):
    links = [self.extract_single_page_links(page_number=page_number) for page_number in range(self.pdf.page_count)]
    return links

  # Extract annotations
  def extract_single_page_annotations(self, page_number: int):
    page = self.pdf.load_page(page_number)
    return page.annots()
  
  def extract_interval_page_annotations(self, interval: tuple):
    annotations = [self.extract_single_page_annotations(page_number=page_number) for page_number in interval]
    return annotations

  def extract_all_page_annotations(self):
    annotations = [self.extract_single_page_annotations(page_number=page_number) for page_number in range(self.pdf.page_count)]
    return annotations

  def extract_get_text_block(self):
    def flags_decomposer(flag):
      l = []
      if flag & 2 ** 0: l.append('superscript')
      if flag & 2 ** 1: l.append('italic')
      if flag & 2 ** 2: l.append('serifed')
      else: l.append('sans')
      if flag & 2 ** 3: l.append('monospaced')
      else: l.append('proportional')
      if flag & 2 ** 4: l.append('bold')

      return ', '.join(l)

    page = self.pdf.load_page(0)
    blocks = page.get_text(option='dict', flags=11, sort=True)
    for block in blocks['blocks']:
      for line in block['lines']:
        for span in line['spans']:
          print('')
          font_properties = 'Font: \'%s\' (%s), size %g, color #%06x' % (
            span['font'],
            flags_decomposer(span['flags']),
            span['size'],
            span['color'],
          )

          print('Text: \'%s\'' % (span['text']))
          print(font_properties)

  # Close the pdf file
  def close_pdf(self):
    self.pdf.close()

if __name__ == '__main__':
  pdf_path = '../assets/poster.pdf'

  extractor = PDFTextExtractor(pdf_path=pdf_path)
  metadata = extractor.get_metadata()
  extractor.extract_get_text_block()