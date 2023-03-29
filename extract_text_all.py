# Purpose:  This script is to whole extract text from a PDF file

import os
import numpy as np
import pypdfium2 as pdfium
from nltk.tokenize import sent_tokenize

class PDF_to_Text:
    """This class is to extract text from a PDF file.
    """
    
    def __init__(self):
        """Initiate the class.
        """
        # get current working directory
        parent_dir = os.path.abspath(os.getcwd())

        parent_dir += "/" 

        file_name = [i for i in os.listdir(parent_dir) if i.endswith(".pdf")][0]
        
        self.parent_dir = parent_dir
        self.file_name = file_name
    
    def create_directory(self):
        """This function is to create a directory in the parent_dir.
        """
        try:
            # Directory
            directory = "before"
            # Path
            path = os.path.join(self.parent_dir, directory)
            
            path += '/'
            
            # it has to put it here or os.mkdir will return None and
            # the self.path = path will not work
            self.path = path
            # print(self.path)
            
            # create a directory called 'before' under the parent_dir:
            os.mkdir(self.path)
        
        except FileExistsError:
            pass
        
     
    def read_pdf(self):
        """This funciton is to read a PDF file.

        Returns
        -------
        PdfDocument
            the PDF document read from pdfium
        """
        try:
            file = self.parent_dir + self.file_name
            pdf = pdfium.PdfDocument(file)
            
            self.pdf = pdf
            
            return self.pdf
        
        except Exception as err:
            print(err)
    
    def get_txt(self):
        """This function is to extract the text from a PDF file.

        Returns
        -------
        dictionary
            A dictionary with page number as the key and the text content as 
            the value.
        """
        try:
            n_pages = len(self.pdf)  # get the number of pages in the document
            page_indices = [i for i in range(n_pages)]  # all pages
            
            # use the first page size as a standard size
            page_size = pdfium.PdfPage(self.pdf[0], self.pdf).get_size()
            width = page_size[0]
            height = page_size[1]
            
            # extract the text page by page
            articles = dict()
            for i in page_indices:
                page = self.pdf[i]
                # Load a text page helper
                textpage = page.get_textpage()
                # get all text in a page:
                text_all = textpage.get_text_range()
                key_name = f"page_{i}"
                articles[key_name] = text_all
            
            self.articles = articles
            
            return self.articles
        
        except Exception as err:
            print(err)
    
    def save_text(self, page_num, idx, doc):
        """This function is to save each paragraph as a txt file.

        Parameters
        ----------
        page_num : str
            the page number where this paragraph is from
        idx : int
            the number of the paragraph in a page
        doc : str
            the paragraph
        
        Returns
        ----------
        str
            the path for storing these paragraph txt files
        """
        try:
            location = f"{self.path}{page_num}_{idx}.txt"
            with open(location, 'w') as f:
                f.write(doc)
            
            return self.path
        except Exception as err:
            print(err)
        
    
    def get_paragraph(self, text, page_num):
        """This function is to break the text contents into paragraph levels.

        Parameters
        ----------
        text : str
            the text contents of a page
        page_num : str
            the page number in a dictionary

        Returns
        -------
        str
            a paragraph
        """
        try:
            # remove "." in Fig. or fig. in the sentences cause it will affect splitting paragraphs
            # and this will affect ChatGPT translation performance
            if ("Fig." in text):
                text = text.replace("Fig.", 'Fig')
            if ("fig." in text):
                text = text.replace("fig.", "fig")
            # check if '\x02' is in the text, if it is, using '-' to join the words
            if ("\x02" in text):
                text = text.replace("\x02", "-")
            # check if '\x00' is in the text, if it is, using " " to replace the words
            if ("\x00" in text):
                text = text.replace("\x00", " ")   
            splitted_docs = text.split("\r\n")
            
            # replace "\r\n" with blank:
            splitted_docs = text.split("\r\n")
            joined_doc = " ".join(splitted_docs)
            
            # Using NLTK to tokenize a document into sentences level:
            t_sent = sent_tokenize(joined_doc)
            
        
            # get every 5 sentences as a paragraph:
            end = end = int((np.ceil(len(t_sent) / 5)) * 5)
            multiples_5 = np.arange(0, end , 5)

            # get the paragraph and save it in a text file:
            for idx, i in enumerate(multiples_5):
                first_idx = i
                last_idx = i + 5
                if first_idx != multiples_5[-1]:
                    doc = " ".join(t_sent[first_idx:last_idx])
                    # save text:
                    self.path = self.save_text(page_num, idx, doc)

                else:
                    doc = " ".join(t_sent[i:])
                    # save text:
                    self.path = self.save_text(page_num, idx, doc) 
            
            return doc, self.path
        
        except Exception as err:
            print(err)
    

    def iterate(self):
        """This function is to iterate each page content and save each paragraph
        as a text file.

        Parameters
        ----------

        Returns
        -------
        str
            the last paragraph in the last page & the path for storing these \
            paragraph txt files
        """
        try:
            # get paragraphs in each of pages:
            for k, v in self.articles.items():
                doc, self.path  = self.get_paragraph(v, k)
                
            print(f"finishing extracting paper {self.file_name}\n\n")
            return doc
        
        except Exception as err:
            print(err)

