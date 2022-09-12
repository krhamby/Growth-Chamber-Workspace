window.addEventListener("DOMContentLoaded", function () {
    const lightToggle = document.getElementById("lightToggle");
    lightToggle.addEventListener("click", toggleLight);
    console.log("test");
}); 

function toggleLight(event) {
    console.log("You clicked the light button!");
    fetch("/api/v1/functions/light", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
    }).then(response => {
        console.log(response);
})};