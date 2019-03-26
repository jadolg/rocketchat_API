## rocketchat_API
Python API wrapper for [Rocket.Chat](https://rocket.chat/docs/developer-guides/rest-api/)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fff725d9a0974c6597c2dd007daaa86e)](https://www.codacy.com/app/jadolg/rocketchat_API?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jadolg/rocketchat_API&amp;utm_campaign=Badge_Grade) [![Build Status](https://travis-ci.org/jadolg/rocketchat_API.png)](https://travis-ci.org/jadolg/rocketchat_API) [![codecov](https://codecov.io/gh/jadolg/rocketchat_API/branch/master/graph/badge.svg)](https://codecov.io/gh/jadolg/rocketchat_API) ![PyPI](https://img.shields.io/pypi/v/rocketchat_API.svg) ![](https://img.shields.io/pypi/dm/rocketchat-api.svg) [![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/jadolg) 

Do you like my library? buy me a 🍺 ➡️ [![Donate Bitcoin](https://img.shields.io/badge/donate-€5-orange.svg)](https://jadolg.github.io/donate-bitcoin/index.html) or [![ko-fi](https://www.ko-fi.com/img/donate_sm.png)](https://ko-fi.com/G2G6GWVV)
### Installation
- From pypi:
`pip3 install rocketchat_API`
- From GitHub:
Clone our repository and `python3 setup.py install`

### Requirements
- [requests](https://github.com/kennethreitz/requests)==2.20.1

### Usage
```
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

proxy_dict = {
              "http"  : "http://127.0.0.1:3128",
              "https" : "https://127.0.0.1:3128",
            }

rocket = RocketChat('user', 'pass', server_url='https://demo.rocket.chat', proxies=proxy_dict)
pprint(rocket.me().json())
pprint(rocket.channels_list().json())
pprint(rocket.chat_post_message('good news everyone!', channel='GENERAL', alias='Farnsworth').json())
pprint(rocket.channels_history('GENERAL', count=5).json())
```

*note*: every method returns a [requests](https://github.com/kennethreitz/requests) Response object.

### Method parameters
Only required parameters are explicit on the RocketChat class but you can still use all other parameters. For a detailed parameters list check the [Rocket chat API](https://rocket.chat/docs/developer-guides/rest-api/)

### API coverage
Most of the API methods are already implemented. If you are interested in a specific call just open an issue or open a pull request.

*note*: Library updated to work with Rocket.Chat >= 0.73.1

### Tests
We are actively testing :) 

Tests run on a Rocket.Chat Docker container so install Docker and docker-compose. To start test server do `docker-compose -f docker-compose-test-server.yml up` and to take test server down `docker-compose -f docker-compose-test-server.yml down`

### Contributing
You can contribute by doing Pull Requests. (It may take a while to merge your code but if it's good it will be merged). Please, try to implement tests for all your code and use a PEP8 compliant code style.

Reporting bugs and asking for features is also contributing ;) Feel free to help us grow by registering issues.

We hang out [here](https://demo.rocket.chat/channel/python_rocketchat_api) if you want to talk. 

### Sponsors
[![aleph-logo](https://s3.amazonaws.com/aleph-engineering/Logo_AE_complete_normal%404x.png)](https://aleph.engineering/)
