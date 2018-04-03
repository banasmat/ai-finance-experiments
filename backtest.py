from app.backtest.BackTester import BackTester
import datetime

if __name__ == '__main__':
    backtester = BackTester()

    date_from = datetime.datetime.strptime('2017-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
    date_to = datetime.datetime.strptime('2017-04-01 00:00:00', '%Y-%m-%d %H:%M:%S')

    backtester.run(date_from, date_to, gran='H1', iterations=3)