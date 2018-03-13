from typing import List, Tuple

import numpy as np
import pandas as pd
import os
import pickle
import csv
from fuzzywuzzy import process

class XBRLDataSetProvider(object):

    titles = {

                 'revenue': [
                     'Revenue',
                     'Revenues',
                     'Revenue1',
                     # 'OperatingRevenues',
                     # 'OtherRevenue',
                     ],

                 'cost of goods sold': [
                     'CostOfGoodsSold',
                     'CostOfGoodsSold1',
                     'CostOfGoodsGold',
                     'CostOfGoodsSoldNet',
                     'CostOfGoodsSoldnet',
                     'NetCostOfGoodsSold',
                     # 'DistributionSalesCostOfGoodsSold',
                     # 'DepreciationCostOfGoodsSold',
                     # 'RestructuringChargesUnderCostOfGoodsSold',
                     # 'EquipmentTransferredToCostOfGoodsSold',
                     # 'MobilityProductsCostOfGoodsSold',
                     # 'LifestyleSegmentCostOfGoodsSold',
                     # 'ProductAndOtherCostOfGoodsSold',
                     # 'EnergyTechnologyCostOfGoodsSold'
                 ],

                 'gross profit': [
                     'GrossProfit',
                     'GrossProfit1',
                     'GrossProfit2',
                     'GrossProfits',
                     # 'ProductGrossProfit',
                     # 'ServicesGrossProfit',
                     # 'LeaseContractsGrossProfit',
                     # 'LicenseGrossProfit',
                     # 'MaintenanceGrossProfit',
                     # 'RentalAndRoyaltyGrossProfit',
                     # 'RealEstateLoansGrossProfit',
                     # 'SystemsGrossProfit'
                 ],

                 'selling, general and admin': [
                     'SellingGeneralAndAdministrative',
                     'OtherSellingGeneralAndAdministrativeExpense',
                 ],

                 'research and development': [
                     'ResearchAndDevelopment',
                     'Research',
                     'Development',
                     'ResearchAndDevelopmentNet',
                     'ResearchAndDevelopmentFees',
                     'ResearchAndDevelopmentCost',
                     'ResearchAmpDevelopment',
                     'In-ProcessResearchAndDevelopment'
                 ],

                 'interest': [
                     'Interest',
                     'Interest1',
                     'InterestExpense-Net'
                 ],

                 'depreciation': [
                     'Depreciation',
                     'Depreciation1',
                     'Depreciation2',
                     'Deprecation',
                     'Depreciations',
                     'Depreciation3',
                     # 'GeneralAndAdministrativeExpenseExcludingDepreciation',
                     # 'Depreciationandamortizationexcludingdepreciationoncommunicationequipment',
                     # 'DepreciationDepletionAmortizationAndAccretionIncludingDiscontinuedOperations',
                     # 'AccumulatedDepreciationDepletionAndAmortizationSaleOfPropertyPlantAndEquipment1',
                     # 'AccumulatedDepreciationDepletionAndAmortizationPropertyPlantAndEquipment',
                     # 'AccumulatedDepreciationDepletionAndAmortizationPropertyPlantAndEquipmentPeriodIncreaseDecrease',
                     # 'CostOfServicesDepreciation'
                     # 'DepreciationandGainLossonDispositionofPropertyPlantEquipment',
                 ],

                 'operating profit': [
                     # 'Operating',
                     'FinancialServicesOperatingProfit',
                     # 'OperatingProfitLoss',
                     # 'OperatingPropertiesNet',
                 ],

                 'gain (loss) sale assets': [
                     'GainLossOnSaleAssets',
                     'GainLossOnSaleOfAssets',
                     'GainLossonSaleofAssets',
                     'GainLossOnSaleofAssets',
                     'GainLossOnSaleOfAssets1',
                     'GainLossOnSalesOfAssets',
                     'GainLossOnSaleAndWrite-DownOfOtherRealEstateAndRepossessedAssets',
                     'GainLossOnSaleOfAssets11',
                 ],

                 'other': [
                     'Other',
                     'Other2',
                     'Others',
                     'OtherRevenue',
                 ],

                 'income before tax': [
                     'IncomeBeforeTaxes',
                     'NetIncomeBeforeTax',
                     # 'ComprehensiveIncomeBeforeTax',
                     # 'TotalComprehensiveIncomeBeforeTax',
                     # 'NetRealizedGainLossIncludedInNetIncomeBeforeTax',
                     # 'OtherComprehensiveIncomeBeforeTax',
                     # 'DefinedBenefitPlanAccumulatedOtherComprehensiveIncomeBeforeTax',
                     # 'OtherComprehensiveIncomeLossAmortizationOfNetUnrealizedHoldingLossesToIncomeBeforeTax',
                     # 'Othercomprehensiveincomelossderivativesqualifyingashedgesreclassificationadjustmentsinnetincomebeforetax',
                     # 'ChangesInOtherThanTemporaryImpairmentLossesRecognizedInOtherComprehensiveIncomeBeforeTax',
                     # 'OtherComprehensiveIncomeAmortizationOfUnrealizedHoldingGainLossPreviouslyRecognizedInOtherComprehensiveIncomeBeforeTax',
                     # 'OtherComprehensiveIncomeLossReclassificationAdjustmentIncludedInNetIncomeBeforeTax',
                     # 'PortionOfLossRecognizedInOtherComprehensiveIncomeBeforeTax',
                     # 'OtherThanTemporaryImpairmentReclassificationAdjustmentForLossesIncludedInNetIncomeBeforeTax',
                     # 'ReclassificationAdjustmentForCreditRelatedOttiIncludedInNetIncomeBeforeTax'
                 ],

                 'income taxes paid': [
                     'IncomeTaxesPaid',
                     'IncomeTaxesPaids',
                     # 'Taxes',
                     'IncomeTaxPaid',
                     'IncomeTaxesPaidNet',
                     'InterestAndIncomeTaxesPaid',
                     'IncomeTaxes',
                     'IncomeTax1',
                     'TaxesPaid1',
                     'IncomeTaxesPaidOther',
                     'IncomeTaxesPaidState',
                     'IncomeTax'
                 ],

                 'net earnings': [
                     'NetEarnings',
                     'NetEarnings1',
                     'NetEarning',
                 ],

                 'cash and short-term investments': [
                     'Cash',
                     'ShortTermInvestments',
                     # 'Investments',
                     # 'Investment',
                     # 'Investments1',
                     # 'Investmentsbs',
                     # 'InvestmentsIn',
                     # 'InvestmentsBS',
                     # 'Investment1',
                 ],

                 'total inventory': [
                     'TotalInventory',
                     'InventoryTotal',
                     # 'Inventory',
                     # 'Inventory1',
                     # 'Inventorys',
                     'TotalInventories',
                     # 'LotInventory'
                 ],

                 'total receivables, net': [
                     'Receivables',
                     'Receivable',
                     'TotalReceivable',
                     'ReceivablesNet',
                     # 'OtherReceivablesNet',
                     # 'Tradereceivablesnet',
                     # 'NotesReceivablesNet',
                     # 'TradeReceivablesNet',
                     # 'ContractReceivablesNet',
                     # 'NoteReceivableNet'
                 ],

                 'prepaid expenses': [
                     'PrepaidExpenses',
                     'PrepaidExpenses3',
                     'PrepaidExpenses1',
                     'PrepaidExpense',
                     'PrepaidExpense1',
                     # 'Prepaid',
                 ],

                 'other current assets, total': [
                     'TotalOtherCurrentAssets'
                     # 'OtherNoncurrentAssetsTotal',
                     'OtherCurrentAssets',
                 ],

                 'total current assets': [
                     'Totalcurrentassets',
                     'TotalCurrentAssets',
                     'TOTALCURRENTASSETS',
                     'TotalCurrentAssets1',
                     'CurrentAssets',
                     'CurrentAsset',
                     # 'NetAssets',
                     # 'NETASSETS'
                     # 'TotalNoncurrentAssets',
                     # 'TotalNoncurrent_Assets',
                 ],

                 'property/plant/equipment': [
                     'PropertyPlantEquipment',
                     'PropertyPlantAndEquipment',
                     'PropertyPlantEquipmentNet',
                     'PropertyAndEquipment',
                 ],

                 'goodwill, net': [
                     'GoodwillNet',
                     'Goodwill',
                     # 'GoodwillNetOfCashAcquired',
                     'Goodwill1',
                     # 'GoodwillLineItems',
                     'Goodwill3'
                 ],

                 'intangibles, net': [
                     'Intangibles',
                     'IntangiblesNet',
                 ],

                 'long-term investments': [
                     'LongTermInvestments',
                     'LongTermInvestment',
                     'InvestmentsLongTerm',
                     # 'PaymentsForProceedsFromLongtermInvestments',
                     # 'PaymentsToAcquireLongtermInvestments',
                     # 'Investments1',
                     # 'PrepaymentsForPurchaseOfLongTermInvestments',
                     # 'PaymentsForAdvancesToAcquireLongTermInvestments'
                 ],

                 'other assets': [
                     'OtherAssets',
                     'OtherAssets1',
                     'OtherAssets3',
                     'OtherAssets2',
                     'AssetsOther',
                     'OtherAsset',
                     'OtherAssts',
                     'OtherAssetsBS',
                     'OtherAssetsCF',
                     'OtherAssetsNc',
                     'OfOtherAssets',
                     'DeferredChargesAndOtherAssets',
                 ],

                 'total assets': [
                     'Totalassets',
                     'TotalAssets',
                     'TotalAssets1',
                     'AssetsTotal',
                     # 'Assets',
                     # 'RestrictedTotalAssets',
                     # 'SubtotalAssets',
                 ],

                 'accounts payable': [
                     'AccountsPayable',
                     'AccountsPayable1',
                     'AccountsPayables',
                     'AccountsPayable3',
                     'AccountsPayable2',
                     'AcountsPayable',
                     'AccountPayable',
                     'AccountsPayable31',
                     'AcountsPayable1',
                     'AccountantsPayable',
                     'AccountsPayableNet',
                     # 'IncreaseDecreaseInAccountsPayable',
                     # 'IncreaseDecreaseInOtherAccountsPayable'
                 ],

                 'accrued expenses': [
                     'Accruedexpenses',
                     'AccruedExpenses',
                     'AcccruedExpenses',
                     'AccruedExpenses1',
                     'Accrued_expenses',
                     'AccruedExpenses3',
                     'AccruedExpense',
                     'AccruedExpenses11',
                     'AccruedExpensesNet',
                     # 'RelatedPartyPayableAndAccruedExpenses'
                 ],

                 'short-term debt': [
                     'ShortTermDebt',
                     # 'ProceedsFromShortTermDebt',
                     'ShortTermDebtnet',
                 ],

                 'long-term debt due': [
                     'LongtermDebtDue'
                 ],

                 'other current liabilities': [
                     'OtherCurrentLiabilities',
                     'OtherCurrentLiablities',
                     'TotalOtherCurrentLiabilities',
                     'OtherNoncurrentLiabilities',
                     # 'Othercurrenttaxliabilities',
                     # 'OtherNonCurrentLiabilities',
                     'TotalOtherCurrentLiabilities',
                 ],

                 'total current liabilities': [
                     'TotalCurrentLiabilities',
                     'TOTALCURRENTLIABILITIES',
                     'TotalCurrentLiabilities1',
                     'TotalCurrentLiabilties',
                     'CurrentLiabilitiesTotal',
                     # 'TotalNoncurrentLiabilities',
                     # 'NoncashOrPartNoncashAcquisitionTotalCurrentLiabilities',
                 ],

                 'long-term debt': [
                     'LongTermDebt',
                     'LongtermDebt',
                     # 'Debt',
                     'LongTermDebts',
                     'DebtLongTerm',
                 ],

                 'deferred income tax': [
                     'DeferredIncomeTax',
                     'DeferredIncomeTaxes',
                     'Deferredincometaxes',
                     # 'DeferredIncome',
                 ],

                 'minority interest': [
                     'MinorityInterest',
                     'MinorityInterest1',
                     'MinorityInterests',
                     'MinorityInterest2',
                     'MinorityInterestOne',
                     # 'PaymentsOfDividendsMinorityInterest',
                     # 'PaymentOfSpecialDividendMinorityInterest',
                     # 'BusinessAcquisitionMinorityInterest',
                     # 'AcquisitionOfMinorityInterest',
                     # 'InvestmentInMinorityInterest',
                     # 'Paymentsofdividendsandredemptionsminorityinterest'
                 ],

                 'other liabilities': [
                     'OtherLiabilities',
                     'OtherLiabilities1',
                     'OtherLiabilites',
                     'LiabilitiesOther',
                     'OfOtherLiabilities',
                     # 'Other',
                     'OtherTaxLiabilities',
                     'AllOtherLiabilities',
                     'VIEOtherLiabilities',
                     # 'OtherTaxliabilities',
                     'OtherLiabilitiesNet',
                     'AboveMarketLeasesandOtherLiabilities',
                     'AccruedLiabilitiesAndOtherLiabilities',
                     'DeferredCreditsAndOtherLiabilities'
                 ],

                 'total liabilities': [
                     'TotalLiabilities',
                     'TOTALLIABILITIES',
                     'LiabilitiesTotal',
                     'Liabilities',
                     # 'SubTotalLiabilities',
                     # 'RestrictedTotalLiabilities',
                     # 'Totalliabilitiesnotsubjecttocompromise',
                     # 'TotalLiabilitiesExclusiveOfLiabilitiesUnderVehiclePrograms',
                     'TotalLiabilitiesAndShareholders'
                 ],

                 'preferred stock': [
                     'Preferredstock',
                     'PreferredStock',
                     'PreferredAStock',
                     'PreferredBStock',
                     'Preferredstock1',
                     'PreferredCStock',
                     'Preferredstock2',
                     'PreferredStockA',
                     'PreferredStockB',
                     'N5PreferredStock',
                     # 'AdditionalPaidInCapitalPreferredStock'
                 ],

                 'common stock': [
                     'CommonStock',
                     'Commonstock',
                     'CommonStockT',
                     'CommonStock1',
                     'Commonstock1',
                     'CommonStock2',
                     'CommonStocksT',
                     # 'AccruedPurchaseOfCommonStock',
                     # 'AdditionalPaidInCapitalCommonStock',
                     # 'DividendsCommonStock',
                     # 'PaymentsForRepurchaseOfCommonStock',
                     # 'PaymentsOfDividendsCommonStock'
                 ],

                 'additional paid in capital': [
                     'AdditionalPaidInCapital',
                     'AdditionalPaidinCapital',
                     'AdditionalPaidInCapital1',
                     'AdditionalPaidInCapital2',
                     'AdditionalPaidinCapitals',
                     'AdditionalPaidInCapital3',
                     'AdditionalPaidInCapital4',
                     'AdditionalPaidInCapital5',
                     'AdditionalPaidInCapitals',
                     'AdditonalPaidInCapital1',
                     'AdditonalPaidInCapital2',
                     'AdditonalPaidInCapital3',
                     'AdditionPaidInCapital',
                     # 'AdditionalPaidInCapitalBcf'
                 ],

                 'retained earnings': [
                     'RetainedEarnings',
                     'Retained-Earnings-Other',
                     # 'RetainedEarningsEnd',
                     # 'CumulativeAdjustmentToRetainedEarnings',
                     # 'RestrictedRetainedEarnings',
                     # 'VariableInterestEntityRetainedEarnings',
                     # 'DividendEquivalentSharesAddedToRestrictedStockUnitsRetainedEarnings'
                 ],

                 'treasury stock-common': [
                     'CommonStockInTreasury',
                     'TreasuryStockCommonValue',
                     'TreasuryStock1',
                     'TreasuryStock2',
                     'TreasuryStocks',
                     'TreasuryStockCommonShares',
                     'TreasuryStockCommonMember'
                 ],

                 'other equity': [
                     'OtherEquity',
                     'OtherEquity1',
                     'EquityOther',
                     # 'PaymentsForRepurchaseOfOtherEquity',
                     'ProceedsFromOtherEquity',
                     'TreasuryStockAndOtherEquity',
                     'IncomeLossfromOtherEquityMethodInvestments',
                     'ProceedsFromShareBasedAwardsAndOtherEquityTransactions',
                     'OtherEquityMethodInvestmentsMember'
                 ],

                 'total shareholders equity': [
                     'TotalShareholdersEquity',
                     'TOTALSHAREHOLDERSEQUITY1',
                     # 'Equity',
                     'TotalCommonShareholdersEquity',
                     # 'TotalShareholdersEquityMember',
                     # 'TotalParentShareholdersEquity',
                     'ShareholdersEquity',
                     # 'TotalShareholdersEquityDeficit',
                     'TotalShareholdersEquityIncludingTreasuryStock',
                     # 'OtherShareholdersEquity',
                     # 'TotalShareholdersEquityAttributableToParentMember'
                 ],

                 'total liabilities and shareholders equity': [
                     'TotalLiabilitiesAndShareholdersEquity',
                     'TotalLiabilitiesAndShareholdersEquity1',
                     'TotalLiabilitiesShareholdersEquity',
                     'Liabilities',
                     'TotalLiabilitiesAndShareholders',
                     'TotalLiabilitiesAndStocholdersEquity',
                     'TotalLiabilitiesAndShareholdersDeficit',
                     'ShareholdersEquity',
                     'TotalLiabilities',
                     'TOTALLIABILITIES',
                     'TotalLiabilitiesAndStockholdersEquity',
                     'Liabilities1',
                     'TotalLiabilitiesAndStockholderEquity',
                     'TotalLiabilitiesandSe'
                 ],

                 'net income': [
                     'NetIncome',
                     'Netincome',
                     'NetIncome1',
                     'NetIncome2',
                     'Netincome1',
                     'NetIncome3',
                     'NetIncome4',
                     'NetIncome5',
                     # 'Net',
                 ],

                 'amortization': [
                     'Amortization',
                     # 'AmortizationandImpairmentofIntangibleAssets',
                     # 'AmortizationOfAcquiredIntangibleAssets1',
                     # 'AmortizationOfDeferredLeaseIncentives',
                     # 'AmortizationOfInvestmentSecurities',
                     # 'InterestExpenseAndAmortizationOfDeferredFinancingCostsThirdParty',
                     ],

                 'total cash from operating activities': [
                     # 'Operating',
                     'TotalCashFlowsFromOperatingActivities',
                     'OperatingActivities',
                     'NetCashFromOperatingActivities',
                     'TotalProceedsFromOperatingActivities',
                     # 'TotalOtherOperatingActivities',
                     'CashFlowsFromOperatingActivities',
                     # 'OtherCashFlowsFromOperatingActivities',
                     'ProfitLossFromOperatingActivities',
                     'ProceedsFromOperatingActivities',
                     'CashFlowsFromOperationgActivities',
                 ],

                 'capital expenditures': [
                     'CapitalExpenditures',
                     'Capitalexpenditures',
                     'CapitalExpenditure',
                     'CapitalExpendituresNet',
                     'NetCapitalExpenditures',
                     # 'IncreaseDecreaseinAccruedCapitalExpenditures',
                     # 'ChangeInAccruedCapitalExpenditures',
                     # 'ChangesInAccruedExpensesRelatedToCapitalExpenditures',
                     # 'IncreaseDecreaseInAccruedCapitalExpenditures',
                     # 'PaymentsForFinancedCapitalExpenditures',
                     # 'AccrualAssociatedWithConstructionAndCapitalExpenditures',
                     # 'ChangeInAccrualsOrLiabilitiesForCapitalExpenditures',
                     # 'NoncashorPartNoncashAccruedCapitalExpenditures',
                     # 'ChangeinLiabilityforCapitalExpenditures'
                 ],

                 'other investing cash flow items': [
                     'OtherInvesting',
                     'InvestingCashFlows',
                     'CashFlowsInvesting',
                     'OtherInvestment',
                     'CashFlowsFromInvestingActivitiesOther',
                     'Otherinvestingactivities',
                     # 'TotalNoncashInvestingActivities',
                     # 'Non-CashInvestingActivities',
                     # 'NonCashInvestingActivities',
                 ],

                 'total cash from investing activities': [
                     'TotalCashFlowsFromInvestingActivities',
                     'InvestingActivities',
                     'CashFlowFromInvestingActivities',
                     'CashFlowsFromInvestingActivities',
                     'ProceedsFromInvestingActivities',
                     'DepositsFromInvestingActivities',
                 ],

                 'cash dividends paid': [
                     'CashDividendsPaid',
                     'CashDividendPaid',
                     'Dividends',
                     'Dividend',
                     'CashDividendsRepaid',
                     # 'NoncashDividendsPaid',
                     'CashDividend',
                     'Dividendsd',
                     'DividendsPaid',
                     'CashDividends',
                     'Dividends1',
                     'Dividendspaid'
                 ],

                 'issuance retirement of stock, net': [
                     'RetirementOfStock',
                     # 'RepaymentOfStock',
                ],

                 'issuance retirement of debt, net': [
                     # 'Issuance',
                     'RetirementOfDebt',
                     'IssuanceForSettlementOfDebtAmount',
                     # 'RepaymentOfDebt',
                     'DebtRetirement',
                     'IssuanceForSettlementOfDebtShares',
                     # 'LossOnRetirementOfDebt',
                     'RetirementOfAssets'
                 ],

                 'total cash from financing activities': [
                     'TotalCashFlowsFromFinancingActivities',
                     'FinancingActivities',
#                     'TotalNoncashFinancingActivities',
                     'CashFlowFromFinancingActivities',
#                     'TotalCash',
                     'CashFlowsFromFinancingActivities',
                     'GainLossFromFinancingActivities',
#                     'NonCashFinancingActivities',
#                      'OtherFinancingActivities'
                 ],

                 'net change in cash': [
                     'NetChangeInCash',
                     'NETCHANGEINCASH',
                     'ChangeInCash',
                     'ChangeInCash1',
                     'ChangeInCash2',
                     'ChangeInCash4',
                     'ChangeInCash3'
                 ]
             }

    @staticmethod
    def extract_cik_numbers():
        res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')

        cik_map = {}

        for quarter_dir in reversed(os.listdir(res_dir)):

            quarter_dir = os.path.join(res_dir, quarter_dir)

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
    def organize_tags():
        res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')
        all_tags = pd.Series()

        for quarter_dir in reversed(os.listdir(res_dir)):

            quarter_dir = os.path.join(res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            tag_file = os.path.join(quarter_dir, 'tag.txt')
            tags = pd.read_csv(tag_file, sep='\t', encoding='utf-8', quoting=csv.QUOTE_NONE, usecols=['tag'])
            all_tags = all_tags.append(tags)

        all_tags = all_tags['tag'].unique().tolist()

        # target_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'tags.txt')
        #
        # with open(target_file_path, 'a') as f:
        #     for item in all_tags:
        #         f.write("%s\n" % item)

        target_file_path = os.path.join(os.path.abspath(os.getcwd()), 'resources', 'tags_organized.txt')

        for title in XBRLDataSetProvider.titles.keys():

            title = title.replace('&', 'and')

            result = process.extract(title, all_tags, limit=15)
            with open(target_file_path, 'a') as f:
                f.write("\n%s:\n" % title)
                for item in result:
                    f.write("%s - %s\n" % (item[0], str(item[1])))

    @staticmethod
    def organize_data_set(dir_separator='\\'):

        res_dir = os.path.join(os.path.abspath(os.getcwd()), 'scrapy', 'xbrl_output')
        output_dir = os.path.join(os.path.abspath(os.getcwd()), 'output', 'xbrl_organized')

        all_quarters = os.listdir(res_dir)
        all_quarters.remove('.gitignore')

        all_ciks = []

        for quarter_dir in os.listdir(res_dir):

            quarter_dir = os.path.join(res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            sub_file = os.path.join(quarter_dir, 'sub.txt')
            subs = pd.read_csv(sub_file, sep='\t', encoding='ISO-8859-1', usecols=['cik'])
            all_ciks = all_ciks + subs['cik'].tolist()

        all_ciks = set(all_ciks)

        # all_data = np.empty((len(all_quarters), ))
        index = pd.MultiIndex.from_product([all_quarters, all_ciks], names=['quarter', 'cik'])
        all_data = pd.DataFrame(index=index, columns=XBRLDataSetProvider.titles.keys())
        pd.options.mode.chained_assignment = None

        for quarter_dir in os.listdir(res_dir):

            quarter_dir = os.path.join(res_dir, quarter_dir)

            if not os.path.isdir(quarter_dir):
                continue

            quarter_name = quarter_dir.rsplit(dir_separator, 1)[-1]
            print('QUARTER', quarter_name)

            num_file = os.path.join(quarter_dir, 'num.txt')
            sub_file = os.path.join(quarter_dir, 'sub.txt')

            numbers = pd.read_csv(num_file, sep='\t', encoding='ISO-8859-1', usecols=['adsh', 'tag', 'value'])
            subs = pd.read_csv(sub_file, sep='\t', encoding='ISO-8859-1', usecols=['adsh', 'cik', 'name'])
            #
            # all_data[quarter_dir] = pd.DataFrame(index=subs['cik'], columns=XBRLDataSetProvider.titles.keys())
            # all_data[quarter_dir].fillna(0, inplace=True)
            numbers = numbers.merge(subs, on='adsh', how='left')

            # i = 0

            for i, cik in subs['cik'].iteritems():
                print('CIK', cik)
                for fixed_tag, tags in XBRLDataSetProvider.titles.items():
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

                    all_data.loc[(all_data.index.get_level_values('quarter') == quarter_name)
                                 & (all_data.index.get_level_values('cik') == cik), fixed_tag] = val

                # break
            # break

        all_data.fillna(0, inplace=True)

        tensor = all_data.values.reshape((len(all_quarters), len(all_ciks), all_data.shape[1]))
        np.save(os.path.join(output_dir, 'xbrl_data'), tensor)
