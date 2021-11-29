window.addEventListener("DOMContentLoaded", function () {
  loadLuxData();
  loadTempData();
  loadHumidityData();
});

function loadLuxData() {
  const dataIndexURL = "/api/v1/data/";
  fetch(dataIndexURL)
    .then(validateJSON)
    .then(data => {
      const allData = [];
      for (const dataset of data.data) {
        const date = new Date(dataset.timestamp);
        const lux = Number(dataset.lux);
        const json = {x: date, y: lux};
        allData.push(json);
      }
      return allData;
    })
    .then(createLuxGraph)
    .catch(error => {
      console.log("Data Fetch Failed: ", error)
    })
}

function createLuxGraph(allData) {
  // Used for debugging
  console.log(allData);

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

function loadTempData() {
  const dataIndexURL = "/api/v1/data/";
  fetch(dataIndexURL)
    .then(validateJSON)
    .then(data => {
      const allData = [];
      for (const dataset of data.data) {
        const date = new Date(dataset.timestamp);
        const temp = Number(dataset.temperature);
        const json = {x: date, y: temp};
        allData.push(json);
      }
      return allData;
    })
    .then(createTemperatureGraph)
    .catch(error => {
      console.log("Data Fetch Failed: ", error)
    })
}

function createTemperatureGraph(allData) {
  // Used for debugging
  console.log(allData);

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

function loadHumidityData() {
  const dataIndexURL = "/api/v1/data/";
  fetch(dataIndexURL)
    .then(validateJSON)
    .then(data => {
      const allData = [];
      for (const dataset of data.data) {
        const date = new Date(dataset.timestamp);
        const humidity = Number(dataset.humidity);
        const json = {x: date, y: humidity};
        allData.push(json);
      }
      return allData;
    })
    .then(createHumidityGraph)
    .catch(error => {
      console.log("Data Fetch Failed: ", error)
    })
}

function createHumidityGraph(allData) {
  // Used for debugging
  console.log(allData);

  const config = {
    type: 'line',
    data: {
      labels: [],
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