window.addEventListener("DOMContentLoaded", function () {
    const lightToggle = document.getElementById("lightToggle");
    lightToggle.addEventListener("click", toggleLight);

    const waterToggle = document.getElementById("waterToggle");
    waterToggle.addEventListener("click", water);
}); 

function toggleLight(event) {
    console.log("You clicked the light button!");
    fetch("/api/v1/functions/light", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
    }).then(response => {
        console.log(response);
})};

function water(event) {
    console.log("You clicked the water button!");
    fetch("/api/v1/functions/water", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
    }).then(response => {
        console.log(response);
})}