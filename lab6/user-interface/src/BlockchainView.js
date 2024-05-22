import React, { useState } from 'react';

function BlockchainView() {
    const [blockchain, setBlockchain] = useState('');

    const viewChain = async () => {
        const response = await fetch('http://localhost:5000/chain');
        const data = await response.json();
        setBlockchain(JSON.stringify(data, null, 2)); // Beautify the JSON response
    };

    return (
        <div className="card mb-3">
            <div className="card-body">
                <h5 className="card-title">Blockchain</h5>
                <button onClick={viewChain} className="btn btn-secondary">View Full Chain</button>
                <pre>{blockchain}</pre>
            </div>
        </div>
    );
}

export default BlockchainView;
