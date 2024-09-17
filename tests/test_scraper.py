import unittest
from unittest.mock import patch, MagicMock
from src.scraper import scrape_website
import json
from datetime import datetime

class TestScrapeWebsite(unittest.TestCase):
    @patch('src.scraper.simple_crawl')
    @patch('src.scraper.kw_model.extract_keywords')
    @patch('src.scraper.crawl_links')
    @patch('src.scraper.filter_content')
    @patch('src.scraper.clean_text')
    @patch('src.scraper.sent_tokenize')
    @patch('src.scraper.save_to_json')
    def test_valid_url_and_instructions(self, mock_save_to_json, mock_sent_tokenize, mock_clean_text, mock_filter_content, mock_crawl_links, mock_extract_keywords, mock_simple_crawl):
        url = "https://example.com"
        instructions = "Test instructions"
        mock_simple_crawl.return_value = MagicMock()
        mock_extract_keywords.return_value = [("keyword1", 1), ("keyword2", 2)]
        mock_crawl_links.return_value = ["https://example.com/link1", "https://example.com/link2"]
        mock_filter_content.return_value = ["filtered content"]
        mock_clean_text.return_value = "cleaned content"
        mock_sent_tokenize.return_value = ["sentence1", "sentence2"]
        mock_save_to_json.return_value = None

        result = scrape_website(url, instructions)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertEqual(json.loads(result)["timestamp"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    @patch('src.scraper.simple_crawl')
    def test_invalid_url(self, mock_simple_crawl):
        url = "invalid_url"
        instructions = "Test instructions"
        mock_simple_crawl.return_value = None

        result = scrape_website(url, instructions)
        self.assertIsNone(result)

    @patch('src.scraper.simple_crawl')
    def test_empty_instructions(self, mock_simple_crawl):
        url = "https://nba.com"
        instructions = ""
        mock_simple_crawl.return_value = MagicMock()

        result = scrape_website(url, instructions)
        print("RESULT:", result)
        self.assertIsNone(result)

    @patch('src.scraper.simple_crawl')
    def test_none_input(self, mock_simple_crawl):
        url = None
        instructions = "Test instructions"
        mock_simple_crawl.return_value = MagicMock()

        result = scrape_website(url, instructions)
        self.assertIsNotNone(result)

    @patch('src.scraper.simple_crawl')
    def test_exception_during_scraping(self, mock_simple_crawl):
        """
        Tests that the function returns None if an exception is raised during scraping.

        :param mock_simple_crawl: A mock object for the simple_crawl function.
        """
        url = "https://nba.com"
        instructions = "Test instructions"
        mock_simple_crawl.side_effect = Exception("Test exception")

        result = scrape_website(url, instructions)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()