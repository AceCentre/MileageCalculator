# Mileage Calculator

## What does this do?

It provides a box for the user to paste lines like:

		OL8 3QL to BR48lW to SW11DR to OL83QL
		OL83QL to  L171DW to OL83QL

and hitting the 'Go' button it will return the mileage between these points.

## How?

By the power of Greyskull!

(No, really: Google Maps API, and the [MapIt API](https://mapit.mysociety.org/docs/#api-by_postcode))

## Why?

To help me fill in my expense claim forms. I was bored having to copy and paste loads of postcodes into google maps so I instead wasted twice as much time making an app to do it for me. 

## Note

We round up to the nearest whole mile. Hope thats ok with you 


## Deploy

* You will need a [Google Maps API Key](https://developers.google.com/maps/documentation/javascript/get-api-key) environmental variable (named 'GAPI_KEY')
* You will also need a [MapIt API Key](https://mapit.mysociety.org/pricing/) environment variable (named as 'MAPIT_KEY')
* You should set a port environmental variable ('PORT" = 33507)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

