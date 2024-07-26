class ColorMap {
  constructor(minVal, maxVal, colorArray, colorFormat) {
    this.minVal = minVal;
    this.maxVal = maxVal;
    this.colorFormat = colorFormat;  // must be "hex" or "rgb"
    this.colorArrayRGB = colorArray.map(color => this.initColor(color));
    this.nColors = this.colorArrayRGB.length;
  }

  componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
  }
  
  RGBToHex(rgb) {
    let r = rgb[0];
    let g = rgb[1];
    let b = rgb[2];
    return "#" + this.componentToHex(r) + this.componentToHex(g) + this.componentToHex(b);
  }

  hexToRGB(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? [
      parseInt(result[1], 16),
      parseInt(result[2], 16),
      parseInt(result[3], 16)
    ] : null;
  }

  initColor(color) {
    if (this.colorFormat === "hex") {
      return this.hexToRGB(color)
    }

    else if (this.colorFormat === "rgb") {
      return color
    }
  }

  getPercentage(val) {
    let percentage = (val-this.minVal)/(this.maxVal-this.minVal);
    if (percentage > 1) {
      return 1
    }
    else if (percentage < 0) {
      return 0
    }

    else {
      return percentage
    }
  }


  interpolate(sectionPercentage, initialRGB, finalRGB) {
    let rgb = [];
    for (let i=0; i<3;i++){
      let ic = initialRGB[i];  // initial component
      let fc = finalRGB[i];  // final component
      let newComponent = sectionPercentage*(fc-ic)+ic;
      rgb.push(
        Math.round(newComponent)
      );
    }
    return rgb
  }

  getSectionPercentages() {
    let sectionPercentages = [];
    for (let i=0;i<(this.nColors);i++) {
      let sectionPerc = i*(1/(this.nColors-1));
      sectionPercentages.push(sectionPerc);
    }
    sectionPercentages.push(1);
    return sectionPercentages
  }

  findInsertPosition(arr, value) {
    let low = 0;
    let high = arr.length - 1;

    while (low <= high) {
        let mid = Math.floor((low + high) / 2);
        if (arr[mid] === value) {
            return [mid, mid];  // Exact match at index mid
        } else if (arr[mid] < value) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    // If not exactly found, low is the index where it would be inserted
    // high is the index just before where it would be inserted
    return [high, low];
  }

  


  getRGBperc(percentage) {
    if (percentage === 0) {
      return this.colorArrayRGB[0]
    }

    else if (percentage === 1) {
      return this.colorArrayRGB[this.nColors-1]
    }
    
    else {
      let sectionPercentages = this.getSectionPercentages();
      let insertPositions = this.findInsertPosition(sectionPercentages, percentage);

      if (insertPositions[0] === insertPositions[1]) {
        return this.colorArrayRGB[insertPositions[0]]
      }

      else {
        let initialIDX = insertPositions[0];
        let finalIDX = insertPositions[1];
        let initialRGB = this.colorArrayRGB[initialIDX];
        let finalRGB = this.colorArrayRGB[finalIDX];

        let initialPerc = sectionPercentages[initialIDX];
        let finalPerc = sectionPercentages[finalIDX];
        let sectionPercentage = (percentage-initialPerc)/(finalPerc-initialPerc);
        return this.interpolate(sectionPercentage, initialRGB, finalRGB)
      }
    }
  }

  getRGB(val) {
    let percentage = this.getPercentage(val);
    return this.getRGBperc(percentage)
  }

  getHEXperc(percentage) {
    let rgb = this.getRGBperc(percentage);
    let hex = this.RGBToHex(rgb);
    return hex
  }
  getHEX(val) {
    let rgb = this.getRGB(val);
    let hex = this.RGBToHex(rgb);
    return hex
  }

}