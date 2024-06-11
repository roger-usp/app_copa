function resetMapContainer(mapContainerID) {
    // Clears the div passed
    // Creates 3 div's inside: map, hover-info and colorbar-div
    let mapDiv = document.createElement("div");
    mapDiv.id = "map";
    mapDiv.style = "height: 70%;";

    let hoverInfo = document.createElement("div");
    hoverInfo.id = "hover-info";
    hoverInfo.style = "height: 5%; display: flex;";

    let pointArrowLegend = document.createElement("div");
    pointArrowLegend.id = "point-arrow-legend";
    pointArrowLegend.style = "height: 5%; display: flex;";

    let colorbarDiv = document.createElement("div");
    colorbarDiv.id = "colorbar-div";
    colorbarDiv.style = "height: 20%;";


    let mapContainer = document.getElementById(mapContainerID);
    mapContainer.innerHTML = "";  // clear previous map
    mapContainer.appendChild(mapDiv);
    mapContainer.appendChild(hoverInfo);
    mapContainer.appendChild(pointArrowLegend);
    mapContainer.appendChild(colorbarDiv);
}



function initMap(mapDivID, centerCoords, zoomLevel) {
    let map = L.map(mapDivID).setView(centerCoords, zoomLevel);
    L.tileLayer(
        'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }
    ).addTo(map);
    return map;
}



function stylePolygonFeature(feature) {
    return {
        fillColor: feature.properties.color,
        weight: 2,
        opacity: 1,
        color: "#444444",
        dashArray: '3',
        fillOpacity: 0.7
    };
}



function stylePointLine(feature) {
    return {color: feature.properties.color};
}



function showInfo(e) {
    let layer = e.target;
    layer.setStyle({dashArray: '0', color: "black", weight: 3})

    let properties = layer.feature.properties;
    let value = properties.value;
    let valueTitle = properties.valueTitle;
    let valueUnit = properties.valueUnit;
    let otherInfo = properties.other; // this is a string in HTML format

    let infoHTML = `<p>${valueTitle}:${value} ${valueUnit}</p>` + otherInfo

    let infoDivID = "hover-info"; // declared in resetMapContainer
    let infoDiv = document.getElementById(infoDivID);
    infoDiv.innerHTML = infoHTML;
    
}



function hideInfo(e){
    let layer = e.target;
    layer.setStyle({dashArray: '3', color: "#444444", weight: 2})
    let infoDivID = "hover-info"; // declared in resetMapContainer
    let infoDiv = document.getElementById(infoDivID);
    infoDiv.innerHTML = "<p></p>";
}



function onEachFeature(feature, layer) {
    layer.on({
        mouseover: showInfo,
        mouseout: hideInfo,
    });
}


function getUniqueColorLegendArray(geojson) {
// the features of the geojson must have "color" and "legend" as properties
    uniqueColorLegendArray = [];
    var unique = true;

    for (let i=0; i<geojson.features.length;i++) {
        let feature = geojson.features[i];
        unique = true;

        for (let j=0; j<uniqueColorLegendArray.length;j++) {
            let colorLegendObj = uniqueColorLegendArray[j];

            let equalColors = colorLegendObj["color"] === feature.properties.color;
            let equalLegends = colorLegendObj["legend"] === feature.properties.legend;
            
            if (equalColors && equalLegends) {
                unique = false;
                break;
            }
        }

        if (unique === true) {
            uniqueColorLegendArray.push({
                "color": feature.properties.color, 
                "legend": feature.properties.legend
            });
        }
    }

    return uniqueColorLegendArray;

}


function fillLegend(characterStr, pointArrowLegend, charLegendArray) {
    for (let i=0;i<charLegendArray.length;i++) {
        let entryContainer = document.createElement("div");
        entryContainer.style = "display: flex;"

        let character = document.createElement("p");
        character.innerHTML = characterStr;
        character.style.color = charLegendArray[i].color;

        let legend = document.createElement("p");
        legend.innerHTML = charLegendArray[i].legend;

        entryContainer.appendChild(character);
        entryContainer.appendChild(legend);

        pointArrowLegend.appendChild(entryContainer);
    }
}


function fillPointArrowLegend(lineGeojson, pointGeojson) {
    let pointArrowLegend = document.getElementById("point-arrow-legend");  // declared in resetMapContainer
    let arrowLegendArray =  getUniqueColorLegendArray(lineGeojson);  // considering there are just arrows, no Lines
    let pointArray = getUniqueColorLegendArray(pointGeojson);

    let arrowCharacter = "&uarr;";
    let pointCharacter = "&#9679;"
    fillLegend(arrowCharacter, pointArrowLegend, arrowLegendArray);
    fillLegend(pointCharacter, pointArrowLegend, pointArray);
}

// Falta fazer os pontos não apareceram como marker
function updateMap(
    mapContainerID,
    colorbarTitle, 
    cmap, 
    polygonGeojson, 
    lineGeojson, 
    pointGeojson, 
    centerCoords, 
    zoomLevel
) {
    resetMapContainer(mapContainerID);

    let map = initMap("map", centerCoords, zoomLevel);
    L.geoJson(polygonGeojson, {style: stylePolygonFeature, onEachFeature: onEachFeature}).addTo(map);
    L.geoJson(lineGeojson, {style: stylePointLine}).addTo(map);
    L.geoJson(pointGeojson, {style: stylePointLine}).addTo(map);

    fillPointArrowLegend(lineGeojson, pointGeojson);
    makeColorbar("colorbar-div", colorbarTitle, 11, cmap);
}

