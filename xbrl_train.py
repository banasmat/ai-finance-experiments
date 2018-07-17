from app.dataset.XBRLDataSetProvider import XBRLDataSetProvider
from app.xbrl.XbrlRnn import XbrlRnn

x, y = XBRLDataSetProvider.get_dataset_for_training()
x, y = XBRLDataSetProvider.scale_by_cik_tag(x, y)

rnn = XbrlRnn()
rnn.train(x[:-1], y[:-1])



predictions = rnn.predict(x[-1:])
# print(predictions[0])
# print(y[-1:][0])
predictions = list(map(lambda x: 0 if x < 0.5 else 1, predictions[0].tolist()))
print(predictions)

test_vals = y[-1:][0].tolist()
print(test_vals)
correct_predictions = 0
for i in range (0, len(predictions)):
    if predictions[i] == test_vals[i]:
        correct_predictions += 1


# accuracy = len(set(predictions) & set(y[-1:][0].tolist())) / len(predictions)
print('accuracy',correct_predictions/len(predictions))


#TODO
# nie puszczać cików razem tylko osobno (?) - tracimy continuum, ale lepsze to niż nic
# LUB
# https://datascience.stackexchange.com/questions/27563/multi-dimentional-and-multivariate-time-series-forecast-rnn-lstm-keras
#
# trzeba jakoś odczytać predictions
# wypluć tabelkę wyników: Symbol/cik : wynik
#
# Dane:
# jeśli zero jest pomiędzy innymi wartościami, brać poprzednią
#
# UWAGA: sprawdzić czy nie trzeba przesunąć danych w Y o 1 (czy chcemy brać wynik z tego roku czy z nastepnego)
#
# Korekcja datasetu:
# porównać kolumny z datasetami z quandla / intrinio
# https://www.quora.com/What-is-the-best-source-for-free-historical-fundamental-stock-data
# https://intrinio.com/tutorial/file_download
# https://www.quandl.com/search?query=fundamental
# https://public.opendatasoft.com/explore/dataset/us-stock-fundamentals/?disjunctive.indicator - FREE, ale tylko quarters (?)
#
# CIK MAP:
# ticker symbol https://www.sec.gov/divisions/corpfin/organization/cfia.shtml (jest też SIC CODE - czyli branża)
# https://gist.github.com/dougvk/8499335
# http://rankandfiled.com/#/data/tickers !!!



# https://app.finviews.com
# 98 tags
# income statement
#["Revenues","CostOfRevenue","GrossProfit","SellingGeneralAndAdministrativeExpense","DepreciationAndAmortization","OperatingExpenses","OperatingIncomeLoss","InterestAndDebtExpense","NonoperatingIncomeExpense","ProfitBeforeTax","IncomeTaxExpenseBenefit","IncomeLossFromEquityMethodInvestments","ProfitLoss","NetIncomeLossAttributableToNoncontrollingInterest","NetIncomeLoss","NetIncomeLossAvailableToCommonStockholdersBasic","EarningsPerShareBasic","EarningsPerShareDiluted","WeightedAverageNumberOfSharesOutstandingBasic","WeightedAverageNumberOfDilutedSharesOutstanding","OtherOperatingIncomeExpenses"]
# balance sheet
#["CashCashEquivalentsAndShortTermInvestments","AccountsAndOtherReceivables","InventoryNet","DeferredAssetsCurrent","PrepaidAndOtherExpenses","OtherAssetsCurrent","AssetsHeldForSaleCurrent","AssetsCurrent","PropertyPlantAndEquipmentNet","AssetsNoncurrent","Assets","AccountsAndOtherPayables","AccruedLiabilitiesCurrent","DebtCurrent","LiabilitiesHeldForSaleCurrent","LiabilitiesCurrent","LongTermDebt","DeferredLiabilitiesNoncurrent","PensionsAndOtherPostEmploymentLiabilities","OtherLiabilitiesNoncurrent","LiabilitiesHeldForSaleNoncurrent","LiabilitiesNoncurrent","Liabilities","TemporaryEquity","CommonStockValue","AdditionalPaidInCapital","CommonStockIncludingAdditionalPaidInCapital","TreasuryStockValue","AccumulatedOtherComprehensiveIncomeLossNetOfTax","RetainedEarningsAccumulatedDeficit","StockholdersEquity","MinorityInterest","StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest","LiabilitiesAndStockholdersEquity","LongTermInvestmentsAndReceivablesNet","OtherAssetsNoncurrent","OtherLiabilitiesCurrent","Goodwill"]
# cash flow
#["NetProfit","IncomeLossFromContinuingOperations","DepreciationAmortizationAndRelated","WriteDownsAndRestructuringSettlementAndImpairmentProvisions","OtherNoncashIncomeExpense","DeferredIncomeTaxExpenseBenefit","VariousGainsAndLosses","IncreaseDecreaseInAccountsAndOtherReceivables","IncreaseDecreaseInInventories","IncreaseDecreaseInPrepaidAndDeferredCurrentAssets","IncreaseDecreaseInOtherOperatingAssets","IncreaseDecreaseInAccountsPayableAndAccruedLiabilities","IncreaseDecreaseInOtherOperatingLiabilities","ChangeInWorkingCapitalAndOtherOperatingAssetsAndLiabilities","CapitalExpenditures","ProceedsAndPaymentsRegardingSecuritiesAndInvestments","AcquisitionsDisposalsOfBusinessesAndOtherProducingAssets","OtherInvestingCashFlows","NetCashProvidedByUsedInInvestingActivitiesContinuingOperations","NetCashProvidedByUsedInInvestingActivities","DividendsAndOtherDistributionPayments","RepurchaseOfStock","ProceedsFromBorrowings","RepaymentsOfBorrowings","OtherFinancingCashFlows","CashAndCashEquivalentsPeriodIncreaseDecreaseBeforeEffectOfExchangeRate","EffectOfExchangeRateOnCashAndCashEquivalents","NetCashProvidedByUsedInDiscontinuedOperations","CashAndCashEquivalentsPeriodIncreaseDecrease","InterestPaid","IncomeTaxesPaidNet","IncreaseDecreaseInOtherOperatingCapitalNet","ProceedsFromStockIssuance","IncomeLossFromDiscontinuedOperationsNetOfTax","ShareBasedCompensation","AmortizationOfFinancingCostsDiscountsAndVariousPremiums","IncreaseDecreaseInEmployeeRelatedLiabilities","CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations","OtherNonCashOperatingItems"]