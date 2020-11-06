# astigmia

## Disclaimer

This application is a personal project and has no affiliation with [Vision PT](https://www.visionpt.com.au) what so ever.

Likewise, I don't take any responsibility if your account is disabled as a result of using this.

Having said that, I don't expect anyone else but myself to use it.

I'm just open sourcing it as a point of motivation to keep plugging away at it.

## Overview

A couple of days a week, I see a <abbr title="Personal trainer">PT</abbr> which is always a good time.

Part of that includes food tracking (ie; you should be hitting this many carbs, this much protein etc)

In order to faciliate that, the gym has [a mobile app]() but it's kind of slow and I'm not a huge fan of it.

It works but the amount of friction that comes with inputting data is a pain and I'd rather prepare my week using a desktop where I can have multiple windows open and so on.

Luckily, being a mobile application, it's relatively easy to view the API calls being made.

`astigmia` is a Django application that makes those API calls in the background and caches the responses locally so as to greatly speed up the pain points mentioned.

## What's in the name?

It's a play on words. The name of the gym is Vision, and ironically I'm short sighted. Likewise, the APIs are a bit short sighted with often redundant information included in the payloads, no consistency in timestamp formats and so on.

[Astigmatism](https://en.wiktionary.org/wiki/astigmatism) refers to when your eyesight is blurred as a result of light not being focused correctly on the retina.

## Current functionality

At the moment, it doesn't do a whole lot but it's more of a hacky side project that I work on here and there.

You can log in, which uses a custom `auth_backend` to authenticate against the backend of the mobile app. From a user point of view, you login with your gym credentials and the returned profile is stored as a Django User object, with some extended properties.

It makes things less of a hassle since I don't have to store anything myself and I can treat the application as effectively stateless.

There are some celery tasks but they're not configured to work with Heroku just yet although they should be shortly.

It's just enough that I've got a solid base to start working away at, and adding new features that I want for myself.

My first aim will be adding the food tracking functionality though since that's what I really want to get usable on a desktop.

## Is it safe to use?

Beats me.

At the moment, I don't do any user agent spoofing but I also don't think anyone looks at the logs.

It seems only fair enough to add a custom user agent string identifying this application as much as I could add a spoof user agent string.

I did mention in an email once that I had intended to build such a thing.

## Things to do

* Migrate away from Heroku in favour of Github Actions (auto deploy doesn't seem to work anyway)
* Add PR steps such as running unit tests + linting
* Consider replacing bootstrap since I don't like having jQuery in the mix (tailwind?)
* Document API quirks
* Add some unit tests (should have really been done in the first place heh)
* Extract API calls into their own standalone Python API client
* Wire up celery background tasks with Heroku
* Add developer setup steps
