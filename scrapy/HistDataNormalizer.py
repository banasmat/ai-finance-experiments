import re
import os


class HistDataNormalizer:

    base_file_dir = 'output/'
    base_target_dir = '../resources/prices/'

    def merge_price_files(self):

        pattern = re.compile('^DAT_MT_(\w+)_M1_.+?\.csv$')

        for filename in os.listdir(self.base_file_dir):
            result = pattern.search(filename)
            if result is not None:
                output_path = self.base_target_dir + result.group(1) + '.csv'

                source_file = open(self.base_file_dir + filename, 'r')

                if os.path.isfile(output_path):
                    mode = 'a'
                else:
                    mode = 'w'
                    # next(source_file) no headers in these files

                output_file = open(output_path, mode)

                for line in source_file:
                    output_file.write(line)

                source_file.close()
                output_file.close()

normalizer = HistDataNormalizer()
normalizer.merge_price_files()
