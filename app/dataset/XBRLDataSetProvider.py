from typing import List, Tuple

import numpy as np
import pandas as pd
import os
import pickle
import csv
from fuzzywuzzy import process
import app.dataset.xbrl_titles as xbrl_titles


class XBRLDataSetProvider(object):


    @staticmethod
    def extract_cik_numbers():
        res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')

        cik_map = {}

        for quarter_dir in reversed(os.listdir(res_dir)):

            quarter_dir = os.path.join(res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            sub_file = os.path.join(quarter_dir, 'sub.txt')
            subs = pd.read_csv(sub_file, sep='\t', encoding='ISO-8859-1', usecols=['cik', 'name'])

            for index, row in subs.iterrows():
                cik_map[row['cik']] = row['name']

        cik_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'cik.pkl')

        with open(cik_file_path, 'wb') as f:
            pickle.dump(cik_map, f)

    @staticmethod
    def organize_tags():
        res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')
        all_tags = pd.Series()

        for quarter_dir in reversed(os.listdir(res_dir)):

            quarter_dir = os.path.join(res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            tag_file = os.path.join(quarter_dir, 'tag.txt')
            tags = pd.read_csv(tag_file, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, usecols=['tag'])
            all_tags = all_tags.append(tags)

        all_tags = all_tags['tag'].unique().tolist()

        # target_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'tags.txt')
        #
        # with open(target_file_path, 'a') as f:
        #     for item in all_tags:
        #         f.write("%s\n" % item)

        target_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'tags_organized.txt')

        for title in xbrl_titles.titles.keys():

            title = title.replace('&', 'and')

            result = process.extract(title, all_tags, limit=15)
            with open(target_file_path, 'a') as f:
                f.write("\n%s:\n" % title)
                for item in result:
                    f.write("%s - %s\n" % (item[0], str(item[1])))

    @staticmethod
    def organize_data_set(dir_separator='\\'):

        res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')
        output_dir = os.path.join(os.path.abspath(os.getcwd()), 'output', 'xbrl_organized')

        # all_quarters = os.listdir(res_dir)
        # all_quarters.remove('.gitignore')
        #
        # all_ciks = []
        #
        # for quarter_dir in os.listdir(res_dir):
        #
        #     quarter_dir = os.path.join(res_dir, quarter_dir)
        #
        #     if not os.path.isdir(quarter_dir):
        #         continue
        #
        #     sub_file = os.path.join(quarter_dir, 'sub.txt')
        #     subs = pd.read_csv(sub_file, sep='\t', encoding='ISO-8859-1', usecols=['cik'])
        #     all_ciks = all_ciks + subs['cik'].tolist()
        #
        # all_ciks = set(all_ciks)

        # all_data = np.empty((len(all_quarters), ))
        # index = pd.MultiIndex.from_product([all_quarters, all_ciks], names=['quarter', 'cik'])
        # all_data = pd.DataFrame(index=index, columns=xbrl_titles.titles.keys())
        pd.options.mode.chained_assignment = None

        for quarter_dir in os.listdir(res_dir):

            quarter_dir = os.path.join(res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            quarter_name = quarter_dir.rsplit(dir_separator, 1)[-1]
            target_file_path = os.path.join(output_dir, quarter_name + '.csv')
            if os.path.exists(target_file_path):
                continue

            print('QUARTER', quarter_name)

            num_file = os.path.join(quarter_dir, 'num.txt')
            sub_file = os.path.join(quarter_dir, 'sub.txt')

            numbers = pd.read_csv(num_file, sep='\t', encoding='ISO-8859-1', usecols=['adsh', 'tag', 'value'])
            subs = pd.read_csv(sub_file, sep='\t', encoding='ISO-8859-1', usecols=['adsh', 'cik', 'name'])
            #
            df = pd.DataFrame(index=subs['cik'], columns=xbrl_titles.titles.keys())
            df.fillna(0, inplace=True)
            numbers = numbers.merge(subs, on='adsh', how='left')

            # i = 0

            for i, cik in subs['cik'].iteritems():
                # print('CIK', cik)
                for fixed_tag, tags in xbrl_titles.titles.items():
                    val = 0
                    for tag in tags:
                        try:
                            val = numbers.loc[(numbers['cik'] == cik) & (numbers['tag'] == tag)]['value'].mean()

                            if np.isnan(val):
                                continue
                            else:
                                break
                        except KeyError:
                            continue

                    if not np.isnan(val):
                        df[fixed_tag].loc[df.index == cik] = val
                    #
                    # all_data.loc[(all_data.index.get_level_values('quarter') == quarter_name)
                    #              & (all_data.index.get_level_values('cik') == cik), fixed_tag] = val

                # break

            with open(target_file_path, 'w') as f:
                df.to_csv(f)
            # break

        # all_data.fillna(0, inplace=True)

        # tensor = all_data.values.reshape((len(all_quarters), len(all_ciks), all_data.shape[1]))
        # np.save(os.path.join(output_dir, 'xbrl_data'), tensor)
