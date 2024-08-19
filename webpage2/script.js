document.getElementById('fileInput1').addEventListener('change', handleFileUpload);
document.getElementById('fileInput2').addEventListener('change', handleFileUpload);
document.getElementById('colorFilter').addEventListener('change', filterGraph);

let cy;
let allElements = [];
let categories = { key: new Set(), value: new Set() };
let categoryColors = {};
let jsonFiles = [];
let nodesFromFile1 = new Set();
let nodesFromFile2 = new Set();

function handleFileUpload(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    const fileIndex = event.target.id === 'fileInput1' ? 1 : 2;
    reader.onload = function(e) {
        const content = e.target.result;
        const jsonData = JSON.parse(content);
        jsonFiles.push({ index: fileIndex, data: jsonData.complete_tuples });

        if (jsonFiles.length === 2) {
            processGraphData();
            assignColors();
            updateFilters();
            updateCategoryCounts();
            renderGraph(allElements);
        }
    };
    reader.readAsText(file);
}

function processGraphData() {
    const nodes = new Map();
    const edges = [];
    categories = { key: new Set(), value: new Set() };

    jsonFiles.forEach(file => {
        const fileIndex = file.index;
        const tuples = file.data;

        tuples.forEach(tuple => {
            const [key, relation, value, keyType, valueType] = tuple;

            categories.key.add(keyType);
            categories.value.add(valueType);

            if (!nodes.has(key)) {
                nodes.set(key, { data: { id: key, label: key, type: keyType, file: fileIndex } });
                if (fileIndex === 1) nodesFromFile1.add(key);
                if (fileIndex === 2) nodesFromFile2.add(key);
            } else {
                if (fileIndex === 1 && nodesFromFile2.has(key)) nodes.get(key).data.file = 3;
                if (fileIndex === 2 && nodesFromFile1.has(key)) nodes.get(key).data.file = 3;
            }

            if (!nodes.has(value)) {
                nodes.set(value, { data: { id: value, label: value, type: valueType, file: fileIndex } });
                if (fileIndex === 1) nodesFromFile1.add(value);
                if (fileIndex === 2) nodesFromFile2.add(value);
            } else {
                if (fileIndex === 1 && nodesFromFile2.has(value)) nodes.get(value).data.file = 3;
                if (fileIndex === 2 && nodesFromFile1.has(value)) nodes.get(value).data.file = 3;
            }

            edges.push({ data: { source: key, target: value, label: relation, directed: true } });
        });
    });

    allElements = [
        ...Array.from(nodes.values()),
        ...edges
    ];

    console.log("Nodes:", Array.from(nodes.values()));
    console.log("Edges:", edges);
    console.log("All Elements:", allElements);
}

function assignColors() {
    const allCategories = [...categories.key, ...categories.value];
    const colorScale = chroma.scale('Set3').colors(allCategories.length);

    allCategories.forEach((category, index) => {
        categoryColors[category] = colorScale[index];
    });

    allElements.forEach(element => {
        if (element.data.type) {
            element.data.color = categoryColors[element.data.type];
        }

        if (element.data.file === 1) {
            element.data.borderColor = 'red';
        } else if (element.data.file === 2) {
            element.data.borderColor = 'green';
        } else if (element.data.file === 3) {
            element.data.borderColor = 'blue';  // Common nodes have blue border
        }
    });

    console.log("Category Colors:", categoryColors);
    console.log("Elements after color assignment:", allElements);
}

function updateFilters() {
    const keyTypeContainer = document.getElementById('keyTypeCheckboxes');
    const valueTypeContainer = document.getElementById('valueTypeCheckboxes');

    keyTypeContainer.innerHTML = '';
    valueTypeContainer.innerHTML = '';

    categories.key.forEach(category => {
        keyTypeContainer.innerHTML += `
            <div class="form-check">
                <input class="form-check-input" type="checkbox" value="${category}" id="keyType_${category}">
                <label class="form-check-label" for="keyType_${category}" style="color: ${categoryColors[category]};">
                    <span class="color-swatch" style="background-color: ${categoryColors[category]};"></span>${category}
                </label>
            </div>`;
    });

    categories.value.forEach(category => {
        valueTypeContainer.innerHTML += `
            <div class="form-check">
                <input class="form-check-input" type="checkbox" value="${category}" id="valueType_${category}">
                <label class="form-check-label" for="valueType_${category}" style="color: ${categoryColors[category]};">
                    <span class="color-swatch" style="background-color: ${categoryColors[category]};"></span>${category}
                </label>
            </div>`;
    });

    document.querySelectorAll('#keyTypeCheckboxes .form-check-input').forEach(checkbox => {
        checkbox.addEventListener('change', filterGraph);
    });
    document.querySelectorAll('#valueTypeCheckboxes .form-check-input').forEach(checkbox => {
        checkbox.addEventListener('change', filterGraph);
    });
}

function updateCategoryCounts() {
    document.getElementById('keyCategories').innerText = `Key Categories: ${Array.from(categories.key).join(', ')}`;
    document.getElementById('valueCategories').innerText = `Value Categories: ${Array.from(categories.value).join(', ')}`;
}

function renderGraph(elements) {
    if (cy) {
        cy.destroy();
    }

    cy = cytoscape({
        container: document.getElementById('cy'),
        elements: elements,
        style: [
            {
                selector: 'node',
                style: {
                    'label': 'data(label)',
                    'background-color': 'data(color)',
                    'border-color': 'data(borderColor)',
                    'border-width': 3,
                    'text-valign': 'center',
                    'color': '#000'
                }
            },
            {
                selector: 'edge',
                style: {
                    'label': 'data(label)',
                    'width': 2,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier',
                    'arrow-scale': 1.5
                }
            }
        ],
        layout: {
            name: 'cose',
            idealEdgeLength: 100,
            nodeRepulsion: 4000,
            gravity: 0.2,
            numIter: 1000,
            coolingFactor: 0.95,
            fit: true
        }
    });

    console.log("Graph rendered with elements:", elements);
}
function filterGraph() {
    const keyTypes = Array.from(document.querySelectorAll('#keyTypeCheckboxes .form-check-input:checked')).map(cb => cb.value);
    const valueTypes = Array.from(document.querySelectorAll('#valueTypeCheckboxes .form-check-input:checked')).map(cb => cb.value);
    const colorFilter = document.getElementById('colorFilter').value;

    let filteredElements = allElements;

    if (keyTypes.length || valueTypes.length || colorFilter) {
        const filteredNodes = new Set();
        filteredElements = allElements.filter(element => {
            if (element.data.source && element.data.target) {
                const sourceNode = allElements.find(el => el.data.id === element.data.source);
                const targetNode = allElements.find(el => el.data.id === element.data.target);

                const keyTypeMatch = !keyTypes.length || keyTypes.includes(sourceNode.data.type);
                const valueTypeMatch = !valueTypes.length || valueTypes.includes(targetNode.data.type);

                const colorFilterMatch = !colorFilter || sourceNode.data.borderColor === colorFilter || targetNode.data.borderColor === colorFilter;

                if (keyTypeMatch && valueTypeMatch && colorFilterMatch) {
                    filteredNodes.add(sourceNode.data.id);
                    filteredNodes.add(targetNode.data.id);
                    return true;
                }
                return false;
            }
            const colorFilterMatch = !colorFilter || element.data.borderColor === colorFilter;
            return colorFilterMatch;
        });

        filteredElements = filteredElements.filter(element => {
            if (element.data.source && element.data.target) {
                return filteredNodes.has(element.data.source) && filteredNodes.has(element.data.target);
            }
            return filteredNodes.has(element.data.id);
        });
    }

    renderGraph(filteredElements);
}
