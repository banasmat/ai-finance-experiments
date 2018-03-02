import time, os
from SECEdgar.crawler import SecCrawler


def get_filings():
    t1 = time.time()

    DEFAULT_DATA_PATH = os.path.join(os.path.abspath(os.getcwd()), 'output')

    # create object
    seccrawler = SecCrawler()

    companyCode = 'AAPL'  # company code for apple
    cik = '0000320193'  # cik code for apple
    date = '20010101'  # date from which filings should be downloaded
    count = '10'  # no of filings

    seccrawler.filing_10Q(str(companyCode), str(cik), str(date), str(count))
    seccrawler.filing_10K(str(companyCode), str(cik), str(date), str(count))
    seccrawler.filing_8K(str(companyCode), str(cik), str(date), str(count))
    seccrawler.filing_13F(str(companyCode), str(cik), str(date), str(count))

    t2 = time.time()
    print("Total Time taken: "),
    print(t2 - t1)


if __name__ == '__main__':
    get_filings()