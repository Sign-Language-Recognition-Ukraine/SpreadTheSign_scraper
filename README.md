# SpreadTheSign Scraper README

## Introduction

This project, `SpreadTheSign_scraper`, is designed to scrape video content related to Sign Language from the [SpreadTheSign](https://spreadthesign.com/) website. The scraped data is intended for use in training artificial intelligence models, specifically those focused on sign language recognition and interpretation. The project is licensed under the GNUv3, allowing for redistribution and modification under certain conditions.

## Overview

The scraper operates in two main phases:

1. **Link Scraping Phase**: It navigates through the website, extracting words, links to sign language videos at the SpreadTheSign website of these words, and the local downloaded versions of those SpreadTheSign videos, and their subindices. If a word has multiple video variants, it is disambiguated with a subindex, but this does not mean that words cannot have multiple entries with subindex 0, as the SpreadTheSign website often contains multiple. pages for the same word, though most of these duplicates contain different videos 
2. **Downloading Phase**: Utilizes the scraped links to download the video files, storing them in /videos/ locally for use.

## Dependencies

- Python 3.x
- Requests library (`requests`)
- BeautifulSoup4 library (`bs4`)
- Time library (`time`)
- CSV library (`csv`)
- urllib (`urllib.request`)
- OS library (`os`)
- Regular Expressions (`re`)

## Usage

### Configuration

Before running the script, configure the `SCRAPE_LINKS` and `DOWNLOAD_LINKS` variables at the top of the script. Setting `SCRAPE_LINKS` to `True` triggers the scraping phase, while setting `DOWNLOAD_LINKS` to `True` after triggers the downloading phase after the initial scraping.

### Running the Script

To run the script, execute it using a Python interpreter. Ensure all dependencies are installed before running.

### Notes

- The script is designed to handle a specific range of URLs. Adjust this range according to the language/dataset preview size you wish to scrape.
- The script includes error handling for cases where video sources are unavailable or cannot be downloaded.
- Downloaded videos are stored in the `videos` directory. 

## Contributing

Contributions to improve the functionality, efficiency, or accuracy of the scraper are welcome. 

## License

This project is licensed under the GNU General Public License v3.0. For more information, please refer to the LICENSE file included in the repository.

## Contact

For inquiries or feedback regarding this project, please contact the author at uslrecognition@gmail.com. For inquiries or feedback regarding SpreadTheSign, view contacts listed on https://spreadthesign.com/.
