function getOptGroups(info) {
    let optGroups = [];
    info.forEach(element => optGroups.push(element["optgroupLabel"]));
    let uniqueOptGroups = [...new Set(optGroups)];
    return uniqueOptGroups;
}


function fillMultiSelectbox(selectID, info) {
    let selectbox = document.getElementById(selectID);
    for (let i=0; i<info.length;i++) {
        let infoEntry = info[i];
        let opt = document.createElement("option");
        opt.value = infoEntry["optionValue"];
        opt.innerHTML = infoEntry["optionInnerHTML"];
        selectbox.appendChild(opt);
    }
}



function fillSelectbox(selectID, info) {
    let selectbox = document.getElementById(selectID);
    let uniqueOptGroups = getOptGroups(info);
    
    for (let i=0; i<uniqueOptGroups.length; i++) {
        let optgroupLabel = uniqueOptGroups[i];

        let optGroup = document.createElement("optgroup");
        optGroup.label = optgroupLabel;

        for (let j=0; j<info.length;j++) {
            let infoEntry = info[j];
            if (infoEntry["optgroupLabel"] === optgroupLabel) {
                let opt = document.createElement("option");
                opt.value = infoEntry["optionValue"];
                opt.innerHTML = infoEntry["optionInnerHTML"];
                optGroup.appendChild(opt);
            }
        }
        selectbox.appendChild(optGroup);
    }
}



async function fillBaseSelect(scriptRoot) {
    let fetchURL = `${scriptRoot}/base-select-info`;
    let response = await fetch(fetchURL);
    let info = await response.json();
    fillSelectbox("base-select", info);
}

async function fillPointSelect(scriptRoot, pointKeeper) {
    let fetchURL = `${scriptRoot}/point-select-info`;
    let response = await fetch(fetchURL);
    let info = await response.json();
    fillMultiSelectbox("point-select", info);
    new MultiSelectTag('point-select', {
        onChange: values => pointKeeper.updateValues(values)
    });
}

async function fillArrowSelect(scriptRoot, arrowKeeper) {
    let fetchURL = `${scriptRoot}/arrow-select-info`;
    let response = await fetch(fetchURL);
    let info = await response.json();
    fillMultiSelectbox("arrow-select", info);
    new MultiSelectTag('arrow-select', {
        onChange: values => arrowKeeper.updateValues(values)
    });
}


class ValueKeeper {
    constructor() {
        this.values = []
    }

    updateValues(newValues) {
        this.values = [];
        newValues.forEach(element => this.values.push(element.value))
    }
}