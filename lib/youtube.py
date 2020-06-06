# SPDX-License-Identifier: BSD-3-Clause

import argparse
import os
import sys
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import google.auth.transport.requests

class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)

        self.add_argument('-S', '--client-secret', metavar='FILE', type=str,
            help='OAuth client secrets file from Google API Console')
        self.add_argument('-T', '--token', metavar='FILE', type=str,
            help='OAuth token cache')


class Client:
    def __init__(self, secrets_file=None, token_file=None):
        if not token_file:
            token_file = (os.environ['XDG_CACHE_HOME']
                if 'XDG_CACHE_HOME' in os.environ
                else os.path.join(os.environ['HOME'], '.cache'))
            token_file = os.path.join(token_file, 'youtube-remote.pickle')

        # Attempt to load OAuth access and refresh tokens from cache
        creds = None
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(google.auth.transport.requests.Request())
            elif not sys.stdin.isatty():
                raise RuntimeError('invalid OAuth credentials in non-interactive mode')
            elif not secrets_file:
                raise RuntimeError('client_secrets.json file required (-S)')
            else:
                # Run OAuth 2.0 Authorization Flow if no valid credentials
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    secrets_file,
                    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])
                creds = flow.run_console()

            # Save credentials
            mask = os.umask(0o077)
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
            os.umask(mask)

        youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=creds)
        self.streams = youtube.liveStreams()
        self.broadcasts = youtube.liveBroadcasts()

    def stream_id(self, name):
        """Retrieve stream ID from given cdn.ingestionInfo.streamName"""
        # <https://developers.google.com/youtube/v3/live/docs/liveStreams/list>
        req = self.streams.list(part='id,cdn', mine=True)
        resp = req.execute()
        for stream in resp['items']:
            if name == stream['cdn']['ingestionInfo']['streamName']:
                return stream['id']
        raise RuntimeError('stream name not found: ' + name)


