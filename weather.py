import os
from dotenv import load_dotenv
import requests
import pycountry
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO


load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
#example: os.getenv("564386539048502374568")

city = input("Enter the city name: ")

url = "https://api.weatherapi.com/v1/current.json"

window = tk.Tk()
window.title("Weather Overlay")
window.geometry("300x120")

location_label = tk.Label(
    window,
    text="Loading...",
    font=("Georgian", 12)
)

temp_label = tk.Label(
    window,
    text="--°C",
    font=("Georgian", 15, "bold")
)

icon_label = tk.Label(window)

content_frame = tk.Frame(window)
content_frame.place(relx=0.5, rely=0.5, anchor="center")

location_label.grid(row=0, column=0, pady=0, sticky="w")
icon_label.grid(row=0, column=1, padx=0)
temp_label.place(x=0, y=45)

window.configure(bg="#1E1E1E")
window.attributes("-topmost", False)
window.attributes("-alpha", 0.85)
window.overrideredirect(False)

content_frame.configure(bg="#1E1E1E")

location_label.configure(
    fg="white",
    bg="#1E1E1E",
    font=("Georgian", 12)
)

icon_label.configure(bg="#1E1E1E")

temp_label.configure(
    fg="white",
    bg="#1E1E1E",
    font=("Georgian", 15, "bold")
)


def update_weather():
    global icon_photo

    try:
        params = {
            "key": api_key,
            "q": city
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        country = data["location"]["country"]
        country_info = pycountry.countries.get(name=country)

        if country_info:
            country_code = country_info.alpha_2
        else:
            country_code = country

        name = data["location"]["name"]
        location = f"{name}, {country_code}"

        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        icon = data["current"]["condition"]["icon"]
        icon_url = f"https:{icon}"

        icon_response = requests.get(icon_url, timeout=10)
        icon_response.raise_for_status()

        icon_image = Image.open(
            BytesIO(icon_response.content)
        )

        icon_photo = ImageTk.PhotoImage(
            icon_image,
            master=window
        )

        location_label.configure(text=location)
        temp_label.configure(text=f"{temp_c}°C")
        icon_label.configure(image=icon_photo)
        icon_label.image = icon_photo

        print("Weather updated successfully!")
        print(location)
        print(temp_c)
        print(condition)

    except requests.exceptions.RequestException as error:
        print("Could not update weather:", error)

    except Exception as error:
        print("Error:", error)

    window.after(300000, update_weather)



update_weather()

window.mainloop()