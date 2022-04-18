import googleapiclient.discovery
import pandas as pd

# api_key
api_service_name = 'youtube'
api_version = 'v3'

# create api service
youtube = googleapiclient.discovery.build(
    serviceName=api_service_name,
    version=api_version,
    developerKey=api_key)

def get_channel_stats(parameter, channel_id_tags):
    # create request using build service
    request = youtube.channels().list(
        part = ','.join(parameter),
        id = channel_id_tags)

    # get response
    response = request.execute()
    
    # create channel dict statistics
    channel_data = dict(
        channel_name = response['items'][0]['snippet']['title'],
        subsciber = response['items'][0]['statistics']['subscriberCount'],
        total_views = response['items'][0]['statistics']['viewCount'],
        total_videos = response['items'][0]['statistics']['videoCount'],
        channel_country = response['items'][0]['snippet']['country'])

    return pd.DataFrame([channel_data])

def get_channel_playlistitems(parameter, playlist_id_tags, total_video_output=50):
    # create request service for playlistItems
    request = youtube.playlistItems().list(
        part = ','.join(parameter),
        playlistId = playlist_id_tags,
        maxResults = total_video_output)
    
    # get response for video id
    response = request.execute()
    
    # create list to retrieve video ids
    all_video_ids = []
    for item in response['items']:
        all_video_ids.append(item['contentDetails']['videoId'])

    # create code using while loop to get more video id
    # in next page using page token parameter
    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request_playlistItems_loop = youtube.playlistItems().list(
                part = ','.join(parameter),
                playlistId = playlist_id_tags,
                maxResults = total_video_output,
                pageToken = next_page_token)
            response_playlistItems_loop = request_playlistItems_loop.execute()

            for item in response_playlistItems_loop['items']:
                all_video_ids.append(item['contentDetails']['videoId'])
            
            next_page_token = response_playlistItems_loop.get('nextPageToken')
    
    return all_video_ids