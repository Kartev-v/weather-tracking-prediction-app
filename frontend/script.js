const API_BASE_URL = window.location.origin === "http://localhost:5000" 
    ? "http://localhost:5000" 
    : "http://localhost:5000";

console.log("🔗 API Base URL:", API_BASE_URL);
console.log("🌐 Page Origin:", window.location.origin);

const cityInput = document.getElementById("cityInput");
const searchBtn = document.getElementById("searchBtn");
const errorMessage = document.getElementById("errorMessage");

const currentWeatherSection = document.getElementById("currentWeatherSection");
const historicalCardsSection = document.getElementById("historicalCardsSection");
const predictionSection = document.getElementById("predictionSection");
const topCitiesSection = document.getElementById("topCitiesSection");

const hottestBtn = document.getElementById("hottestBtn");
const coldestBtn = document.getElementById("coldestBtn");

searchBtn.addEventListener("click", handleSearchWeather);
cityInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        handleSearchWeather();
    }
});

hottestBtn.addEventListener("click", handleGetHottestCities);
coldestBtn.addEventListener("click", handleGetColdestCities);

async function handleSearchWeather() {
    const city = cityInput.value.trim();
    
    if (!city) {
        showError("Please enter a city name");
        return;
    }
    
    clearError();
    hideSearchSections();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/weather?city=${encodeURIComponent(city)}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        console.log("API Response:", data);
        
        if (data.success && data.weather) {
            displayCurrentWeather(data.weather);
            displayHistoricalCards(data.highest_temp, data.lowest_temp);
            displayPrediction(data.prediction);
        } else {
            showError(data.message || "City not found");
            hideSearchSections();
        }
    } catch (error) {
        console.error("Error:", error);
        showError("Error fetching weather. Make sure the backend server is running on port 5000.");
        hideSearchSections();
    }
}

function hideSearchSections() {
    currentWeatherSection.classList.add("hidden");
    historicalCardsSection.classList.add("hidden");
    predictionSection.classList.add("hidden");
}

function displayCurrentWeather(weather) {
    try {
        if (!weather || typeof weather !== 'object') {
            console.error("Invalid weather data:", weather);
            return;
        }
        
        document.getElementById("weatherCity").textContent = 
            `${weather.city || "Unknown"}, ${weather.country || ""}`;
        document.getElementById("temperature").textContent = 
            `${weather.temperature || "--"}°C`;
        document.getElementById("description").textContent = 
            capitalizeWords(weather.description || "--");
        document.getElementById("humidity").textContent = 
            `${weather.humidity || "--"}%`;
        document.getElementById("windSpeed").textContent = 
            `${weather.wind_speed || "--"} m/s`;
        document.getElementById("pressure").textContent = 
            `${weather.pressure || "--"} hPa`;
        
        currentWeatherSection.classList.remove("hidden");
    } catch (error) {
        console.error("Error displaying current weather:", error);
        showError("Error displaying weather data");
    }
}

function displayHistoricalCards(highest, lowest) {
    try {
        if (highest && typeof highest === 'object' && highest.temp !== null) {
            document.getElementById("highestTemp").textContent = `${highest.temp}°C`;
            document.getElementById("highestCity").textContent = highest.station || "Unknown Location";
        } else {
            document.getElementById("highestTemp").textContent = "--°C";
            document.getElementById("highestCity").textContent = "No Database Record";
        }
        
        if (lowest && typeof lowest === 'object' && lowest.temp !== null) {
            document.getElementById("lowestTemp").textContent = `${lowest.temp}°C`;
            document.getElementById("lowestCity").textContent = lowest.station || "Unknown Location";
        } else {
            document.getElementById("lowestTemp").textContent = "--°C";
            document.getElementById("lowestCity").textContent = "No Database Record";
        }
        
        historicalCardsSection.classList.remove("hidden");
    } catch (error) {
        console.error("Error displaying historical cards:", error);
        historicalCardsSection.classList.add("hidden");
    }
}

function displayPrediction(prediction) {
    try {
        if (prediction && typeof prediction === 'object' && prediction.predicted_temp) {
            document.getElementById("predictedTemp").textContent = 
                `${prediction.predicted_temp || "--"}°C`;
            document.getElementById("predictedWind").textContent = 
                `${prediction.predicted_wind_speed || "--"} m/s`;
            document.getElementById("predictionMethod").textContent = 
                prediction.method || "Moving Average";
            
            predictionSection.classList.remove("hidden");
        } else {
            console.warn("No prediction data available");
            predictionSection.classList.add("hidden");
        }
    } catch (error) {
        console.error("Error displaying prediction:", error);
        predictionSection.classList.add("hidden");
    }
}

async function handleGetHottestCities() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/hottest-cities`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        console.log("Hottest Cities Response:", data);
        
        if (data.success && Array.isArray(data.cities)) {
            displayTopCities(data.cities, "🔥 Top 5 Hottest Cities");
        } else {
            showError("Error fetching hottest cities");
        }
    } catch (error) {
        console.error("Error:", error);
        showError("Error fetching hottest cities. Check server connection.");
    }
}

async function handleGetColdestCities() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/coldest-cities`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        console.log("Coldest Cities Response:", data);
        
        if (data.success && Array.isArray(data.cities)) {
            displayTopCities(data.cities, "❄️ Top 5 Coldest Cities");
        } else {
            showError("Error fetching coldest cities");
        }
    } catch (error) {
        console.error("Error:", error);
        showError("Error fetching coldest cities. Check server connection.");
    }
}

function displayTopCities(cities, title) {
    try {
        const topCitiesList = document.getElementById("topCitiesList");
        const topCitiesTitle = document.getElementById("topCitiesTitle");
        
        topCitiesTitle.textContent = title;
        topCitiesList.innerHTML = "";
        
        if (!cities || cities.length === 0) {
            topCitiesList.innerHTML = `<div class="city-row">No records found in database</div>`;
        } else {
            cities.forEach((city, index) => {
                const row = document.createElement("div");
                row.className = "city-row";
                row.innerHTML = `
                    <span class="rank">#${index + 1}</span>
                    <span class="name">${city.name || "Unknown"}</span>
                    <span class="temp">${city.temp || "--"}°C</span>
                `;
                topCitiesList.appendChild(row);
            });
        }
        
        topCitiesSection.classList.remove("hidden");
    } catch (error) {
        console.error("Error displaying top cities:", error);
        showError("Error displaying cities list");
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.add("show");
}

function clearError() {
    errorMessage.textContent = "";
    errorMessage.classList.remove("show");
}

function capitalizeWords(str) {
    if (!str || typeof str !== 'string') return "--";
    return str.replace(/\b\w/g, (char) => char.toUpperCase());
}