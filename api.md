## POST /ticket/new

Create a new analysis ticket.

#### Rate-Limit:

100 requests per 10min/user

#### Query Parameters:

none

#### Headers:

- `Cookie` - session ID
- `Authorization` - Bearer token as alternative to the cookie

Either one is required.

#### Request:

none

#### Response:

```json
{
  "ticket-id": "h9ed-q5d3-2dd7-4f3d"
}
```

#### Status Codes:

- 200: success
- 429: rate-limit exceeded

#### Notes:

- It is possible that a video is never uploaded for a ticket and an empty ID will float around in the DB. All such tickets won't be displayed on the user's profile and will be purged at the end of the week.

## POST /ticket/video

Upload a video file for analysis.

#### Rate-Limit:

10 requests per 10min/user

#### Query Parameters:

- `ticket-id`

#### Headers:

- `Cookie` - session ID
- `Authorization` - Bearer token as alternative to the cookie
- `Content-Type`=`application/octet-stream`

#### Request:

octet-stream, video file

#### Response:

```json
{
  "status": "success" // or "bad-ticket", "failed-upload", "invalid-video", "too-long", "internal-error", etc...
}
```

#### Status Codes:

- 200: success
- 400: bad ticket, failed upload, invalid video, too long, etc...
- 401: unauthorized, bad session or token
- 429: rate-limit exceeded

#### Notes:

- Both on client-side and server-side, limit video file to 1GiB. The video file is uploaded as-is since client-side compression is not feasible.
- Video is compressed and split into 10s fragments, and stored in a temporary bucket storage under the generated ticket ID.
- The compression and fragmentation params should be available in server-side config: `res=480p`, `vb=500k`, `va=128k`, `frag=10s`.
- Video will be available for streaming on the results page for a limited time, after which it will be deleted and only textual results will be available.
- At any point, it can be re-uploaded to replace the current video file. There's no guard rail against uploading a completely different video file. Expect the results of new analyses to be inconsistent in that case.

## GET /ticket/stream

Get a video file fragment for streaming.

#### Rate-Limit:

This endpoint can be viewed by guests, but different rate limits apply to them.

Active rate limits:

- 100 authorized requests per 1min/user
- 20 unauthorized requests per 1min/guest
- 20 unauthorized requests per 1min/ticket

#### Query Parameters:

- `ticket-id`
- `time` - time at which to get the current fragment

#### Headers:

- `Cookie` - **OPTIONAL** session ID
- `Authorization` - **OPTIONAL** Bearer token as alternative to the cookie

#### Request:

none

#### Response:

**Normally:**
octet-stream, video file

**In case of an error:**

```json
{
  "status": "not-uploaded" // or "bad-ticket", "bad-time", "internal-error", etc...
}
```

#### Status Codes:

- 200: success
- 400: bad ticket, bad time, etc...
- 404: not found, video was never uploaded
- 429: rate-limit exceeded

#### Notes:

- Fragment length can be read from metadata of the first fetched fragment. Then, knowing that the first fragment in order starts at `0.0s`, client can deduce when every fragment begins and ends. This knowledge will allow it to compute the `time` of desired fragments.
- If 200 is returned and there's no content, it means the video is being uploaded or processed. Client should retry after a short delay.
- 404 means the video was never uploaded for the ticket. Client may retry uploading the video.

## POST /ticket/analyze

Request an analysis type for a ticket.

#### Rate-Limit:

100 requests per 10min/user

#### Query Parameters:

- `ticket-id`
- `type` - analysis type, e.g. `quality-summary`

#### Headers:

- `Cookie` - session ID
- `Authorization` - Bearer token as alternative to the cookie

#### Request:

none

#### Response:

```json
{
  "status": "success", // or "bad-ticket", "bad-type", "already-analyzed", "internal-error", etc...
  "request-deps": ["transcription", "audio-gaps"] // or []
}
```

#### Status Codes:

- 200: success
- 400: bad ticket, bad type, already analyzed, etc...
- 401: unauthorized, bad session or token
- 429: rate-limit exceeded

#### Notes:

- If the analysis type is dependent on other analyses, the response will include the types that were automatically requested as a side-effect.

## GET /ticket/status

Get the results or statuses of different types of analysis for a ticket.

#### Rate-Limit:

This endpoint can be viewed by guests, but different rate limits apply to them.

Active rate limits:

- 100 authorized requests per 10min/user
- 20 unauthorized requests per 10min/guest
- 20 unauthorized requests per 10min/ticket

#### Query Parameters:

- `ticket-id`
- `send-results` - boolean, whether to send the results of finished analyses

#### Headers:

- `Cookie` - **OPTIONAL** session ID
- `Authorization` - **OPTIONAL** Bearer token as alternative to the cookie

#### Request:

none

#### Response:

Without `send-results`:

```json
{
  "transcription": 0.5, // in-progress
  "audio-gaps": {} // finished, no results sent
}
```

With `send-results`:

```json
{
  "transcription": 0.5, // in-progress
  "audio-gaps": {
    "gaps": [
      {
        "start": 0.125,
        "end": 1.07
      },
      {
        "start": 3.15,
        "end": 5.82
      }
    ]
  } // finished, here are the results
}
```

#### Notes:

Usage:

1. On initial page display, this endpoint is requested to get the results of finished analyses and the progress of any pending analyses.
2. If there are any pending analyses, the page periodically polls this endpoint with `send-results=false` to check if any new results are available.
3. Whenever a new analysis reports status of type object `{}`, the page polls this endpoint once more with `send-results=true` to get the results.
4. If there are no more pending analyses, the page displays the results and stops polling until the user requests a new analysis. Otherwise rinse and repeat.

Analyses not included in the response are assumed to be available to be requested.

More analysis types:

- `transcription`
- `audio-gaps`
- `noise-detection`
- `language-complexity`
- `background-actors`
- `...`

## POST /ticket/delete

Delete a ticket and all its associated data. You must be the owner of the ticket.

#### Rate-Limit:

100 requests per 10min/user

#### Query Parameters:

- `ticket-id`

#### Headers:

- `Cookie` - session ID
- `Authorization` - Bearer token as alternative to the cookie

#### Request:

none

#### Response:

```json
{
  "status": "success" // or "bad-ticket", "internal-error", etc...
}
```

#### Status Codes:

- 200: success
- 400: bad ticket, etc...
- 401: unauthorized, bad session or token
- 429: rate-limit exceeded

## POST /ticket/cancel

Cancel an analysis request for a ticket. You must be the owner of the ticket.

#### Rate-Limit:

100 requests per 10min/user

#### Query Parameters:

- `ticket-id`
- `type` - analysis type, e.g. `quality-summary`, cancel all if not specified

#### Headers:

- `Cookie` - session ID
- `Authorization` - Bearer token as alternative to the cookie

#### Request:

none

#### Response:

```json
{
  "status": "success" // or "bad-ticket", "bad-type", "not-analyzed", "internal-error", etc...
}
```

#### Status Codes:

- 200: success
- 400: bad ticket, bad type, not analyzed, etc...
- 401: unauthorized, bad session or token
- 429: rate-limit exceeded
