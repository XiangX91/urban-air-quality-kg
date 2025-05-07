fetch('AQgraph.json')
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById('network');
    const options = {
      nodes: { shape: 'dot', size: 12 },
      edges: { arrows: 'to' },
      physics: { stabilization: true },
      interaction: { hover: true, tooltipDelay: 200 }
    };

    const network = new vis.Network(container, data, options);
  })
  .catch(error => console.error('Error loading JSON:', error));

