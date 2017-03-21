## rocketchat_API
Python API wrapper for [Rocket.Chat](https://rocket.chat/docs/developer-guides/rest-api)

### Usage
```
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

rocket = RocketChat('myuser', 'mypassword')
pprint(rocket.me().json())
pprint(rocket.channels_list().json())
pprint(rocket.chat_post_message('GENERAL', 'good news everyone!', alias='Farnsworth').json())
pprint(rocket.channels_history('GENERAL', count=5).json())
```

*note*: every method returns a [requests](https://github.com/kennethreitz/requests) Response object.

### Method parameters
Only required parameters are explicit on the RocketChat class but you can still use all other parameters. For a detailed parameters list check the [Rocket chat API](https://rocket.chat/docs/developer-guides/rest-api)

### API coverage
I've implemented only a few methods until now but I want to make them all. If you are interested in a specific call just open an issue or open a pull request.
*note*: This have being tested only on Rocket.Chat >= 0.52.0

### Tests
No tests have being implemented. If you are interested in writing them please open a pull request.

### Contributing
You can contribute by doing Pull Requests. (It may take a while to merge your code but if it's good it will be merged). We hang out [here](https://demo.rocket.chat/channel/python_rocketchat_api) if you want to talk.
