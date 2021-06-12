## Setup

How to get a token: https://support.plex.tv/articles/201998867-investigate-media-information-and-formats/

Create file `local.yml` at location `plexsnake/snake/config/`. Make sure you set your token in your local.yml, if you 
don't want plexsnake to interact with certain libraries (👀), you can whitelist your libraries in the `local.yml` file 
as well.

Example of `local.yml` file:

```
plex:
  api_endpoint: "http://192.168.33.2:32400"
  token: "tRAjZTXH237yaw2yiKe1"


whitelisted_libraries:
  - "Movies"
  - "Movies - Animated"
  - "Stand-up comedy"
  - "TV"
  - "Sports"
```


## Usage

`python app.py --help`