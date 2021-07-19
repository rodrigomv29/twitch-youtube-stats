import requests

def get_channel_id(api_key):
    channel = input("Enter channel name: ")
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&maxResults=1&q=" + channel + "&key=" + api_key

    response = requests.get(url)
    data = response.json()
    return (data['items'][0]['id']['channelId'])

def get_stats(channel_id, api_key):
    url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet&part=statistics&id=' + channel_id + "&key=" + api_key
    response = requests.get(url)
    data = response.json()
    return data
    
def main():
    api_key = "AIzaSyCdon2Ht4qsO50eVJpu9nJO5iJx7TSIOhM"
    channel_id = get_channel_id(api_key)
    stats = get_stats(channel_id, api_key)
    print(stats)
    
    
if __name__ == "__main__":
    main()

