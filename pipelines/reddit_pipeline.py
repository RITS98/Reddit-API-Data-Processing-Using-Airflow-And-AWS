import pandas as pd
from etls.connect_reddit import connect_to_reddit_api, extract_posts, transform_data, load_data_to_csv
from utils.constants import CLIENT_ID, SECRET, OUTPUT_PATH

def extract_reddit_data(file_name, subreddit, time_filter='day', limit=None):

    instance = connect_to_reddit_api(CLIENT_ID, SECRET, 'User-Agent')
    # extraction
    posts = extract_posts(instance, subreddit, time_filter, limit)
    post_df = pd.DataFrame(posts)
    # transformation
    post_df = transform_data(post_df)
    # loading to csv
    file_path = f'{OUTPUT_PATH}/{file_name}.csv'
    load_data_to_csv(post_df, file_path)

    return file_path

