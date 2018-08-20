import quandl, datetime
from app.Config import Config

def quandl_stocks(symbol, start_date=(2000, 1, 1), end_date=None, gran='daily'):

    config_key_index = 1

    query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(1, 13)]

    start_date = datetime.date(*start_date)

    if end_date:
        end_date = datetime.date(*end_date)
    else:
        end_date = datetime.date.today()

    try:
        return quandl.get(query_list,
                          returns='pandas',
                          start_date=start_date,
                          end_date=end_date,
                          collapse=gran,
                          order='asc'
                          )
    except quandl.errors.quandl_error.LimitExceededError as e:

        print(e)

        config_key_index += 1

        if config_key_index >= len(Config['quandl']['api_keys']):
            config_key_index = 0

        quandl.ApiConfig.api_key = Config['quandl']['api_keys'][config_key_index]

        try:

            return quandl.get(query_list,
                              returns='pandas',
                              start_date=start_date,
                              end_date=end_date,
                              collapse=gran,
                              order='asc'
                              )
        except quandl.errors.quandl_error.LimitExceededError as e:
            print(e)
