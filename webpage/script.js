document.getElementById('fileInput').addEventListener('change', handleFileUpload);
document.getElementById('keyType').addEventListener('change', filterGraph);
document.getElementById('valueType').addEventListener('change', filterGraph);

let cy;
let allElements = [];
let categories = { key: new Set(), value: new Set() };
let categoryColors = {};

function handleFileUpload(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        const jsonData = JSON.parse(content);
        processGraphData(jsonData.complete_tuples);
        assignColors();
        updateFilters();
        updateCategoryCounts();
        renderGraph(allElements);
    };
    reader.readAsText(file);
}

function processGraphData(tuples) {
    const nodes = new Map();
    const edges = [];
    categories = { key: new Set(), value: new Set() };

    tuples.forEach(tuple => {
        const [key, relation, value, keyType, valueType] = tuple;

        categories.key.add(keyType);
        categories.value.add(valueType);

        if (!nodes.has(key)) {
            nodes.set(key, { data: { id: key, label: key, type: keyType } });
        }
        if (!nodes.has(value)) {
            nodes.set(value, { data: { id: value, label: value, type: valueType } });
        }

        edges.push({ data: { source: key, target: value, label: relation, directed: true } });
    });

    allElements = [
        ...Array.from(nodes.values()),
        ...edges
    ];
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
    });
}

function updateFilters() {
    const keyTypeSelect = document.getElementById('keyType');
    const valueTypeSelect = document.getElementById('valueType');

    keyTypeSelect.innerHTML = '<option value="">All</option>';
    valueTypeSelect.innerHTML = '<option value="">All</option>';

    categories.key.forEach(category => {
        keyTypeSelect.innerHTML += `<option value="${category}" style="color: ${categoryColors[category]};" class="color-option">
            <span class="color-swatch" style="background-color: ${categoryColors[category]};"></span>${category}
        </option>`;
    });

    categories.value.forEach(category => {
        valueTypeSelect.innerHTML += `<option value="${category}" style="color: ${categoryColors[category]};" class="color-option">
            <span class="color-swatch" style="background-color: ${categoryColors[category]};"></span>${category}
        </option>`;
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
            name: 'cose'
        }
    });
}

function filterGraph() {
    const keyType = document.getElementById('keyType').value;
    const valueType = document.getElementById('valueType').value;

    let filteredElements = allElements;

    if (keyType || valueType) {
        const filteredNodes = new Set();
        filteredElements = allElements.filter(element => {
            if (element.data.source && element.data.target) {
                const sourceNode = allElements.find(el => el.data.id === element.data.source);
                const targetNode = allElements.find(el => el.data.id === element.data.target);

                const keyTypeMatch = !keyType || sourceNode.data.type === keyType;
                const valueTypeMatch = !valueType || targetNode.data.type === valueType;

                if (keyTypeMatch && valueTypeMatch) {
                    filteredNodes.add(sourceNode.data.id);
                    filteredNodes.add(targetNode.data.id);
                    return true;
                }
                return false;
            }
            return true;
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
