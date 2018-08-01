import numpy as np
import pandas as pd
import time
import os
import pickle
import csv
import app.dataset.xbrl_titles as xbrl_titles
from app.live_update.quandl_price_fetcher import quandl_stocks
import calendar
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime


class XBRLDataSetProvider(object):
    res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')
    yahoo_fundamentals_dataset_dir = os.path.join(os.path.abspath(os.getcwd()), 'output', 'yahoo_fundamentals')
    xbrl_dataset_dir = os.path.join(os.path.abspath(os.getcwd()), 'output', 'xbrl_dataset')
    xbrl_dataset_fixed_dir = os.path.join(os.path.abspath(os.getcwd()), 'output', 'xbrl_dataset_fixed')
    xbrl_data_x_file_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'xbrl_data_x.pkl')
    xbrl_data_y_file_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'xbrl_data_y.pkl')
    yahoo_fundamentals_data_x_file_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'yahoo_fundamentals_data_x.pkl')
    yahoo_fundamentals_data_y_file_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'yahoo_fundamentals_data_y.pkl')
    most_popular_tags_file_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'most_popular_tags.txt')
    common_tags_file_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'common_tags.txt')
    company_list_dir = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'company_list')
    cik_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'cik.pkl')
    # cik_map_file_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'cik_map.csv')
    cik_map_file_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'cik_map_precise.csv')
    stock_historical_prices_dir = os.path.join(os.path.abspath(os.getcwd()), 'output', 'stock_historical_prices')

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

        with open(XBRLDataSetProvider.cik_file_path, 'wb') as f:
            pickle.dump(cik_map, f)

    @staticmethod
    def get_common_tags():
        all_tags = pd.DataFrame()

        for quarter_dir in reversed(os.listdir(XBRLDataSetProvider.res_dir)):

            quarter_dir = os.path.join(XBRLDataSetProvider.res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue
            print(quarter_dir)
            num_file = os.path.join(quarter_dir, 'num.txt')
            tag_file = os.path.join(quarter_dir, 'tag.txt')
            sub_file = os.path.join(quarter_dir, 'sub.txt')
            numbers = pd.read_csv(num_file, sep='\t', encoding='ISO-8859-1', usecols=['tag', 'adsh'])
            tags = pd.read_csv(tag_file, sep='\t', encoding='ISO-8859-1', usecols=['tag', 'custom', 'abstract'], engine='python', error_bad_lines=False)
            subs = pd.read_csv(sub_file, sep='\t', encoding='ISO-8859-1', usecols=['adsh', 'fp'])
            numbers = numbers.merge(tags, on='tag', how='left')
            numbers = numbers.merge(subs, on='adsh', how='left')


            numbers = numbers.loc[numbers['custom'] == 0]
            numbers = numbers.loc[numbers['abstract'] == 0]
            numbers: pd.DataFrame = numbers.loc[numbers['fp'].isin(['FY'])]


            print('adsh len', len(numbers['adsh'].unique()))

            all_tags = all_tags.append(numbers)

        all_tags = all_tags.groupby(['tag'])['tag'].count()
        all_tags = all_tags.sort_values(ascending=True)
        #all_tags = all_tags.index.unique().tolist()

        with open(XBRLDataSetProvider.common_tags_file_path, 'w') as f:
            for tag, count in all_tags.iteritems():
                # f.write("%s - %d\n" % (tag, count))
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
        # output_dir = os.path.join(os.path.abspath(os.getcwd()), 'output', 'xbrl_most_popular_tags')
        output_dir = XBRLDataSetProvider.xbrl_dataset_dir
        # with open(XBRLDataSetProvider.most_popular_tags_file_path, 'r') as f:
        with open(XBRLDataSetProvider.common_tags_file_path, 'r') as f:
            for tag in f:
                all_tags.append(tag.strip())

        all_tags = all_tags[-2320:]
        all_tags = sorted(all_tags)

        pd.options.mode.chained_assignment = None

        # example_cik = 1459200
        quarters = list(reversed(os.listdir(XBRLDataSetProvider.res_dir)))

        for i, quarter_dir in enumerate(quarters):

            quarter_dir = os.path.join(XBRLDataSetProvider.res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            quarter_name = quarter_dir.rsplit(dir_separator, 1)[-1]
            current_year = quarter_name[:4]

            lock_file_path = os.path.join(output_dir, 'lock_' + quarter_name + '.lock')
            target_file_path = os.path.join(output_dir, current_year + '.csv')

            if os.path.exists(lock_file_path):
                continue

            with open(lock_file_path, 'w') as f:
                f.write('processing')

            print('QUARTER', quarter_name)

            num_file = os.path.join(quarter_dir, 'num.txt')
            sub_file = os.path.join(quarter_dir, 'sub.txt')
            tag_file = os.path.join(quarter_dir, 'tag.txt')

            numbers = pd.read_csv(num_file, sep='\t', encoding='ISO-8859-1', usecols=['adsh', 'tag', 'value', 'qtrs', 'ddate', 'coreg'])
            subs = pd.read_csv(sub_file, sep='\t', encoding='ISO-8859-1', usecols=['adsh', 'cik', 'fp'])
            tags = pd.read_csv(tag_file, sep='\t', encoding='ISO-8859-1', usecols=['tag', 'iord', 'custom', 'version', 'tlabel', 'abstract'])

            numbers = numbers.merge(subs, on='adsh', how='left')
            numbers = numbers.merge(tags, on='tag', how='left')

            print('num shape before prefiltering', numbers.shape)
            numbers: pd.DataFrame = numbers.loc[numbers['tag'].isin(all_tags)]
            numbers: pd.DataFrame = numbers.loc[numbers['fp'].isin(['FY'])]
            numbers: pd.DataFrame = numbers.loc[numbers['coreg'].isnull()]
            numbers: pd.DataFrame = numbers.loc[(numbers['qtrs'].isin([0,4]))]
            numbers: pd.DataFrame = numbers.loc[(numbers['ddate'].astype(str).str.startswith(current_year)) | numbers['ddate'].astype(str).str.startswith(str(int(current_year)-1))]
            print('num shape after prefiltering', numbers.shape)

            ciks = numbers['cik'].sort_values(ascending=True).unique()

            # numbers: pd.DataFrame = numbers.loc[numbers['cik'].isin(ciks)]
            # print('num shape after prefiltering ciks', numbers.shape)
            numbers.sort_values(by=['tag', 'cik'], ascending=True, inplace=True)

            df = pd.DataFrame(index=ciks, columns=all_tags)
            df.fillna(0, inplace=True)

            for tag in all_tags:

                tag_vals = numbers.loc[numbers.tag == tag]

                for cik in ciks:
                    cik_vals = tag_vals.loc[tag_vals.cik == cik]
                    if cik_vals.shape[0] == 0:
                        continue
                    vals = cik_vals.loc[(cik_vals.tag == tag)]
                    # numbers.drop(index=vals.index, inplace=True)
                    if vals.shape[0] > 0:
                        val = vals.nlargest(1, 'ddate')
                        df[tag].loc[df.index == cik] = val['value'].mean()

            df = df[(df.T != 0).any()]
            header = True
            if os.path.exists(target_file_path):
                header = False

            with open(target_file_path, 'a') as f:
                df.to_csv(f, header=header)

    @staticmethod
    def preorganize_tags():

        all_tags = XBRLDataSetProvider._get_all_tags()

        target_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'tags_preorganized.txt')

        results = {}

        for title in xbrl_titles.titles:

            _title = title

            to_replace = ['of', 'gross', 'net', 'and', 'gain', 'loss', 'total', 'other', 'current', 'from', 'in']
            for rep in to_replace:
                _title = ' ' + _title + ' '
                _title = _title.replace(' ' + rep + ' ', ' ')
                _title = _title.replace(',', ' ')
                _title = _title.replace('/', ' ')
                _title = _title.replace('(', ' ')
                _title = _title.replace(')', ' ')
                _title = _title.replace('-', ' ')

            keywords = _title.split(' ')
            keywords = list(filter(None, keywords))

            results[title] = []

            for keyword in keywords:
                print(keyword)
                for tag in all_tags:
                    print(tag)
                    if keyword in str(tag):
                        results[title].append(tag)

        with open(target_file_path, 'w') as f:
            for title, keywords in results.items():
                f.write("\n%s:[\n" % title)
                for item in keywords:
                    f.write("    '%s',\n" % item)
                f.write("]\n")

    @staticmethod
    def organize_tags():

        from fuzzywuzzy import process

        all_tags = XBRLDataSetProvider._get_all_tags()

        # target_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'tags.txt')
        #
        # with open(target_file_path, 'a') as f:
        #     for item in all_tags:
        #         f.write("%s\n" % item)

        target_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'tags_organized.txt')

        for title in xbrl_titles.titles:

            title = title.replace('&', 'and')
            print(title)
            result = process.extract(title, all_tags, limit=15)
            with open(target_file_path, 'a') as f:
                f.write("\n%s:\n" % title)
                for item in result:
                    f.write("%s - %s\n" % (item[0], str(item[1])))

    @staticmethod
    def _get_all_tags():

        all_tags = []

        for quarter_dir in reversed(os.listdir(XBRLDataSetProvider.res_dir)):

            quarter_dir = os.path.join(XBRLDataSetProvider.res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            num_file = os.path.join(quarter_dir, 'num.txt')
            tags = pd.read_csv(num_file, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, usecols=['tag'])

            all_tags = all_tags + tags['tag'].tolist()
            all_tags = list(set(all_tags))

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

    @staticmethod
    def get_all_ciks_map():
        all_ciks = pd.DataFrame()
        all_companies = pd.DataFrame()

        for company_list in os.listdir(XBRLDataSetProvider.company_list_dir):
            companies = pd.read_csv(os.path.join(XBRLDataSetProvider.company_list_dir, company_list), usecols=["Symbol", "Name", "industry"]) # "LastSale","MarketCap","IPOyear","Sector",
            all_companies = all_companies.append(companies)

        for quarter_dir in reversed(os.listdir(XBRLDataSetProvider.res_dir)):

            quarter_dir = os.path.join(XBRLDataSetProvider.res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            sub_file = os.path.join(quarter_dir, 'sub.txt')
            subs = pd.read_csv(sub_file, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, usecols=['cik', 'name'])

            all_ciks = all_ciks.append(subs)
            all_ciks.drop_duplicates('cik', inplace=True)

        all_ciks.sort_values('name', inplace=True)
        all_companies.sort_values('Name', inplace=True)

        all_ciks['name_copy'] = all_ciks['name']
        all_companies['name_copy'] = all_companies['Name']

        def __clean_name(name):
            return name.lower().replace(',', '').replace('.', '').replace('\'', '').replace('"', '')

        all_ciks['name_copy'] = all_ciks['name_copy'].apply(lambda name: __clean_name(name))
        all_companies['name_copy'] = all_companies['name_copy'].apply(lambda name: __clean_name(name))

        print('all ciks', all_ciks.shape)

        all_ciks = all_ciks.merge(all_companies, on='name_copy', how='left')
        all_ciks = all_ciks.drop('Name', axis=1)
        all_ciks = all_ciks.drop('name_copy', axis=1)
        all_ciks['symbol'] = all_ciks['Symbol']
        all_ciks = all_ciks.drop('Symbol', axis=1)

        all_ciks.drop_duplicates('symbol', inplace=True)
        # print(all_ciks.head(20))
        print('ciks with symbols', all_ciks.loc[~pd.isnull(all_ciks['symbol'])].shape)
        with open(XBRLDataSetProvider.cik_map_file_path, 'w') as f:
            all_ciks.to_csv(f, index=False)

    @staticmethod
    def xbrl_statistical_analysis():

        for year_file in reversed(os.listdir(XBRLDataSetProvider.xbrl_dataset_dir)):
            if year_file[0] == '.':
                continue
            with open(os.path.join(XBRLDataSetProvider.xbrl_dataset_dir, year_file), 'r') as f:
                print('YEAR', year_file[0:4])
                df: pd.DataFrame = pd.read_csv(f)
                # print(df.describe())

                # nulls_summary = pd.DataFrame(df.isnull().any(), columns=['Nulls'])
                # nulls_summary['Num_of_nulls [qty]'] = pd.DataFrame(df.isnull().sum())
                # nulls_summary['Num_of_nulls [%]'] = round((df.isnull().mean() * 100), 2)
                # print(nulls_summary)

                # print('non zeros [qty]', df.astype(bool).sum(axis=0))
                non_zero_perc: pd.Series = round((df.astype(bool).sum(axis=0)/df.shape[0] * 100), 2)
                # print('non zeros [%]', non_zero_perc)
                print('non zeros above 90 [%]', non_zero_perc.loc[non_zero_perc >= 70])

    @staticmethod
    def gather_stock_prices():

        ciks_map = pd.read_csv(XBRLDataSetProvider.cik_map_file_path, usecols=['cik', 'symbol'])
        ciks_map = ciks_map.loc[~pd.isnull(ciks_map['symbol'])]

        date_format = "%Y-%m-%d"

        pd.options.mode.chained_assignment = None

        for year_file in reversed(sorted(os.listdir(XBRLDataSetProvider.xbrl_dataset_dir))):
            if year_file[0] == '.':
                continue

            year = year_file[0:4]
            print('YEAR', year)

            target_file = os.path.join(XBRLDataSetProvider.stock_historical_prices_dir, year + '.csv')

            if os.path.isfile(target_file):
                f = open(target_file, 'r')
                df: pd.DataFrame = pd.read_csv(f, index_col='symbol')
            else:
                df = pd.DataFrame(index=ciks_map['symbol'])

            updated_df = pd.DataFrame(index=ciks_map['symbol'])
            updated_df = updated_df.merge(df, left_index=True, right_index=True, how='left')
            df = updated_df
            df = df[~df.index.duplicated(keep='first')]

            dates = XBRLDataSetProvider.__get_last_month_day_dates(year)

            for date_str in dates:
                if date_str not in df.columns:
                    df[date_str] = pd.Series()

            for symbol, row in df.iterrows():

                if pd.isnull(row[dates[11]]):
                    time.sleep(5)
                    date_from = (int(year), 1, 1)
                    date_to = (int(year), 12, 31)
                    try:
                        print(symbol)
                        price_data = quandl_stocks(symbol, date_from, date_to, gran='monthly')

                        close_col_name = None

                        for col in price_data.columns:
                            if col[-5:] == 'Close':
                                close_col_name = col
                                break
                        if close_col_name is None:
                            raise LookupError("No Close column returned for symbol: " + row['symbol'])
                        else:
                            # First fill row with default zeros
                            df.loc[symbol, dates] = 0
                            for price_date, price_val in price_data[close_col_name].iteritems():
                                price_date = price_date.strftime(date_format)
                                df.loc[symbol, price_date] = price_val
                                print(symbol, '-', price_date, ':', price_val)
                            # Saving every request result to file

                    except ValueError as e:
                        #FIXME why ValueError is thrown
                        print('ValueError occured', symbol, str(e))
                        for price_date in dates:
                            df.loc[symbol, price_date] = 0

                    try:
                        f.close()
                    except NameError:
                        'file doesn\'t yet exist'
                    f = open(target_file, 'w')

                    df.to_csv(f)
                    f.close()
    @staticmethod
    def __get_last_month_day_dates(year):

        dates = []

        for month in range(1, 13):
            last_day = calendar.monthrange(int(year), month)[1]
            month = str(month)
            if len(month) == 1:
                month = '0' + month
            date_str = '-'.join([year, month, str(last_day)])
            dates.append(date_str)

        return dates

    @staticmethod
    def prepare_dataset_from_yahoo_fundamentals():

        symbol_files = os.listdir(XBRLDataSetProvider.yahoo_fundamentals_dataset_dir)
        price_files = os.listdir(XBRLDataSetProvider.stock_historical_prices_dir)

        dataset_x = None
        dataset_y = None
        years = []
        years_len = None
        tags_len = None
        i = 0

        #TODO
        # - read columns, get years
        # - open relevant year files, merge prices to one value
        # - merge prices for every year to df (?)

        all_prices_df = XBRLDataSetProvider.__get_all_prices_df()
        empty_price_symbols = XBRLDataSetProvider.__get_empty_price_symbols(all_prices_df)

        for symbol_file in symbol_files:

            symbol = symbol_file[:-4]
            if symbol in empty_price_symbols:
                continue

            with open(os.path.join(XBRLDataSetProvider.yahoo_fundamentals_dataset_dir, symbol_file), 'r') as f:
                df: pd.DataFrame = pd.read_csv(f, index_col=0)

                # Assuming that first file has got the right number of years/tags
                if years_len is None:
                    years_len = df.shape[1]
                    tags_len = df.shape[0]
                    for col in df.columns:
                        years.append(col[-4:])

                # Some files have duplicated whole lists. TODO clean them up
                df = df.head(tags_len)

                current_year = datetime.today().year

                if len(df.columns) == 0:
                    continue

                if df.columns[0][-4:] != str(current_year-1):
                    continue

                if df.shape[0] < tags_len:
                    continue

                j = 0
                while df.shape[1] < years_len:
                    df[str(j)] = np.nan
                    j += 1

                if dataset_x is None:
                    dataset_x = np.zeros((0, tags_len, years_len))
                    dataset_y = np.zeros((0, years_len))

                for year in years:
                    with open(os.path.join(XBRLDataSetProvider.stock_historical_prices_dir, year + '.csv'), 'r') as yf:
                        price_df = pd.read_csv(yf)

                print(symbol)
                dataset_x = np.insert(dataset_x, i, df.as_matrix(), axis=0)
                i += 1
        print(dataset_x.shape)
        with open(XBRLDataSetProvider.yahoo_fundamentals_data_x_file_path, 'wb') as f:
            pickle.dump(dataset_x, f)


    @staticmethod
    def prepare_dataset_for_training():

        years_len = 0

        with open(XBRLDataSetProvider.cik_map_file_path, 'r') as f:
            all_ciks = set(pd.read_csv(f)['cik'])

        for year_file in os.listdir(XBRLDataSetProvider.xbrl_dataset_dir):
            if year_file[0] == '.':
                continue
            with open(os.path.join(XBRLDataSetProvider.xbrl_dataset_dir, year_file), 'r') as f:
                print('YEAR', year_file[0:4])
                df: pd.DataFrame = pd.read_csv(f, index_col=0)

                df = df[~df.index.duplicated(keep='last')]

                # TODO 'combine' similar columns

                years_len += 1

                diff = XBRLDataSetProvider.__list_diff(all_ciks, list(df.index))
                diff_df = pd.DataFrame(index=diff, columns=df.columns)
                diff_df.fillna(0, inplace=True)

                df = df.append(diff_df)
                print(df.shape)
                df = df.sort_index()

            target_file_path = os.path.join(XBRLDataSetProvider.xbrl_dataset_fixed_dir, year_file)
            with open(target_file_path, 'w') as f:
                df.to_csv(f)

    @staticmethod
    def __get_empty_price_symbols(all_prices_df: pd.DataFrame):
        all_prices_df.index = all_prices_df.pop('symbol')
        all_prices_df = all_prices_df.mean(axis=1)

        return list(all_prices_df[all_prices_df == 0].index)

    @staticmethod
    def __get_all_prices_df():

        year_files = os.listdir(XBRLDataSetProvider.xbrl_dataset_fixed_dir)  # [:3]

        all_prices_df = None

        # First locate and remove ciks with not even single historical price
        for year_file in sorted(year_files):
            if year_file[0] == '.':
                continue
            year = year_file[0:4]
            with open(os.path.join(XBRLDataSetProvider.stock_historical_prices_dir, year + '.csv'), 'r') as f:
                price_df = pd.read_csv(f)
                # price_df.index = price_df.pop('symbol')

                if all_prices_df is None:
                    all_prices_df = price_df.copy()
                else:
                    all_prices_df = all_prices_df.merge(price_df, on='symbol', how='left')

        return all_prices_df

    @staticmethod
    def get_dataset_for_training():
        if os.path.isfile(XBRLDataSetProvider.xbrl_data_x_file_path) and os.path.isfile(XBRLDataSetProvider.xbrl_data_y_file_path):
            with open(XBRLDataSetProvider.xbrl_data_x_file_path, 'rb') as f:
                x = pickle.load(f)
            with open(XBRLDataSetProvider.xbrl_data_y_file_path, 'rb') as f:
                y = pickle.load(f)
            return x, y

        ciks_map = pd.read_csv(XBRLDataSetProvider.cik_map_file_path, usecols=['cik', 'symbol'])
        ciks_map = ciks_map.loc[~pd.isnull(ciks_map['symbol'])]
        ciks_map = ciks_map.sort_values('symbol')
        ciks_map = ciks_map.drop_duplicates('cik', 'first')

        year_files = os.listdir(XBRLDataSetProvider.xbrl_dataset_fixed_dir) #[:3]

        dataset_x = None
        dataset_y = None
        i = 0

        all_prices_df = XBRLDataSetProvider.__get_all_prices_df()
        empty_price_symbols = XBRLDataSetProvider.__get_empty_price_symbols(all_prices_df)

        ciks_map = ciks_map.loc[~ciks_map['symbol'].isin(empty_price_symbols)]

        prev_df_y = None

        for year_file in sorted(year_files):
            if year_file[0] == '.':
                continue

            year = year_file[0:4]
            print('YEAR', year)

            with open(os.path.join(XBRLDataSetProvider.stock_historical_prices_dir, year + '.csv'), 'r') as f:
                price_df = pd.read_csv(f)

            with open(os.path.join(XBRLDataSetProvider.xbrl_dataset_fixed_dir, year_file), 'r') as f:

                df_x: pd.DataFrame = pd.read_csv(f, index_col=0)
                df_x['cik'] = df_x.index
                df_x = df_x.merge(ciks_map, on='cik', how='right')
                df_x.index = df_x.pop('cik')
                df_x.drop(['symbol'], axis=1, inplace=True)

                df_y = pd.DataFrame(df_x.index, columns=['cik'])
                df_y = df_y.merge(ciks_map, on='cik', how='right')
                # print(df_y.groupby(df_y.columns.tolist(),as_index=False).size())

                df_y: pd.DataFrame = df_y.merge(price_df, on='symbol', how='left')
                df_y = df_y.drop_duplicates('cik', 'first')

                df_y.index = df_y.pop('cik')
                df_y.drop(['symbol'], axis=1, inplace=True)

                # print(df_x.index)
                # print(df_y.index)
                # this_year_last_month_day_dates = XBRLDataSetProvider.__get_last_month_day_dates(year)
                # df_y = df_y[this_year_last_month_day_dates]

                df_y.fillna(0, inplace=True)
                if prev_df_y is None:
                    prev_df_y = pd.DataFrame(index=df_y.index, columns=df_y.columns)
                    prev_df_y.fillna(0, inplace=True)
                print(df_x.shape)
                print(df_y.shape)
                if dataset_x is None:
                    dataset_x = np.zeros((len(year_files)-1, df_x.shape[0], df_x.shape[1]))
                    dataset_y = np.zeros((len(year_files)-1, df_x.shape[0],)) # TODO verify if we don't need np.zeros((len(year_files)-1, df_x.shape[0], 1)) instead

                # print(df_y.mean(axis=1))

                dataset_x[i] = df_x.values
                dataset_y[i] = XBRLDataSetProvider.__get_xbrl_label(df_y, prev_df_y)

                # print(dataset_y)
                # quit()

                i += 1

                prev_df_y = df_y

        with open(XBRLDataSetProvider.xbrl_data_x_file_path, 'wb') as f:
            pickle.dump(dataset_x, f)
        with open(XBRLDataSetProvider.xbrl_data_y_file_path, 'wb') as f:
            pickle.dump(dataset_y, f)

        return dataset_x, dataset_y

    @staticmethod
    def scale_by_cik_tag(x, y):
        # cik, tag, year
        x = x.transpose((1, 2, 0))
        # cik, year
        y = y.transpose()

        for cik_index in range(0, x.shape[0]):
            x[cik_index] = XBRLDataSetProvider.scale_dataset(x[cik_index])
            x[cik_index] = np.nan_to_num(x[cik_index])

        # year, cik, tag
        x = x.transpose((2, 0, 1))
        # year, cik
        y = y.transpose()

        return x, y

    @staticmethod
    def scale_dataset(data: np.array):
        for i in range(0, data.shape[0]):

            _max = data[i].max()
            _min = data[i].min()

            if _max == 0 and _min == 0:
                data[i] = np.zeros(data[i].shape)
            elif _max - _min == 0:
                data[i] = np.full(data[i].shape, 1)
            else:
                for j in range(0, data[i].shape[0]):
                    data[i][j] = (data[i][j] - _min) / (_max - _min)
        return data


    @staticmethod
    def __get_xbrl_label(df_y, prev_df_y):
        df_y_mean = df_y.mean(axis=1)
        prev_df_y_mean = prev_df_y.mean(axis=1)

        diff_percent_df = (df_y_mean - prev_df_y_mean) / ((prev_df_y_mean + df_y_mean) / 2)
        diff_percent_df = diff_percent_df.apply(lambda x: 1 if x > 0.2 else 0)

        return diff_percent_df.values

    @staticmethod
    def __list_diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]