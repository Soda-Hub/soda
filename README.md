# Soda

[![Build Status](https://travis-ci.org/Soda-Hub/soda.svg?branch=master)](https://travis-ci.org/Soda-Hub/soda)

Soda: Let's build an open social network based on [ActivityPub][1].

I will be documenting my journey in building up an ActivityPub social network that will be able to participate in the [Fediverse][2] networks on [my blog][3], and the code will be stored in this repository.

The main reference will be the "[Guide for new ActivityPub implementers][4]", which is the most up to date official reference I am able to find. We will be testing our implementation by attempting to federate with one of the [Mastodon][5] instances, as the official test suite does not look like it will [not be coming back up any time soon][6].

## Plan
- [x] Setup web framework ([Starlette][7])
- [ ] Webfinger support for discovering identities ([Reference][8])
- [ ] Follow user support
- [ ] Publish test/image support

.. and more to come.


## License

Copyright 2020 Victor Neo

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

```
http://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


[1]: https://activitypub.rocks/
[2]: https://fediverse.party/
[3]: https://cheshire.io
[4]: https://socialhub.activitypub.rocks/t/guide-for-new-activitypub-implementers/479
[5]: https://github.com/tootsuite/mastodon
[6]: https://socialhub.activitypub.rocks/t/the-activitypub-test-suite/290
[7]: https://www.starlette.io/
[8]: https://blog.joinmastodon.org/2018/06/how-to-implement-a-basic-activitypub-server/
