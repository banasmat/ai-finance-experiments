import os
import pandas as pd

'''
SUB – Submission data set; this includes one record for each XBRL submission.
NUM – Number data set; this includes one row for each distinct amount from each submission included in the SUB data set.
TAG – Tag data set; includes defining information about each tag.
PRE – Presentation data set; this provides information about how the tags and numbers were presented in the primary financial statements. (Text representation of TAG)

SUB:
adsh -  unique (primary) key
cik - registrant id
name - registrant name
sic - type of business id
countryba - country code
... address data ...
afs - Filer status with the SEC at the time of submission:
    1-LAF=Large Accelerated,
    2-ACC=Accelerated,
    3-SRA=Smaller Reporting Accelerated,
    4-NON=Non-Accelerated,
    5-SML=Smaller Reporting Filer,
    NULL=not assigned.
wksi - 	Well Known Seasoned Issuer (WKSI). An issuer that meets specific SEC requirements (boolean)
form - The submission type of the registrant’s filing.
period - Balance Sheet Date.
filled - datetime
accepted - datetime
fye - Fiscal Year End Date.
fy - Fiscal Year Focus
fp - Fiscal Period Focus: ALPHANUMERIC (FY, Q1, Q2, Q3, Q4, H1, H2, M9, T1, T2, T3, M8, CY)
prevrpt - Previous Report –TRUE indicates that the submission information was subsequently amended. (boolean)
detail - boolean
instance
nciks
acisks

NUM
adsh - reference to SUB
tag - reference to TAG
version - tag version
value - not scaled, 4 digits after .
ddate - The end date for the data value, rounded to the nearest month end.
qtrs - The count of the number of quarters represented by the data value, rounded to the nearest whole number. “0” indicates it is a point-in-time value.
uom - unit of measure
coreg - co-registrant/parent company
footnote - note on value


NOTES
len all NUM: 2255775
len adsh: 6506
all/adsh = 346

w jednym kwartale:
mamy 6500 firm, każda ma po 350 wartości (dla różnych tagów, dla różnych dat)

PROPOZYCJA
bierzemy wszystkie wartości, sortujemy wg firm, tagów, dat
tak samo sortujemy wszystkie historyczne xblry - trzeba się upewnić, że jest tyle samo


'''

file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'xbrl', '2017q3', 'pre.txt')

subs: pd.DataFrame = pd.read_csv(file_path, sep='\t', encoding='ISO-8859-1')
print(subs[['tag', 'plabel']].tail())
# print(len(subs['adsh'].drop_duplicates()))
# print(len(subs['adsh']))
# print(len(subs['adsh'])/len(subs['adsh'].drop_duplicates()))

# with open(os.path.join(os.path.abspath(os.getcwd()), 'resources', '2017q3', 'sub.txt'),"r") as f:
