from src.client import RufusClient

if __name__ == "__main__":

    client = RufusClient()

    instructions = "Give me all information about the Sacramento Kings"

    documents = client.scrape("https://www.nba.com", instructions)
    print(documents)