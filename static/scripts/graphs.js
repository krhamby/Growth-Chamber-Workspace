let isCacheSupported = 'caches' in window;

window.addEventListener("DOMContentLoaded", function () {
  createGraphs();
  cacheData();

  const luxFilter = document.getElementById("luxFilter");
  luxFilter.addEventListener("click", toggleLuxFilter);
});

async function cacheData() {
  if (isCacheSupported) {
    caches.open("data").then(cache => {
      cache.add("/api/v1/data/").then(cache => {
        console.log("Cached data");
      });   
    });
  }
}

async function createGraphs() {
  const dataIndexURL = "/api/v1/data/";
  fetch(dataIndexURL)
    .then(validateJSON)
    .then(data => {
      extractLuxData(data);
      extractTempData(data);
      extractHumidityData(data);
    })
    .catch(error => {
      console.log("Data Fetch and Graph Creation Failed: ", error)
    });
}

function extractLuxData(data) {
  const allData = [];
  for (const dataset of data.data) {
    const date = new Date(dataset.timestamp);
    const lux = Number(dataset.lux);
    const json = {x: date, y: lux};
    allData.push(json);
  }
  createLuxGraph(allData);
}

function extractTempData(data) {
  const allData = [];
  for (const dataset of data.data) {
    const date = new Date(dataset.timestamp);
    const temp = Number(dataset.temperature);
    const json = {x: date, y: temp};
    allData.push(json);
  }
  createTemperatureGraph(allData);
}

function extractHumidityData(data) {
  const allData = [];
  for (const dataset of data.data) {
    const date = new Date(dataset.timestamp);
    const humidity = Number(dataset.humidity);
    const json = {x: date, y: humidity};
    allData.push(json);
  }
  createHumidityGraph(allData);
}

function toggleLuxFilter(event) {
  const oldChart = document.getElementById("luxChart");
  oldChart.parentNode.removeChild(oldChart);
  const newChart = document.createElement("canvas"); 
  newChart.id = "luxChart";
  document.getElementById("lux").appendChild(newChart);

  caches.open("data").then(cache => {
    cache.match("/api/v1/data/").then(response => {
      response.json().then(data => {
        const filteredData = [];
        for (const dataset of data.data) {
          const date = new Date(dataset.timestamp);
          const lux = Number(dataset.lux);
          const filter = new Date() - 1000 * 60 * 10; // NOTE: temporary filter for 10 minutes
          if ((date - 0) >= filter) {
            const json = {x: date, y: lux};
            filteredData.push(json);
          }
        }
        createLuxGraph(filteredData);
      });
    });
  });
}


async function createLuxGraph(allData) {
  const config = {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        data: allData,
        label: "Lux",
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)'
      }],
    },
    options: {
      scales: {
        x: {
          type: "time",
          time: {
            displayFormats: {
              quarter: "MMM",
              month: "MMM",
              day: "MMM do",
              hour: "MMM do h:mm aaaaa",
              minute: "m",
              second: "s"
            }
          }
        },
      }
    }
  }
  // console.log(label);
  // const canvasId = String(label.toLowerCase()) + "Chart";
  const luxChart = new Chart(
  document.getElementById("luxChart"),
  config
  );
}

function createTemperatureGraph(allData) {
  const config = {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        data: allData,
        label: "Temperature (F)",
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)'
      }],
    },
    options: {
      scales: {
        x: {
          type: "time",
          time: {
            displayFormats: {
              quarter: "MMM",
              month: "MMM",
              day: "MMM do",
              hour: "MMM do h:mm aaaaa",
              minute: "m",
              second: "s"
            }
          }
        },
      }
    }
  }
  const temperatureChart = new Chart(
    document.getElementById("temperatureChart"),
    config
  );
}

function createHumidityGraph(allData) {
  const config = {
    type: 'line',
    data: {
      datasets: [{
        data: allData,
        label: "Humidity (%)",
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)'
      }],
    },
    options: {
      scales: {
        x: {
          type: "time",
          time: {
            displayFormats: {
              quarter: "MMM",
              month: "MMM",
              day: "MMM do",
              hour: "MMM do h:mm aaaaa",
              minute: "m",
              second: "s"
            }
          }
        },
      }
    }
  }
  const humidityChart = new Chart(
    document.getElementById("humidityChart"),
    config
  );
}

/**
 * Validate a response to ensure the HTTP status code indcates success.
 * 
 * @param {Response} response HTTP response to be checked
 * @returns {object} object encoded by JSON in the response
 */
function validateJSON(response) {
  if (response.ok) {
    return response.json();
  } else {
    return Promise.reject(response);
  }
}