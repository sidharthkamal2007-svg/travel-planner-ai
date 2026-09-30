import streamlit as st
import requests
import math

# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="TRAVEL PLANNER AI",
    page_icon="✈️",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM STYLE
# ---------------------------------------------------------

st.markdown("""
<style>
.main {
    background: #f7f9fc;
}

.title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 0;
}

.tagline {
    text-align: center;
    font-size: 24px;
    font-weight: 600;
    margin-top: 0;
}

.subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}

.food {
    padding: 15px;
    border-radius: 12px;
    background: #fff8e8;
    margin-bottom: 10px;
}

.place {
    padding: 15px;
    border-radius: 12px;
    background: #eef7ff;
    margin-bottom: 10px;
}

.day {
    padding: 18px;
    border-radius: 15px;
    background: white;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FOOD DATABASE
# ---------------------------------------------------------

FOOD_DATA = {
    "chennai": [
        "Masala Dosa",
        "Idli & Sambar",
        "Chennai Filter Coffee",
        "Kothu Parotta",
        "Biryani",
        "Pongal"
    ],
    "delhi": [
        "Chole Bhature",
        "Butter Chicken",
        "Paratha",
        "Chaat",
        "Kebabs",
        "Rajma Chawal"
    ],
    "mumbai": [
        "Vada Pav",
        "Pav Bhaji",
        "Misal Pav",
        "Bombay Sandwich",
        "Bhel Puri",
        "Pani Puri"
    ],
    "hyderabad": [
        "Hyderabadi Biryani",
        "Haleem",
        "Double Ka Meetha",
        "Mirchi Ka Salan",
        "Osmania Biscuit"
    ],
    "bangalore": [
        "Masala Dosa",
        "Idli Vada",
        "Bisi Bele Bath",
        "Ragi Mudde",
        "Filter Coffee"
    ],
    "bengaluru": [
        "Masala Dosa",
        "Idli Vada",
        "Bisi Bele Bath",
        "Ragi Mudde",
        "Filter Coffee"
    ],
    "kolkata": [
        "Kolkata Biryani",
        "Rosogolla",
        "Kathi Roll",
        "Mishti Doi",
        "Fish Curry"
    ],
    "jaipur": [
        "Dal Baati Churma",
        "Pyaaz Kachori",
        "Ghewar",
        "Laal Maas",
        "Gatte Ki Sabzi"
    ],
    "goa": [
        "Goan Fish Curry",
        "Prawn Balchao",
        "Vindaloo",
        "Bebinca",
        "Pork Sorpotel"
    ],
    "agra": [
        "Petha",
        "Mughlai Cuisine",
        "Bedai",
        "Dalmoth"
    ],
    "varanasi": [
        "Kachori Sabzi",
        "Banarasi Chaat",
        "Lassi",
        "Tamatar Chaat",
        "Banarasi Paan"
    ],
    "kochi": [
        "Kerala Sadya",
        "Appam & Stew",
        "Kerala Parotta",
        "Fish Curry",
        "Puttu & Kadala"
    ],
    "madurai": [
        "Madurai Jigarthanda",
        "Parotta",
        "Kari Dosa",
        "Idli",
        "Madurai Biryani"
    ],
    "paris": [
        "Croissant",
        "Macaron",
        "Crêpes",
        "French Onion Soup",
        "Coq au Vin"
    ],
    "tokyo": [
        "Sushi",
        "Ramen",
        "Tempura",
        "Takoyaki",
        "Okonomiyaki"
    ],
    "rome": [
        "Pasta Carbonara",
        "Roman Pizza",
        "Cacio e Pepe",
        "Gelato",
        "Supplì"
    ],
    "new york": [
        "New York Pizza",
        "Bagel",
        "Cheesecake",
        "Hot Dog",
        "Pastrami Sandwich"
    ]
}

# ---------------------------------------------------------
# FALLBACK TOURIST PLACES
# ---------------------------------------------------------

FALLBACK_PLACES = {
    "chennai": [
        ("Marina Beach", 13.0500, 80.2824),
        ("Kapaleeshwarar Temple", 13.0339, 80.2707),
        ("Fort St. George", 13.0795, 80.2870),
        ("Government Museum Chennai", 13.0694, 80.2609),
        ("San Thome Basilica", 13.0335, 80.2785),
        ("Valluvar Kottam", 13.0524, 80.2417),
        ("Guindy National Park", 13.0068, 80.2206),
        ("Elliot's Beach", 12.9982, 80.2707)
    ],

    "delhi": [
        ("India Gate", 28.6129, 77.2295),
        ("Red Fort", 28.6562, 77.2410),
        ("Qutub Minar", 28.5244, 77.1855),
        ("Lotus Temple", 28.5535, 77.2588),
        ("Humayun's Tomb", 28.5933, 77.2507),
        ("Akshardham Temple", 28.6127, 77.2773)
    ],

    "mumbai": [
        ("Gateway of India", 18.9220, 72.8347),
        ("Marine Drive", 18.9431, 72.8235),
        ("Chhatrapati Shivaji Terminus", 18.9402, 72.8356),
        ("Juhu Beach", 19.0988, 72.8265),
        ("Siddhivinayak Temple", 19.0178, 72.8303)
    ],

    "hyderabad": [
        ("Charminar", 17.3616, 78.4747),
        ("Golconda Fort", 17.3833, 78.4011),
        ("Hussain Sagar Lake", 17.4239, 78.4738),
        ("Salar Jung Museum", 17.3713, 78.4804),
        ("Chowmahalla Palace", 17.3578, 78.4717)
    ],

    "bangalore": [
        ("Bangalore Palace", 12.9987, 77.5920),
        ("Lalbagh Botanical Garden", 12.9507, 77.5848),
        ("Cubbon Park", 12.9763, 77.5929),
        ("Vidhana Soudha", 12.9796, 77.5906),
        ("ISKCON Temple", 13.0108, 77.5511)
    ],

    "bengaluru": [
        ("Bangalore Palace", 12.9987, 77.5920),
        ("Lalbagh Botanical Garden", 12.9507, 77.5848),
        ("Cubbon Park", 12.9763, 77.5929),
        ("Vidhana Soudha", 12.9796, 77.5906),
        ("ISKCON Temple", 13.0108, 77.5511)
    ],

    "jaipur": [
        ("Amber Fort", 26.9855, 75.8513),
        ("Hawa Mahal", 26.9239, 75.8267),
        ("City Palace", 26.9258, 75.8237),
        ("Jantar Mantar", 26.9247, 75.8246),
        ("Jal Mahal", 26.9535, 75.8460)
    ],

    "goa": [
        ("Baga Beach", 15.5557, 73.7517),
        ("Fort Aguada", 15.4920, 73.7737),
        ("Basilica of Bom Jesus", 15.5009, 73.9117),
        ("Calangute Beach", 15.5449, 73.7553),
        ("Chapora Fort", 15.6136, 73.7395)
    ],

    "agra": [
        ("Taj Mahal", 27.1751, 78.0421),
        ("Agra Fort", 27.1795, 78.0211),
        ("Mehtab Bagh", 27.1799, 78.0421),
        ("Itmad-ud-Daulah's Tomb", 27.1929, 78.0309)
    ],

    "varanasi": [
        ("Kashi Vishwanath Temple", 25.3109, 83.0107),
        ("Dashashwamedh Ghat", 25.3069, 83.0107),
        ("Assi Ghat", 25.2891, 83.0050),
        ("Sarnath", 25.3810, 83.0227)
    ],

    "kochi": [
        ("Fort Kochi", 9.9658, 76.2421),
        ("Chinese Fishing Nets", 9.9675, 76.2429),
        ("Mattancherry Palace", 9.9615, 76.2590),
        ("Jew Town", 9.9580, 76.2590),
        ("Marine Drive Kochi", 9.9740, 76.2740)
    ],

    "madurai": [
        ("Meenakshi Amman Temple", 9.9195, 78.1193),
        ("Thirumalai Nayakkar Palace", 9.9167, 78.1195),
        ("Gandhi Memorial Museum", 9.9340, 78.1378),
        ("Vandiyur Mariamman Teppakulam", 9.9067, 78.1400)
    ],

    "paris": [
        ("Eiffel Tower", 48.8584, 2.2945),
        ("Louvre Museum", 48.8606, 2.3376),
        ("Arc de Triomphe", 48.8738, 2.2950),
        ("Notre-Dame", 48.8530, 2.3499)
    ],

    "tokyo": [
        ("Shibuya Crossing", 35.6595, 139.7005),
        ("Senso-ji Temple", 35.7148, 139.7967),
        ("Tokyo Skytree", 35.7101, 139.8107),
        ("Tokyo Tower", 35.6586, 139.7454)
    ],

    "rome": [
        ("Colosseum", 41.8902, 12.4922),
        ("Trevi Fountain", 41.9009, 12.4833),
        ("Vatican Museums", 41.9065, 12.4536),
        ("Pantheon", 41.8986, 12.4769)
    ],

    "new york": [
        ("Statue of Liberty", 40.6892, -74.0445),
        ("Central Park", 40.7829, -73.9654),
        ("Times Square", 40.7580, -73.9855),
        ("Empire State Building", 40.7484, -73.9857)
    ]
}

# ---------------------------------------------------------
# DESTINATION SEARCH
# ---------------------------------------------------------

def find_destination(city):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "TravelPlannerAI/1.0"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        data = response.json()

        if data:
            return {
                "name": data[0]["display_name"],
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"])
            }

    except Exception:
        pass

    return None


# ---------------------------------------------------------
# TOURIST PLACES FROM OPENSTREETMAP
# ---------------------------------------------------------

def get_osm_places(lat, lon):

    query = f"""
    [out:json][timeout:15];

    (
      node(around:30000,{lat},{lon})["tourism"="attraction"];
      node(around:30000,{lat},{lon})["tourism"="museum"];
      node(around:30000,{lat},{lon})["tourism"="viewpoint"];
      node(around:30000,{lat},{lon})["tourism"="zoo"];
      node(around:30000,{lat},{lon})["tourism"="theme_park"];
      node(around:30000,{lat},{lon})["historic"="monument"];
      node(around:30000,{lat},{lon})["historic"="castle"];
      node(around:30000,{lat},{lon})["leisure"="park"];
      node(around:30000,{lat},{lon})["natural"="beach"];
    );

    out center;
    """

    servers = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter"
    ]

    for server in servers:

        try:

            response = requests.post(
                server,
                data=query,
                timeout=25
            )

            data = response.json()

            places = []

            for item in data.get("elements", []):

                tags = item.get("tags", {})
                name = tags.get("name")

                if not name:
                    continue

                item_lat = item.get("lat")
                item_lon = item.get("lon")

                if item_lat is None:
                    center = item.get("center", {})
                    item_lat = center.get("lat")
                    item_lon = center.get("lon")

                if item_lat is None:
                    continue

                places.append(
                    (name, float(item_lat), float(item_lon))
                )

            # Remove duplicates
            unique = []
            names = set()

            for place in places:
                if place[0] not in names:
                    unique.append(place)
                    names.add(place[0])

            if unique:
                return unique[:15]

        except Exception:
            continue

    return []


# ---------------------------------------------------------
# WEATHER
# ---------------------------------------------------------

def get_weather(lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        return response.json().get("current")

    except Exception:
        return None


def weather_text(code):

    weather = {
        0: "Clear Sky ☀️",
        1: "Mainly Clear 🌤️",
        2: "Partly Cloudy ⛅",
        3: "Cloudy ☁️",
        45: "Fog 🌫️",
        48: "Fog 🌫️",
        51: "Light Drizzle 🌦️",
        61: "Rain 🌧️",
        63: "Rain 🌧️",
        65: "Heavy Rain 🌧️",
        71: "Snow ❄️",
        80: "Rain Showers 🌦️",
        81: "Rain Showers 🌦️",
        82: "Heavy Showers 🌧️",
        95: "Thunderstorm ⛈️"
    }

    return weather.get(code, "Weather data available")


# ---------------------------------------------------------
# FOOD
# ---------------------------------------------------------

def get_food(city):

    key = city.lower().strip()

    return FOOD_DATA.get(
        key,
        [
            "Local traditional dishes",
            "Popular street food",
            "Regional speciality",
            "Traditional dessert",
            "Local beverage"
        ]
    )


# ---------------------------------------------------------
# BUDGET
# ---------------------------------------------------------

def calculate_budget(days, travellers):

    food = 500 * days * travellers
    local_travel = 400 * days * travellers
    stay = 1000 * days * travellers

    total = food + local_travel + stay

    return food, local_travel, stay, total


# ---------------------------------------------------------
# ITINERARY
# ---------------------------------------------------------

def make_itinerary(days, places, foods):

    itinerary = []

    if not places:
        places = [("Explore the city", 0, 0)]

    for day in range(days):

        first = places[(day * 2) % len(places)]
        second = places[(day * 2 + 1) % len(places)]

        food = foods[day % len(foods)]

        itinerary.append({
            "day": day + 1,
            "place1": first[0],
            "place2": second[0],
            "food": food
        })

    return itinerary


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="title">✈️ TRAVEL PLANNER AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="tagline">Varata Mame Durr</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Plan your trip with destinations, places, food, weather, map and budget.</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# INPUT AREA
# ---------------------------------------------------------

st.sidebar.header("🌍 Trip Details")

destination = st.sidebar.text_input(
    "📍 Destination",
    placeholder="Example: Chennai"
)

days = st.sidebar.number_input(
    "📅 Number of Days",
    min_value=1,
    max_value=30,
    value=3
)

travellers = st.sidebar.number_input(
    "👥 Travellers",
    min_value=1,
    max_value=50,
    value=2
)

trip_type = st.sidebar.selectbox(
    "🧑‍🤝‍🧑 Trip Type",
    ["Friends", "Family", "Couple", "Solo"]
)

interest = st.sidebar.selectbox(
    "❤️ Main Interest",
    ["Everything", "Nature", "History", "Food", "Adventure", "Relaxing"]
)

budget = st.sidebar.number_input(
    "💰 Your Budget (₹)",
    min_value=1000,
    max_value=1000000,
    value=15000,
    step=1000
)

plan_button = st.sidebar.button(
    "🚀 Create My Travel Plan",
    use_container_width=True
)

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if not plan_button:

    st.info(
        "👈 Enter your destination, number of days and travellers, "
        "then click **Create My Travel Plan**."
    )

    st.markdown("""
    ### ✨ What this project can do

    📍 Find destination location  
    🏛️ Show tourist places  
    🍴 Show famous local food  
    🌤️ Show current weather  
    🗺️ Display destination map  
    💰 Calculate estimated budget  
    📅 Create day-wise itinerary  
    🤖 Provide travel assistant responses  
    """)

else:

    if not destination.strip():

        st.error("Please enter a destination.")

    else:

        with st.spinner("🌍 Finding your destination..."):

            location = find_destination(destination)

        if location is None:

            st.warning(
                "Online location search failed. "
                "I will try using the destination name."
            )

            key = destination.lower().strip()

            if key in FALLBACK_PLACES:

                first_place = FALLBACK_PLACES[key][0]

                location = {
                    "name": destination.title(),
                    "lat": first_place[1],
                    "lon": first_place[2]
                }

            else:

                st.error(
                    "Sorry da 😕 Destination could not be found. "
                    "Try a city name like Chennai, Paris or Tokyo."
                )

                st.stop()

        # -------------------------------------------------
        # DESTINATION
        # -------------------------------------------------

        st.success(f"📍 Destination found: **{location['name']}**")

        # -------------------------------------------------
        # WEATHER
        # -------------------------------------------------

        weather = get_weather(
            location["lat"],
            location["lon"]
        )

        st.subheader("🌤️ Current Weather")

        if weather:

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Temperature",
                f"{weather['temperature_2m']} °C"
            )

            c2.metric(
                "Feels Like",
                f"{weather['apparent_temperature']} °C"
            )

            c3.metric(
                "Humidity",
                f"{weather['relative_humidity_2m']}%"
            )

            c4.metric(
                "Wind",
                f"{weather['wind_speed_10m']} km/h"
            )

            st.info(
                weather_text(weather["weather_code"])
            )

        # -------------------------------------------------
        # TOURIST PLACES
        # -------------------------------------------------

        st.subheader("🏛️ Places To Visit")

        with st.spinner("🔎 Finding tourist places..."):

            places = get_osm_places(
                location["lat"],
                location["lon"]
            )

        if not places:

            places = FALLBACK_PLACES.get(
                destination.lower().strip(),
                []
            )

        if interest == "Nature":

            nature_words = [
                "beach", "park", "garden", "lake",
                "waterfall", "zoo", "viewpoint"
            ]

            filtered = [
                p for p in places
                if any(word in p[0].lower() for word in nature_words)
            ]

            if filtered:
                places = filtered

        elif interest == "History":

            history_words = [
                "fort", "museum", "temple", "palace",
                "monument", "church", "castle", "historic"
            ]

            filtered = [
                p for p in places
                if any(word in p[0].lower() for word in history_words)
            ]

            if filtered:
                places = filtered

        places = places[:12]

        if places:

            for i, place in enumerate(places, 1):

                st.markdown(
                    f"""
                    <div class="place">
                    <b>{i}. {place[0]}</b><br>
                    📍 Latitude: {place[1]:.4f} |
                    Longitude: {place[2]:.4f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.warning(
                "No tourist places were found for this destination."
            )

        # -------------------------------------------------
        # MAP
        # -------------------------------------------------

        st.subheader("🗺️ Destination Map")

        map_data = [
            {
                "lat": location["lat"],
                "lon": location["lon"]
            }
        ]

        for place in places:

            map_data.append({
                "lat": place[1],
                "lon": place[2]
            })

        st.map(map_data)

        # -------------------------------------------------
        # FOOD
        # -------------------------------------------------

        st.subheader("🍴 Famous Local Food")

        foods = get_food(destination)

        food_columns = st.columns(2)

        for i, food in enumerate(foods):

            with food_columns[i % 2]:

                st.markdown(
                    f"""
                    <div class="food">
                    🍴 <b>{food}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # -------------------------------------------------
        # BUDGET
        # -------------------------------------------------

        st.subheader("💰 Estimated Trip Budget")

        food_cost, travel_cost, stay_cost, total = calculate_budget(
            days,
            travellers
        )

        b1, b2, b3, b4 = st.columns(4)

        b1.metric("🍴 Food", f"₹{food_cost:,}")
        b2.metric("🚕 Local Travel", f"₹{travel_cost:,}")
        b3.metric("🏨 Stay", f"₹{stay_cost:,}")
        b4.metric("💰 Estimated Total", f"₹{total:,}")

        if budget >= total:

            st.success(
                f"✅ Your budget of ₹{budget:,} is enough "
                f"for the estimated trip cost."
            )

        else:

            st.warning(
                f"⚠️ Estimated cost is ₹{total:,}. "
                f"Your budget is ₹{budget:,}."
            )

        # -------------------------------------------------
        # ITINERARY
        # -------------------------------------------------

        st.subheader("📅 Your Day-Wise Itinerary")

        itinerary = make_itinerary(
            days,
            places,
            foods
        )

        for item in itinerary:

            st.markdown(
                f"""
                <div class="day">

                <h3>📅 Day {item['day']}</h3>

                🌅 Morning:
                <b>{item['place1']}</b>

                <br><br>

                🌇 Evening:
                <b>{item['place2']}</b>

                <br><br>

                🍴 Food to try:
                <b>{item['food']}</b>

                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # TRIP SUMMARY
        # -------------------------------------------------

        st.subheader("📋 Trip Summary")

        st.write(
            f"""
            **Destination:** {destination.title()}

            **Trip Type:** {trip_type}

            **Travellers:** {travellers}

            **Duration:** {days} days

            **Main Interest:** {interest}

            **Budget:** ₹{budget:,}

            **Estimated Cost:** ₹{total:,}
            """
        )

        # -------------------------------------------------
        # TRAVEL ASSISTANT
        # -------------------------------------------------

        st.subheader("🤖 Travel Assistant")

        question = st.text_input(
            "Ask something about your trip...",
            placeholder="Example: What food should I try?"
        )

        if question:

            q = question.lower()

            if "food" in q or "eat" in q:

                st.info(
                    "🍴 You should try: "
                    + ", ".join(foods[:5])
                )

            elif "place" in q or "visit" in q:

                if places:

                    st.info(
                        "🏛️ Places you can visit: "
                        + ", ".join([p[0] for p in places[:6]])
                    )

            elif "budget" in q or "cost" in q:

                st.info(
                    f"💰 Estimated trip cost: ₹{total:,}"
                )

            elif "weather" in q:

                if weather:

                    st.info(
                        f"🌤️ Current temperature is "
                        f"{weather['temperature_2m']} °C. "
                        f"{weather_text(weather['weather_code'])}"
                    )

            elif "day" in q:

                st.info(
                    f"📅 Your trip is planned for {days} days."
                )

            else:

                st.info(
                    "🤖 I can help with places, food, "
                    "budget, weather and itinerary."
                )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "✈️ TRAVEL PLANNER AI • Varata Mame Durr • "
    "Powered by OpenStreetMap, Open-Meteo & Streamlit"
)
