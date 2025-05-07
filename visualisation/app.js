fetch('AQgraph.json')
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById('network');

    const options = {
      nodes: { shape: 'dot', size: 12 },
      edges: { arrows: 'to', font: { align: 'middle' } },
      physics: { stabilization: true },
      interaction: { hover: true, tooltipDelay: 200 }
    };

    const network = new vis.Network(container, data, options);

    const infoBox = document.createElement('div');
    infoBox.style.position = 'absolute';
    infoBox.style.backgroundColor = '#f0f0f0';
    infoBox.style.border = '1px solid #ddd';
    infoBox.style.padding = '10px';
    infoBox.style.borderRadius = '5px';
    infoBox.style.display = 'none';
    document.body.appendChild(infoBox);

    network.on('click', function(properties) {
      const ids = properties.nodes;
      const edgeIds = properties.edges;

      if (ids.length > 0) {
        const clickedNode = data.nodes.find(node => node.id === ids[0]);
        infoBox.innerHTML = `<strong>Node Information</strong><pre>${JSON.stringify(clickedNode, null, 2)}</pre>`;
        infoBox.style.left = properties.event.srcEvent.pageX + 'px';
        infoBox.style.top = properties.event.srcEvent.pageY + 'px';
        infoBox.style.display = 'block';
      } else if (edgeIds.length > 0) {
        const clickedEdge = data.edges.find(edge => edge.id === edgeIds[0]);
        infoBox.innerHTML = `<strong>Edge Information</strong><pre>${JSON.stringify(clickedEdge, null, 2)}</pre>`;
        infoBox.style.left = properties.event.srcEvent.pageX + 'px';
        infoBox.style.top = properties.event.srcEvent.pageY + 'px';
        infoBox.style.display = 'block';
      } else {
        infoBox.style.display = 'none';
      }
    });

    network.on('dragStart', function() {
      infoBox.style.display = 'none';
    });

  })
  .catch(error => console.error('Error loading JSON:', error));
