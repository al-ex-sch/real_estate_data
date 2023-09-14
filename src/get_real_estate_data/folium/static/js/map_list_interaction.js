function highlightMarker(index) {
    // Get the marker element and change its background color
    var markerElement = document.getElementById("marker_" + index);
    markerElement.style.backgroundColor = "yellow";

    // Get the property item element and change its background color
    var propertyElement = document.getElementById("property_" + index);
    propertyElement.style.backgroundColor = "#f0f0f0";
}

function unhighlightMarker(index) {
    // Get the marker element and reset its background color
    var markerElement = document.getElementById("marker_" + index);
    markerElement.style.backgroundColor = "";

    // Get the property item element and reset its background color
    var propertyElement = document.getElementById("property_" + index);
    propertyElement.style.backgroundColor = "";
}
