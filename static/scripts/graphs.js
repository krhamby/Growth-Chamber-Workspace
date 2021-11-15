window.addEventListener("DOMContentLoaded", function() {
    loadData();
});

function loadData() {
    const dataIndexURL = "localhost:5000/api/v1/data/";
    fetch(dataIndexURL)
        .then(validateJSON)
        .then(createGraphs)
        .catch(error => {
            console.log("Data Fetch Failed: ", error)
    })
}

function createGraphs(data) {
    // Date object
    const d = new Date();

    // Options for DateTimeFormat
    const options = {
      month: "numeric", day: "numeric",
      hour:"numeric", minute: "numeric", second: "numeric"
    };

    /* While this works for now, I may want a helper method or 
    different implementation */
    const labels = [
        new Intl.DateTimeFormat("en-US", options).format(d - 10800000 * 8),
        new Intl.DateTimeFormat("en-US", options).format(d - 10800000 * 7),
        new Intl.DateTimeFormat("en-US", options).format(d - 10800000 * 6),
        new Intl.DateTimeFormat("en-US", options).format(d - 10800000 * 5),
        new Intl.DateTimeFormat("en-US", options).format(d - 10800000 * 4),
        new Intl.DateTimeFormat("en-US", options).format(d - 10800000 * 3),
        new Intl.DateTimeFormat("en-US", options).format(d - 10800000 * 2),
        new Intl.DateTimeFormat("en-US", options).format(d - 10800000),
        new Intl.DateTimeFormat("en-US", options).format(d),
      ];
      
    const data = {
      labels: labels,
      datasets: [{
        label: 'Lux',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: [1000, 1050, 1060, 1100, 900],
      }]
    };
    const config = {
      type: 'line',
      data: data,
      options: {
          scales: {
              x: {
                  type: "timeseries"
              }
          }
      }
    };
    const luxChart = new Chart(
      document.getElementById('luxChart'),
      config
      );
}

// function convertTime(date) {
//     return "${date.}"
// }

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