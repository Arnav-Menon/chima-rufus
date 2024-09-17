from .scraper import scrape_website

class RufusClient:
    def scrape(self, url, instructions):
        """
        Scrape the given URL for information related to the given instructions.

        Args:
            url (str): The URL to scrape.
            instructions (str): The instructions to follow while scraping.

        Returns:
            list: A list of scraped information.
        """
        if not (isinstance(url, str) and url) or not (isinstance(instructions, str) and instructions):
            raise ValueError("Invalid input type")

        # Scrape the website for information
        return scrape_website(url, instructions)
