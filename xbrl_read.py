from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider
import time
from multiprocessing import Process

# if __name__ == '__main__':
#
#     num_proc = 4
#     processes = []
#     for i in range(0,num_proc):
#         processes.append(Process(target=XBRLDataSetProvider.prepare_data_set_with_most_popular_tags))
#         processes[i].start()
#         time.sleep(20)
#
#     for i in range(0,num_proc):
#         processes[i].join()

# XBRLDataSetProvider.organize_data_set()
# XBRLDataSetProvider.extract_cik_numbers()
# XBRLDataSetProvider.organize_tags()
#XBRLDataSetProvider.preorganize_tags()
# XBRLDataSetProvider.get_most_popular_tags()
# XBRLDataSetProvider.get_common_tags()
# XBRLDataSetProvider.prepare_data_set_with_most_popular_tags()
XBRLDataSetProvider.xbrl_statistical_analysis()
# XBRLDataSetProvider.get_all_ciks_map()
# XBRLDataSetProvider.append_prices_to_dataset()
#XBRLDataSetProvider.prepare_dataset_for_training()
