import quandl, datetime

quandl.ApiConfig.api_key = 'cRdqvQB3sUYztU_SxFsX'
# quandl.ApiConfig.api_key = 'a5w2rRgAWxwj-kHKNofH'

def quandl_stocks(symbol, start_date=(2000, 1, 1), end_date=None, gran='daily'):

    query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(1, 13)]

    start_date = datetime.date(*start_date)

    if end_date:
        end_date = datetime.date(*end_date)
    else:
        end_date = datetime.date.today()

    return quandl.get(query_list,
                      returns='pandas',
                      start_date=start_date,
                      end_date=end_date,
                      collapse=gran,
                      order='asc'
                      )