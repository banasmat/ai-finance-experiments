from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider
from app.xbrl.XbrlRnn import XbrlRnn

x, y = XBRLDataSetProvider.get_dataset_from_yahoo_fundamentals()

# TODO
# scale wih sklearn scaler
# flatten data
# pick algorithm
# train