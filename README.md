# Python Automation Scripts

Web scraping with BeautifulSoup/Selenium, file operations (batch rename, clean), API client with retry logic, and cron-like task scheduling. Modular scripts for routine IT work.

## Usage

```python
from src.scraper import WebScraper
scraper = WebScraper()
scraper.scrape_page("https://example.com")
```

```python
from src.file_ops import FileOperations
ops = FileOperations()
ops.batch_rename("/path/to/files", "*.txt", "prefix_")
```

## Project Structure

```
src/
├── scraper.py       # Web scraping
├── file_ops.py      # File operations
├── api_client.py    # API client
└── scheduler.py     # Task scheduling
```

## License

MIT
