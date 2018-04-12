from typing import List, Tuple
import random
import numpy as np
import pandas as pd
import os
import pickle
import csv
from fuzzywuzzy import process
import app.dataset.xbrl_titles as xbrl_titles


class XBRLDataSetProvider(object):
    res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')
    most_popular_tags_file_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'most_popular_tags.txt')
    common_tags_file_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'common_tags.txt')

    @staticmethod
    def extract_cik_numbers():
        cik_map = {}

        for quarter_dir in reversed(os.listdir(XBRLDataSetProvider.res_dir)):

            quarter_dir = os.path.join(XBRLDataSetProvider.res_dir, quarter_dir)

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
    def get_common_tags():
        all_tags = pd.Series()

        for quarter_dir in reversed(os.listdir(XBRLDataSetProvider.res_dir)):

            quarter_dir = os.path.join(XBRLDataSetProvider.res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue
            print(quarter_dir)
            num_file = os.path.join(quarter_dir, 'num.txt')
            tag_file = os.path.join(quarter_dir, 'tag.txt')
            numbers = pd.read_csv(num_file, sep='\t', encoding='ISO-8859-1', usecols=['tag'])
            tags = pd.read_csv(tag_file, sep='\t', encoding='ISO-8859-1', usecols=['tag', 'custom', 'abstract'], engine='python', error_bad_lines=False)
            numbers = numbers.merge(tags, on='tag', how='left')

            numbers = numbers.loc[numbers['custom'] == 0]
            numbers = numbers.loc[numbers['abstract'] == 0]
            all_tags = all_tags.append(numbers)

        all_tags = all_tags.groupby(['tag'])['tag'].count()
        all_tags = all_tags.sort_values(ascending=True)
        all_tags = all_tags.index.unique().tolist()

        with open(XBRLDataSetProvider.common_tags_file_path, 'w') as f:
            for tag in all_tags:
                f.write("%s\n" % tag)

    @staticmethod
    def get_most_popular_tags():

        all_tags = pd.Series()

        for quarter_dir in reversed(os.listdir(XBRLDataSetProvider.res_dir)):

            quarter_dir = os.path.join(XBRLDataSetProvider.res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            num_file = os.path.join(quarter_dir, 'num.txt')
            numbers = pd.read_csv(num_file, sep='\t', encoding='ISO-8859-1', usecols=['tag'])
            all_tags = all_tags.append(numbers)

        all_tags = all_tags.groupby(['tag'])['tag'].count()
        all_tags = all_tags.sort_values(ascending=True)
        all_tags = all_tags[(all_tags >= 20000)].index.unique().tolist()

        with open(XBRLDataSetProvider.most_popular_tags_file_path, 'w') as f:
            for tag in all_tags:
                f.write("%s\n" % tag)


    @staticmethod
    def prepare_data_set_with_most_popular_tags(dir_separator='\\'):
        all_tags = []
        output_dir = os.path.join(os.path.abspath(os.getcwd()), 'output', 'xbrl_most_popular_tags')
        with open(XBRLDataSetProvider.most_popular_tags_file_path, 'r') as f:
            for tag in f:
                all_tags.append(tag.strip())

        # all_tags = sorted(all_tags)
        # all_tags = all_tags[-100:]

        pd.options.mode.chained_assignment = None

        example_cik = 1459200


        for quarter_dir in reversed(os.listdir(XBRLDataSetProvider.res_dir)):

            quarter_dir = os.path.join(XBRLDataSetProvider.res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            quarter_name = quarter_dir.rsplit(dir_separator, 1)[-1]
            target_file_path = os.path.join(output_dir, quarter_name + '.csv')
            if os.path.exists(target_file_path):
                continue

            # with open(target_file_path, 'w') as f:
            #     f.write('processing')

            print('QUARTER', quarter_name)

            num_file = os.path.join(quarter_dir, 'num.txt')
            sub_file = os.path.join(quarter_dir, 'sub.txt')
            tag_file = os.path.join(quarter_dir, 'tag.txt')

            numbers = pd.read_csv(num_file, sep='\t', encoding='ISO-8859-1', usecols=['adsh', 'tag', 'value', 'qtrs', 'ddate'])
            subs = pd.read_csv(sub_file, sep='\t', encoding='ISO-8859-1', usecols=['adsh', 'cik', 'fp'])
            tags = pd.read_csv(tag_file, sep='\t', encoding='ISO-8859-1', usecols=['tag', 'iord', 'custom', 'version', 'tlabel', 'abstract'])

            numbers = numbers.merge(subs, on='adsh', how='left')
            numbers = numbers.merge(tags, on='tag', how='left')
            with open(target_file_path, 'w') as f:
                numbers = numbers.loc[(numbers.cik == example_cik)]
                quarter_year = int(quarter_name[:4])

                if(quarter_name[5:6] == '1'):
                    quarter_year = quarter_year-1

                numbers: pd.DataFrame = numbers.loc[numbers['ddate'].astype(str).str.startswith(str(quarter_year))]
                numbers.to_csv(f, index=False, columns=['adsh', 'tag', 'iord', 'ddate', 'qtrs', 'value', 'fp', 'version', 'custom', 'abstract', 'tlabel'])

            # print('num shape before prefiltering', numbers.shape)
            # numbers: pd.DataFrame = numbers.loc[numbers['tag'].isin(all_tags)]
            # numbers: pd.DataFrame = numbers.loc[numbers['fp'].isin(['FY'])]
            # numbers: pd.DataFrame = numbers.loc[(numbers['qtrs'].isin([0,4]))]
            # numbers: pd.DataFrame = numbers.loc[numbers['ddate'].astype(str).str.startswith(quarter_name[:4])]
            # print('num shape after prefiltering', numbers.shape)
            #
            # df = pd.DataFrame(index=numbers['cik'], columns=numbers['tag'].unique().tolist())
            # df.fillna(0, inplace=True)
            #
            # for i, row in numbers.iterrows():
            #     df[row['tag']].loc[df.index == row['cik']] = row['value']
            #
            # with open(target_file_path, 'w') as f:
            #     df.to_csv(f)


    @staticmethod
    def organize_tags():
        all_tags = XBRLDataSetProvider._get_all_tags()

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
    def _get_all_tags():

        all_tags = pd.Series()

        for quarter_dir in reversed(os.listdir(XBRLDataSetProvider.res_dir)):

            quarter_dir = os.path.join(XBRLDataSetProvider.res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            tag_file = os.path.join(quarter_dir, 'tag.txt')
            tags = pd.read_csv(tag_file, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, usecols=['tag'])
            all_tags = all_tags.append(tags)
        return all_tags

    @staticmethod
    def organize_data_set(dir_separator='\\'):

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

        for quarter_dir in os.listdir(XBRLDataSetProvider.res_dir):

            quarter_dir = os.path.join(XBRLDataSetProvider.res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            quarter_name = quarter_dir.rsplit(dir_separator, 1)[-1]
            target_file_path = os.path.join(output_dir, quarter_name + '.csv')
            if os.path.exists(target_file_path):
                continue


            with open(target_file_path, 'w') as f:
                f.write('processing')

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
