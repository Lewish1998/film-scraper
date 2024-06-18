from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')

with open("todays_films.txt", "w") as f, open("future_films.txt", "w") as f:
    f.write("")

cineworld_urls = [
    "https://www.cineworld.co.uk/cinemas/glasgow-renfrew-street/057#/",
    "https://www.cineworld.co.uk/cinemas/glasgow-silverburn/088#/",
    "https://www.cineworld.co.uk/cinemas/glasgow-parkhead/005#/",
]

all_movies = []


for url in cineworld_urls:

    if url == "https://www.cineworld.co.uk/cinemas/glasgow-renfrew-street/057#/":
        with open("todays_films.txt", "a") as x, open("future_films.txt", "a") as y:
            x.write("~" * 40 + "\n")
            location = "Cineworld - Renfrew Street"
            x.write(f"{location}\n")
            x.write("-" * 40 + "\n")

            y.write("~" * 40 + "\n")
            location = "Cineworld - Renfrew Street"
            y.write(f"{location}\n")
            y.write("-" * 40 + "\n")
    if url == "https://www.cineworld.co.uk/cinemas/glasgow-silverburn/088#/":
        with open("todays_films.txt", "a") as x, open("future_films.txt", "a") as y:
            x.write("~" * 40 + "\n")
            location = "Cineworld - Silverburn"
            x.write(f"{location}\n")
            x.write("-" * 40 + "\n")

            y.write("~" * 40 + "\n")
            location = "Cineworld - Silverburn"
            y.write(f"{location}\n")
            y.write("-" * 40 + "\n")
    if url == "https://www.cineworld.co.uk/cinemas/glasgow-parkhead/005#/":
        with open("todays_films.txt", "a") as x, open("future_films.txt", "a") as y:
            x.write("~" * 40 + "\n")
            location = "Cineworld - Parkhead"
            x.write(f"{location}\n")
            x.write("-" * 40 + "\n")

            y.write("~" * 40 + "\n")
            location = "Cineworld - Parkhead"
            y.write(f"{location}\n")
            y.write("-" * 40 + "\n")

    driver = webdriver.Chrome(options=options)
    print(f"Getting films from {location}. Please wait...\n")
    driver.get(url)

    # Waiting for page to load
    time.sleep(6)

    # Reject cookies
    reject_cookies = driver.find_element(by=By.ID, value="onetrust-accept-btn-handler")
    if reject_cookies:
        print("Cookies found. Rejecting.\n")
        reject_cookies.click()
    else:
        print("Could not find cookies.\n")

    time.sleep(3)

    # Find movies
    movies = driver.find_elements(By.CLASS_NAME, "movie-row")

    # Loop through movies and write showtimes to file
    for movie in movies:
        title_element = movie.find_element(By.CLASS_NAME, "qb-movie-name")
        title = title_element.text.strip()
        showtimes_elements = movie.find_elements(By.CLASS_NAME, "btn-primary")
        showtimes = [time.text.strip() for time in showtimes_elements]

        todays_showtimes = []
        future_showtimes = []

        for showtime in showtimes:
            if any(
                day in showtime
                for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            ):
                future_showtimes.append(showtime)
            else:
                todays_showtimes.append(showtime)

        if todays_showtimes:
            with open("todays_films.txt", "a") as today_file:
                today_file.write(f"Location: {location}\n")
                today_file.write(f"Title: {title}\n")
                today_file.write(f"Showtimes: {', '.join(todays_showtimes)}\n")
                today_file.write("-" * 40 + "\n")

        if future_showtimes:
            with open("future_films.txt", "a") as future_file:
                future_file.write(f"Location: {location}\n")
                future_file.write(f"Title: {title}\n")
                future_file.write(f"Showtimes: {', '.join(future_showtimes)}\n")
                future_file.write("-" * 40 + "\n")

    print("Showtimes written to file\n")
    print("Closing web driver\n")
    time.sleep(2)
    # Close the WebDriver
    driver.quit()


time.sleep(3)
print("Creating json file of todays films")

import json

movies_data = []

with open("todays_films.txt", "r") as today_file:
    location = None
    title = None
    showtimes = []
    for line in today_file:
        line = line.strip()  # Remove leading/trailing whitespace
        if line.startswith("Cineworld"):
            if title:
                movies_data.append(
                    {"location": location, "title": title, "showtimes": showtimes}
                )
                title = None  # Reset title for the next movie
                showtimes = []  # Reset showtimes for the next movie
            location = line  # Update location
        elif line.startswith("Title:"):
            if title:
                movies_data.append(
                    {"location": location, "title": title, "showtimes": showtimes}
                )
                showtimes = []  # Reset showtimes for the next movie
            title = line.split(": ", 1)[1].strip()
        elif line.startswith("Showtimes:"):
            showtimes.extend(line.split(": ", 1)[1].strip().split(", "))

    # Append the last movie read from the file
    if title:
        movies_data.append(
            {"location": location, "title": title, "showtimes": showtimes}
        )

# Write movies_data to JSON file
with open("movies_schedule.json", "w") as json_file:
    json.dump(movies_data, json_file, indent=2)

print("Json created")
