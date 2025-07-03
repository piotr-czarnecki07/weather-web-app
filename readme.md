# IMPORTANT

Redis might not be available due to the free database plan and Redis policy, which removes unused free databases after a period of inactivity.

# Overview

Web scraping application for fetching weather data from an API.  
Uses Redis for saving caches, which reduces network traffic.  
Weather data is searched by entering the city name.  
Saved caches are stored for an hour and then deleted.

If the website is to be hosted, the `ALLOWED_HOSTS` variable should be updated to match the domain.

## Starting the Environment

*Note: If the project is hosted on a domain, there's no need to follow the steps below.*

1. Ensure Python 3.10+ is installed.
2. Create a virtual environment, for example, by running `py -m venv venv` in the Command Prompt.
3. Activate the environment.
4. Install dependencies from `requirements.txt`.
5. Create a `.env` file based on the `.env.example` in the same directory as `.env.example`. (UWAGA: na potrzeby rekrutacji wzór pliku `.env` jest dostępny w [HASLA](./HASLA.md)).
6. Change the Command Prompt's current working directory to the `./weather_api/` directory.
7. Run `manage.py runserver` and open the browser on the provided host.

## Usage

On the main page, there is an input field where you can enter the name of the city for which you want to obtain the weather.  
After entering the city name (in English), you will be shown the current weather for that city.  
Underneath, there's a forecast for the next days.  
By clicking on one of these, you can see the details of the weather for that day.

## Credits

- Idea: [https://roadmap.sh/projects/weather-api-wrapper-service](https://roadmap.sh/projects/weather-api-wrapper-service)  
- API: [https://www.weatherapi.com](https://www.weatherapi.com)  
- Code: [https://github.com/piotr-czarnecki07](https://github.com/piotr-czarnecki07)