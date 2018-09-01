# AI finance experiments
Project containing multiple experiments on usage of machine learning with finance data.
The ideas were following:
* Predicting forex price changes taking into account forex calendar news using simple neural network and recurrent one.
* Trading on forex using reinforcement learning.
* Predicting stocks price changes based on financial statements analysis with neural networks.

None of the experiments brought satisfying results but the main goal of learning some python and machine learning by the
 author has been reached. Although for the time being, the project is not well organized and not easily ready to use, 
 someone might find some parts of it useful for own experiments. It contains a collection of scripts that can be used for
 gathering financial data and transforming it to a form that can be used by ML algorithms.
 
## Helpful commands examples

### Scrape forex historical prices data
`cd scrapy && scrapy crawl histdata`

### Merge scraped csv files (forex historical prices)
`cd scrapy && python HistDataNormalizer.py`

### Scrape fundamentals from yahoo finance
`cd scrapy && scrapy crawl yahoo_finance -a start=0 -a end=10`

### Conda environment
save: `conda list --explicit > spec-file.txt`
install: `conda install --name nn --file spec-file.txt`

## Links

### Stock symbols/names
* http://eoddata.com/symbols.aspx