# This script is to make an API call and ask ChatGPT 3.5 to translate

import os
import time
import openai
import api_key # this is your API key
import numpy as np
import pandas as pd
from tqdm import tqdm

class Translator:
    """This class is to use ChatGPT 3.5 to translate English to Traditional Chinese.
    """
    
    def __init__(self, path, language):
        """Initiate the class

        Parameters
        ----------
        path : str
            the path where the text files for translation locate
        language : str
            the language you want ChatGPT to translate into
        """
        # checking if it is Mac or Windows file path
        if '/' in path:
            path = path + '/'
        else:
            path = path + '\\'
        
        parent_dir = path.split("before")[0]
        
        # get api key:
        key = api_key.api_key
        
        self.path = path
        self.parent_dir = parent_dir
        self.key = key
        self.language = language
    
    def create_directory(self):
        """This function is to create a directory in the parent_dir.
        """
        try:
            # Directory
            directory = "log"
            
            new_parent_dir = self.parent_dir + 'after'
            
            # Path
            log_path = os.path.join(new_parent_dir, directory)
            
            # checking if it is Mac or Windows file path
            if '/' in self.parent_dir:
                log_path = log_path + '/'
            else:
                log_path = log_path + '\\'
            
            # it has to put it here or os.mkdir will return None and
            # the self.new_path = new_path will not work
            save_translation_path = log_path.split("log")[0]
            
            self.log_path = log_path
            self.save_translation_path = save_translation_path
            # print(self.path)
            
            # create a directory called 'after' under the parent_dir:
            # this directory is to save the translation result
            os.makedirs(self.log_path, exist_ok = True)
        
        except FileExistsError:
            pass  
    
    def get_metadata(self, before = True):
        """This function is to get the metadata about the txt files for translation.
        
        Parameters
        ----------
        before : bool, optional
            if it is True, we will get the metadata from 'before' directory, by default True
            
        Returns
        -------
        Pandas Dataframe
            the metadata of the given path
        """
        try:
            if before == True:
                file_lst = os.listdir(self.path)
            else:
                file_lst = os.listdir(self.save_translation_path)
            
            file_lst = [ i for i in file_lst if (i.endswith('.txt')) & (i.startswith('page'))]
            # print(file_lst)
            metadata = pd.DataFrame(file_lst, columns = ['file_name'])
            
            # get page number:
            metadata['page_num'] = metadata.file_name.map(lambda x: x.split('_')[1])
            # get paragraph number:
            if before == True:
                metadata['paragraph_num'] = metadata.file_name.map(lambda x: x.split("_")[-1].split('.')[0])
            else:
                metadata['paragraph_num'] = metadata.file_name.map(lambda x: x.split("_")[2])
                
            #change dtype:
            num_col = ['page_num', 'paragraph_num']

            for i in num_col:
                metadata[i] = pd.to_numeric(metadata[i])
            
            # get the paragraph sequence:
            metadata.sort_values(by = ['page_num', 'paragraph_num'], inplace=True) 
            # reset index:
            metadata.reset_index(drop=True, inplace=True)
            
            self.metadata = metadata
            
            return self.metadata
        
        except Exception as err:
            print(err)
    
    def read_txt_file(self, fname, before = True):
        """This function is to read a text file for translation.

        Parameters
        ----------
        fname : str
            the text file for translation
        before : bool, optional
            if it is True, we will get the metadata from 'before' directory, by default True
            
        Returns
        -------
        str
            the paragraph for translation
        """
        try:
            if before == True:
                location = self.path + fname
            else:
                location = self.save_translation_path + fname
            with open(location, 'r') as f:
                doc = f.read()
            
            return doc
        
        except Exception as err:
            print(err)

    def translate(self, text):
        """This function is to make an API call to let ChatGPT 3.5 translate the
        paragraph.

        Parameters
        ----------
        text : str
            the paragraph for translation

        Returns
        -------
        OpenAIObject, JSON
            the return log and translation results from API call Chat Completion
        """
        try:
            openai.api_key = self.key
            
            completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {'role': 'user',
                            'content': f"Please translate the text from \
                                English to {self.language},\
                                and return only translated text, \
                                not include the origin text,\
                                here is the text: {text}"
                            }
                                ],
                        temperature=0.2,
                        max_tokens=1024,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                        )
            return completion
        
        except Exception as err:
            print(err)

    def get_translation(self, result, original_filename):
        """This function is to save the log and extract the translation text.

        Parameters
        ----------
        result : OpenAIObject, JSON
            the return log and translation results from API call Chat Completion
        original_filename : str
            the orignal text file for translation

        Returns
        -------
        Pandas Dataframe, str
            the df with API log and the translation text
        """
        try:
            # save the log:
            df = pd.json_normalize(result)
            # get the translation:
            translation_content = result["choices"][0]["message"]["content"].strip()
            # print("finishing translation_content")
            
            # save the translation content:
            fname = original_filename.split(".")[0]
            location = f"{self.save_translation_path}{fname}_translation.txt"
            
            with open(location, 'w') as f:
                f.write(translation_content)
            
            return df, translation_content
        
        except Exception as err:
            print(err)
    
    def iterate(self):
        """This function is to iterate all the text files and make API call to 
        let ChatGPT translate the text into Traditional Chinese.

        Returns
        -------
        Pandas Dataframe, str
            the df with API log and the translation text
        """
        try:
            for i in tqdm(range(len(self.metadata))[:2]):
                
                time.sleep(3)
                fname = self.metadata['file_name'].iloc[i]
                # read paragraph:
                doc = self.read_txt_file(fname)
                # API call ChatGPT to translate:
                result = self.translate(doc)
                # print("finishing translation")
                
                # get translation results:
                df_log, translation_content = self.get_translation(result, fname)
                
                # save df_log:
                log_fname = fname.split('.')[0]
                location = f"{self.log_path}{log_fname}_log.csv"
                df_log.to_csv(location, index = False)
            
            return df_log, translation_content
            # return doc
        
        except Exception as err:
            print(err)
    
    # merging all the translation result into 1 text file:
    
    def check_page_num(self):
        """This function is to check if the next paragraph is within the same page.

        Returns
        -------
        Pandas Dataframe
            The metadata with check_same_page column
        """
        try:
            t_metadata = self.get_metadata(before=False)
            
            t_metadata['check_same_page'] = np.nan
            for i in range(len(t_metadata)):
                try:
                    page_num = t_metadata['page_num'].iloc[i]
                    next_item_page_num = t_metadata['page_num'].iloc[i+1]
                    if page_num == next_item_page_num:
                        # t_metadata['check_same_page'].iloc[i] = True
                        t_metadata.loc[i, 'check_same_page'] = True
                    else:
                        # t_metadata['check_same_page'].iloc[i] = False
                        t_metadata.loc[i, 'check_same_page'] = False
                except IndexError:
                    # t_metadata['check_same_page'].iloc[i] = True
                    t_metadata.loc[i, 'check_same_page'] = True
            
            self.t_metadata = t_metadata
                
            return self.t_metadata
        
        except Exception as err:
            print(err)
    
    def merge_files(self):
        """This function is to merge all the translated text files into 1 text file.

        Returns
        -------
        str
            the merged translated paragraph 
        """
        try:
            self.t_metadata = self.check_page_num()
            
            lang_translation = ""

            for i in range(len(self.t_metadata['file_name'])):
                
                fname = self.t_metadata['file_name'].iloc[i]
                same_page = self.t_metadata['check_same_page'].iloc[i]
                # read the translation result:
                doc = self.read_txt_file(fname, before=False)
        
                # break lines
                doc = doc.replace("。", "。\n")
                
                if same_page == True:
                    lang_translation += doc + "\n"
                else:
                    lang_translation += doc + "\n\n"
            
            # save the result:
            location = f"{self.save_translation_path}merge_translation.txt"     
            with open(location, 'w') as f:
                f.write(lang_translation)
            
            return lang_translation
        
        except Exception as err:
            print(err)
    
    def price_calculation(self):
        """This function is to calculate the cumulated price for the API call per PDF file.

        Returns
        -------
        int
            the total tokens, includes input and the completion (output) texts.
        """
        try:
            file_lst = os.listdir(self.log_path)
            file_lst = [i for i in file_lst if (i.endswith('.csv') & (i.startswith('page')))]
            
            df_price = pd.DataFrame()

            for i in file_lst:
                location = self.log_path + i
                df_1 = pd.read_csv(location)
                df_price = pd.concat([df_price, df_1])
            
            # total tokens for this API call:
            total_tokens = df_price['usage.total_tokens'].sum()
            price = (total_tokens/1000) * 0.002
            
            print(f"\nHere is the summary of cost for this API call:")
            print(f"total tokens: {total_tokens}, price: ${price} (US)")  
            
            return total_tokens
              
        except Exception as err:
            print(err)
