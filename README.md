# Python Automation Scripts
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


Comprehensive IT automation toolkit featuring web scraping, file operations, API integrations, and system administration scripts.

## Description

Production-ready automation library for common IT tasks including web scraping with BeautifulSoup and Selenium, file operations, API integrations, and system administration. Each module is designed to be reusable and configurable.

## Skills & Technologies

- Python 3.9+
- Requests
- BeautifulSoup
- Selenium
- Pandas
- Schedule/Cron
- API Integration
- File Operations

## Installation

```bash
git clone https://github.com/AmirAsaad/python-automation-scripts.git
cd python-automation-scripts
pip install -r requirements.txt
```

## Usage

### Web Scraping

```python
from src.scraper import WebScraper

scraper = WebScraper()
scraper.scrape_page("https://example.com")
```

### File Automation

```python
from src.file_ops import FileOperations

ops = FileOperations()
ops.batch_rename("/path/to/files", "*.txt", "prefix_")
```

## Project Structure

```
python-automation-scripts/
├── src/
│   ├── scraper.py           # Web scraping
│   ├── file_ops.py          # File operations
│   ├── api_client.py         # API client
│   └── scheduler.py          # Task scheduling
├── requirements.txt
└── README.md
```

## References

- [Requests Documentation](https://docs.python-requests.org/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)

## License

MIT License
