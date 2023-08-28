import unittest
import os
from pdf.loader import load_pdf_local

class LoaderTest(unittest.TestCase):
    def test_loader_local_pdf(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "example_data", "sample.pdf")
        content = load_pdf_local(pdf_path)
        ## TODO: need to find a way to access document object
        self.assertEqual(str(content['page_content']), "page_content='A Simple PDF File \n This is a small demonstration .pdf file - \n just for use in the Virtual Mechanics tutorials. More text. And more \n text. And more text. And more text. And more text. \n And more text. And more text. And more text. And more text. And more \n text. And more text. Boring, zzzzz. And more text. And more text. And \n more text. And more text. And more text. And more text. And more text. \n And more text. And more text. \n And more text. And more text. And more text. And more text. And more \n text. And more text. And more text. Even more. Continued on page 2 ...' metadata={'source': 'example_data/sample.pdf', 'page': 0}")


if __name__ == '__main__':
    unittest.main()
