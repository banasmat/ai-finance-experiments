## Scrape hist data
`cd scrapy && scrapy crawl histdata`

## Merge scraped csvs
`cd scrapy && python HistDataNormalizer.py`

## Conda environment
save: `conda list --explicit > spec-file.txt`
install: `conda install --name nn --file spec-file.txt`

## Links

### Stock symbols/names
* http://eoddata.com/symbols.aspx