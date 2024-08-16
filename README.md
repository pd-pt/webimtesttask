## Installation

`python3 -m venv venv`
`source venv/bin/activate`
`pip3 install -r requirements.txt`
`cp .env.prod .env`
`python3 gen_secret.py`

## Running

`python3 tornado_app.py`

Open http://localhost:8888

## Note

Due to absense of free domain name and VPS server provided, there is no docker and nginx configs so it's only local version which can be run as described above.