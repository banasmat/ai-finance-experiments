## Scrape hist data
`cd scrapy && scrapy crawl histdata`

## Merge scraped csvs
`cd scrapy && python HistDataNormalizer.py`

## Scrape fundamentals from yahoo finance
`cd scrapy && scrapy crawl yahoo_finance -a start=0 -a end=10`

## Conda environment
save: `conda list --explicit > spec-file.txt`
install: `conda install --name nn --file spec-file.txt`

## Links

### Stock symbols/names
* http://eoddata.com/symbols.aspx