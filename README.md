## rocketchat_API
Python API wrapper for [Rocket.Chat](https://rocket.chat/docs/developer-guides/rest-api)

### Installation
- From pypi:
`pip3 install rocketchat_API`
- From GitHub:
Clone our repository and `python3 setup.py install`

### Requirements
- [requests](https://github.com/kennethreitz/requests)==2.13.0

### Usage
```
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

proxyDict = {
              "http"  : "http://127.0.0.1:3128",
              "https" : "https://127.0.0.1:3128",
            }

rocket = RocketChat('user', 'pass', server_url='https://demo.rocket.chat', proxies=proxyDict)
pprint(rocket.me().json())
pprint(rocket.channels_list().json())
pprint(rocket.chat_post_message('good news everyone!', channel='GENERAL', alias='Farnsworth').json())
pprint(rocket.channels_history('GENERAL', count=5).json())
```

*note*: every method returns a [requests](https://github.com/kennethreitz/requests) Response object.

### Method parameters
Only required parameters are explicit on the RocketChat class but you can still use all other parameters. For a detailed parameters list check the [Rocket chat API](https://rocket.chat/docs/developer-guides/rest-api)

### API coverage
I've implemented only a few methods until now but I want to make them all. If you are interested in a specific call just open an issue or open a pull request.

*note*: Library updated to work with Rocket.Chat >= 0.58.0

### Tests
No tests have being implemented. If you are interested in writing them please open a pull request.

### Contributing
You can contribute by doing Pull Requests. (It may take a while to merge your code but if it's good it will be merged). We hang out [here](https://demo.rocket.chat/channel/python_rocketchat_api) if you want to talk.
