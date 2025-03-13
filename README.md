# Map Scraper

A modern, efficient Google Maps scraper built with Python and Selenium. This tool allows you to extract detailed business information and reviews based on location and business type searches.

## 🌟 Features

- **Business Information Extraction**
  - Business name and address
  - Contact information (phone, website)
  - Ratings and review counts
  - Detailed review data

- **Smart Data Collection**
  - Configurable number of results
  - Automatic scrolling
  - Cookie consent handling
  - Error recovery and retries

- **Rich Output**
  - Excel workbook generation
  - Separate sheets for businesses and reviews
  - Formatted and styled output
  - Auto-adjusted column widths

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Git (for development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Fabi0za/Map-Scraper.git
   cd Map-Scraper
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Chrome WebDriver:
   ```bash
   # The webdriver-manager package will handle this automatically
   ```

## 📖 Usage

### Basic Usage

Run the scraper with basic options:
```bash
python -m modules.run "Ansbach" "electrician" --max-results 20
```

### Command Line Options

- `location`: Location to search in (e.g., "Ansbach")
- `business_type`: Type of business to search for (e.g., "electrician")
- `--max-results`: Maximum number of results to scrape (default: 20)
- `--output`: Custom output file path (default: businesses_TIMESTAMP.xlsx)
- `--headless`: Run Chrome in headless mode
- `--verbose`: Enable verbose logging

### Examples

1. Search for 30 restaurants in Berlin:
   ```bash
   python -m modules.run "Berlin" "restaurant" --max-results 30
   ```

2. Search in headless mode with custom output:
   ```bash
   python -m modules.run "Munich" "hotel" --headless --output hotels.xlsx
   ```

## 📊 Output Format

The scraper generates an Excel workbook with two sheets:

1. **Businesses Sheet**
   - Business Name
   - Street Address
   - Postal Code
   - City
   - Phone
   - Website
   - Average Rating
   - Number of Reviews

2. **Reviews Sheet**
   - Business Name
   - Review Text
   - Rating
   - Time Posted
   - Positive Points
   - Negative Points
   - Services Used

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes following our conventions
4. Push to your branch
5. Create a Pull Request

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

#### Types
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

#### Scopes
- `scraper`: Core scraping functionality
- `config`: Configuration and settings
- `selectors`: HTML/CSS selectors
- `data`: Data models and structures
- `utils`: Utility functions
- `docs`: Documentation
- `tests`: Test suite

Example:
```
feat(scraper): add support for multiple search queries

- Add queue system for managing multiple queries
- Implement concurrent processing
- Add rate limiting to prevent detection

Fixes #123
```

## 🔧 Troubleshooting

### Common Issues

1. **Selector Errors**
   - Error: "Element not found"
   - Solution: Google Maps UI might have changed. Check for selector updates.

2. **Rate Limiting**
   - Error: "Too many requests"
   - Solution: Increase delays between requests or use proxies.

3. **Chrome Driver Issues**
   - Error: "Chrome driver not found"
   - Solution: Ensure Chrome is installed and up to date.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- GitHub: [@Fabi0za](https://github.com/Fabi0za)

## 🙏 Acknowledgments

- [Selenium](https://www.selenium.dev/) for web automation
- [OpenPyXL](https://openpyxl.readthedocs.io/) for Excel file handling