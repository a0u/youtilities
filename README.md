# YouTilities

Command-line utilites to automate YouTube resources

* `bcast`: [live broadcast](https://developers.google.com/youtube/v3/live/docs/liveBroadcasts) controller
* `stream`: [live stream](https://developers.google.com/youtube/v3/live/docs/liveStreams) controller

## Usage

```sh
$ ./bin/stream add test
xxxx-xxxx-xxxx-xxxx-xxxx
$ ./bin/bcast start "Test Title" xxxx-xxxx-xxxx-xxxx-xxxx
$ ./bin/bcast stop
$ ./bin/stream rm test
```

Streams are reusable across multiple broadcasts.

## Credentials

Follow the [quickstart guide](https://developers.google.com/youtube/v3/quickstart/python)
to create an OAuth 2.0 client ID in the
[Google API console](https://console.developers.google.com/), and then
download the client secrets JSON file.
Its path must be specified with the `-S` option on the initial use of
the tools.

By default, OAuth access and refresh tokens are cached at
`${XDG_CACHE_HOME}/youtube-remote.pickle`, typically
`${HOME}/.cache/youtube-remote.pickle`.
Once authorized, subsequent invocations can be non-interactive.
