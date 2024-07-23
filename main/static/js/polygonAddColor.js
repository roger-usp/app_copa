function getPolygonGeojsonMax(geojson) {
    let valuesArray = [];
    geojson.features.forEach(feature => valuesArray.push(feature.properties.value));
    return Math.max(...valuesArray);   
}


function getGeojsonCmap(geojson, colorArray, colorFormat) {
    let minVal = 0;
    let maxVal = getPolygonGeojsonMax(geojson);
    let cmap = new ColorMap(minVal, maxVal, colorArray, colorFormat);
    return cmap;
}


function fillGeojsonColor(geojson, cmap) {
    let newGeojson = {"type": "FeatureCollection", "features": []};
    geojson.features.forEach(
        function(feature) {
            let newFeature = Object.assign({}, feature);
            let color = cmap.getHEX(feature.properties.value);
            newFeature.properties["color"] = color;
            newGeojson.features.push(newFeature)
        }
    );
    newGeojson["metadata"] = geojson["metadata"]
    return newGeojson;
}
