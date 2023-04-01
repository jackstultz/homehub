#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 23:11:18 2023

@author: jackstultz
"""

import datetime
import feedparser
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = '/Users/jackstultz/Downloads/home-hub-382317-fc58301dc348.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

calendar_service = build('calendar', 'v3', credentials=credentials)

CBC_PEI_FEED_URL = 'https://www.cbc.ca/cmlink/rss-canada-pei'
BBC_NEWS_FEED_URL = 'http://feeds.bbci.co.uk/news/rss.xml'



def get_upcoming_events():
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events_result = calendar_service.events().list(calendarId='mjtstultz@gmail.com', timeMin=now,
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{start}: {event['summary']}")

if __name__ == "__main__":
    get_upcoming_events()


def fetch_and_display_news(feed_url, source_name, max_articles=5):
    news_feed = feedparser.parse(feed_url)
    
    print(f"\n{source_name} - Top {max_articles} articles:")
    for i, entry in enumerate(news_feed.entries[:max_articles]):
        print(f"{i+1}. {entry.title}")
        print(f"   Link: {entry.link}\n")

if __name__ == "__main__":
    fetch_and_display_news(CBC_PEI_FEED_URL, "CBC PEI")
    fetch_and_display_news(BBC_NEWS_FEED_URL, "BBC News")
