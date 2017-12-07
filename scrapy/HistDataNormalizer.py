import os
import json
import zipfile

class HistDataNormalizer:

    base_file_dir = 'spider/output/'
    base_target_dir = 'output/' #TODO later change to ../resources/prices

    def run(self):
        pass
        #TODO merge csv files https://stackoverflow.com/questions/2512386/how-to-merge-200-csv-files-in-python


normalizer = HistDataNormalizer()
normalizer.run()
