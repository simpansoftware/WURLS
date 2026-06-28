# WURLS - W URL Shortener
## Demo
Demo is hosted [right here](https://wurls.4lvaret.tech/).
## What is it?
It's an URL shortener, with some pretty nifty features. (please dont use this commercially, at the least migrate to a real db before doing that)
## Features
- It shortens urls
- Generates qr codes for urls
- No JS needed!
- URL validation!
## Usage
### To shorten a link
Go to the main page and then choose your options and it should be shortened
### To see the statistics for a page
Go to stats in the bottom right corner, enter your link or shortened id and you will see statistics. <br>
Those statistics include the shortened link, the regular one, a qr code and the view count for that website.
### Endpoints
- `GET /qr?url=<shortid>`
    For seeing the qr code of a shortened page (GET)
- `GET /l?url=<shortid>`
    For redirecting to a page.
- `GET /g?url=<url>`
    For seeing the short id of a page.
- `POST /shorten` 
    Creates a shortened url. Requires form data:
    - `url=<yoururl>` (required)
    - `custom=<YOURCODE>` (optional)

## Credits
- Me, for making the frontend and backend
- W3Schools for a Flask tutorial that I followed and that i kind of understand now
