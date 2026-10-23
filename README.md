# 🌦️ WeatherScope — Interactive Weather Forecast & Analytics Web Application

A modern, responsive, and full-featured **Weather Forecast Website** built using **Python, Streamlit, Pandas, Plotly**, and the **Open-Meteo API**. Designed specifically for BTech students and fresher software engineers to showcase clean coding, API integration, interactive data visualization, and data analytics skills on their resumes.

---

## 📌 Project Overview

**WeatherScope** provides real-time current weather metrics, 24-hour hourly forecasts, and a 7-day daily weather outlook for any city worldwide. Users can search for any global location, toggle between metric and imperial units (Celsius/Fahrenheit, km/h/mph, mm/inches), inspect interactive Plotly charts, and export processed forecast data directly into CSV format.

### ✨ Key Features
- **Global City Geocoding & Search**: Search any city worldwide with automatic coordinate resolution and multi-match selection.
- **Instant Current Weather**: Real-time temperature, "feels like" apparent temperature, humidity %, wind speed & direction, precipitation, UV index, and atmospheric pressure.
- **7-Day Forecast Cards**: Clean daily forecast cards with minimum and maximum temperatures, rain probability %, and WMO weather condition icons.
- **24-Hour Hourly Breakdown**: Continuous hourly temperature curve and condition tracking for the next 24 hours.
- **Interactive Plotly Visualizations**:
  - 🌡️ **Temperature Trend**: High & Low temperature range with smooth shaded area ribbons.
  - 🌧️ **Precipitation Outlook**: Dual-metric visualization for rain probability (%) and rainfall accumulation.
  - 💨 **Wind Speed**: Maximum daily wind speed analysis.
  - ⏱️ **24-Hour Curve**: Spline-interpolated hourly temperature fluctuation.
- **Data Analytics & Pandas Processing**: Calculates statistical metrics such as average weekly temperatures, hottest/coldest day, rainiest day, and total rainfall.
- **CSV Data Export**: Download cleaned forecast data as a CSV file for further analytical workflows.
- **Zero API Key Requirement**: Uses Open-Meteo's open-access non-commercial endpoints—no registration or private API keys required.
- **Responsive & Modern UI**: Built with Streamlit and enhanced with custom CSS cards, shadows, and badges.

---

## 🛠️ Technology Stack

| Layer | Tool / Library | Role & Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core application logic and data pipelines |
| **Web Framework** | Streamlit | Rapid reactive web interface and session state |
| **Data Processing** | Pandas | Cleaning JSON API payloads, datetime parsing, calculating summary statistics |
| **Data Visualization** | Plotly (Graph Objects) | Interactive charts with tooltips, dual-axes, and custom themes |
| **API Integration** | Requests & Open-Meteo API | Geocoding city search and fetching comprehensive meteorological models |

---

## 📁 Project Structure

```text
weather_forecaste/
│
├── app.py              # Main Streamlit web application & UI layout
├── weather_api.py      # Open-Meteo Geocoding & Forecast API integrations
├── utils.py            # WMO weather code mapping & Pandas data transformations
├── requirements.txt    # Project dependencies
└── README.md           # Project guide, deployment steps & viva Q&A
```

---

## 🚀 Getting Started (Run Locally)

### 1. Prerequisites
Ensure you have **Python 3.10 or higher** installed on your system. You can check by running:
```bash
python --version
```

### 2. Clone or Navigate to the Project Folder
Open your terminal or PowerShell and navigate to the project directory:
```bash
cd "C:\Users\dsaid\OneDrive\Documents\weather_forecaste"
```

### 3. (Optional but Recommended) Create a Virtual Environment
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Streamlit will automatically launch your default browser and open the dashboard at `http://localhost:8501`.

---

## 🌐 Deploy to Streamlit Community Cloud (Free Hosting)

Streamlit Community Cloud allows you to deploy and share your web app for free directly from your GitHub repository.

### Step-by-Step Deployment:
1. **Push your code to GitHub** (see instructions below).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and click **Sign In** (connect your GitHub account).
3. Click the **"New app"** button.
4. Fill in the deployment details:
   - **Repository**: `your-github-username/weather-forecast-dashboard`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy!"**.
6. Streamlit Cloud will read `requirements.txt`, install packages, and deploy your live website with a public URL you can include on your resume!

---

## 📦 How to Upload to GitHub

Follow these steps in your project directory:

```bash
# 1. Initialize Git repository
git init

# 2. Add all project files
git add .

# 3. Commit the changes
git commit -m "Initial commit: WeatherScope Dashboard with Streamlit, Pandas, Plotly & Open-Meteo"

# 4. Rename default branch to main
git branch -M main

# 5. Create a new repository on https://github.com/new (e.g. 'weather-forecast-dashboard')
# 6. Link your local repo to GitHub (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/weather-forecast-dashboard.git

# 7. Push the code
git push -u origin main
```

---

## 🎓 Viva & Interview Preparation (Simple English Guide)

When presenting this project in college viva or job interviews, here is how you can explain every component clearly:

### 1. High-Level Architecture
> *"The project follows a modular 3-tier architecture: Presentation Layer (Streamlit & Plotly), Data Transformation Layer (Pandas & utils.py), and API Service Layer (weather_api.py). When a user enters a city name, the app calls the Open-Meteo Geocoding API to resolve latitude and longitude coordinates. Then, it queries the Open-Meteo Forecast endpoint to receive hourly and 7-day weather predictions. The raw nested JSON response is parsed into clean Pandas DataFrames, which feed into interactive Plotly figures and custom Streamlit UI cards."*

### 2. Why Open-Meteo API?
- **No API Keys Needed**: It allows open access for non-commercial and educational use without rate limit barriers.
- **Accurate Geocoding**: Resolves global cities with state, country, and official timezone.
- **Rich Meteorological Parameters**: Provides temperatures, precipitation probabilities, wind speeds, UV index, and WMO standard codes.

### 3. How is Pandas Utilized?
- **Nested JSON to Tabular DataFrame**: Open-Meteo returns parallel arrays (`time`, `temperature_2m_max`, etc.). Pandas converts them into structured tables.
- **Datetime Parsing & Localization**: `pd.to_datetime` parses timestamps into custom formatted day labels (`"Today"`, `"Tomorrow"`, `"Fri, Oct 24"`).
- **Statistical Aggregation**: Uses Pandas `.mean()`, `.idxmax()`, `.idxmin()`, and boolean masks (`(df['precipitation_sum'] > 0.5).sum()`) to compute weekly insights like the hottest day, coolest day, and rainy day frequencies.
- **Data Export**: Generates CSV files using `.to_csv()` for user download.

### 4. Why Plotly over Matplotlib or Seaborn?
- Matplotlib generates static image files (PNG/JPEG) that cannot be zoomed or hovered over on the web.
- Plotly produces interactive WebGL/SVG graphics that let users hover over individual data points, isolate traces, toggle legends, and zoom into specific time ranges seamlessly on desktop and mobile devices.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
