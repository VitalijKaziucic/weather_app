import streamlit as st
import plotly.express as px
from weather_api import WeatherApi


class WeatherForecastApp:
    header = "Weather Forecast for the Next Days"
    help = "Select the number of forecasted days"
    columns = 5

    def __init__(self):
        self.weather_data = None
        self.days = None

    def get_data_by_days(self):

        data_index = int(len(self.weather_data["list"]) / 5) * int(self.days)
        data = self.weather_data["list"][:data_index + 1]
        return data[:data_index]

    def fill_temperature_plot(self):
        dates = []
        temperatures = []

        for day_data in self.get_data_by_days():
            full_datetime_string = day_data["dt_txt"]
            dates.append(full_datetime_string)
            temperatures.append(day_data["main"]["temp"])

        figure = px.line(x=dates,
                         y=temperatures,
                         labels={"x": "Date", "y": "Temperature (C)"})
        st.plotly_chart(figure, theme=None, use_container_width=True)

    def fill_sky(self):
        images_dict = {
            "Clear": "images/clear.png",
            "Clouds": "images/cloud.png",
            "Rain": "images/rain.png",
            "Snow": "images/snow.png"
        }

        weather_data = self.get_data_by_days()

        for index in range(0, len(weather_data), self.columns):
            cloud_data = weather_data[index: index + self.columns]

            for i, column in enumerate(st.columns(self.columns)):
                try:
                    cloud_status = cloud_data[i]["weather"][0]["main"]
                except IndexError:
                    break
                else:
                    with column:
                        temperature = round(cloud_data[i]["main"]["temp"])
                        temperature_string = f"+ {temperature}" if temperature > 0 else temperature
                        datetime_string = cloud_data[i]["dt_txt"]
                        caption_string = f"{datetime_string[:-3]}\n Temperature: {temperature_string}"
                        st.image(images_dict[cloud_status], width=115)
                        st.write(caption_string)

    def run_app(self):

        st.title(self.header)
        place = st.text_input(label="Place:", key="place_input")
        self.days = st.slider(label="Forecast Days", key="select", min_value=1, max_value=5, step=1, help=self.help)
        option = st.selectbox(label="Select data to view", options=("", "Temperature", "Sky"))

        if option and place:
            day_string = "day" if self.days == 1 else "days"

            text = f"Temperature for the next {self.days} {day_string} in  {place}"
            st.subheader(text)

            weather = WeatherApi(place)
            self.weather_data = weather.get_api_data()
            if self.weather_data["cod"] != "200":
                st.error(self.weather_data["message"].capitalize())
            else:
                match option:
                    case "Sky":
                        self.fill_sky()
                    case "Temperature":
                        self.fill_temperature_plot()


