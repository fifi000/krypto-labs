import React from 'react';
import ProfileBlock from './ProfileBlock';
import Contacts from './Contacts';
import BlockchainView from './BlockchainView';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <div className="container mt-3">
      <ProfileBlock />
      <Contacts />
      <BlockchainView />
    </div>
  );
}

export default App;
