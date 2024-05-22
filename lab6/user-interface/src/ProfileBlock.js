import React from 'react';

function ProfileBlock() {
  const mineBlock = async () => {
    const response = await fetch('http://localhost:5000/mine');
    const data = await response.json();
    alert(JSON.stringify(data));
  };

  return (
    <div className="card mb-3">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-center">
          <div>
            <img src="https://www.gimpuj.info/gallery/75398_17_11_12_12_01_56_0.png" alt="Tytus Bomba" height="64"/>
            <label className="form-label">Tytus Bomba</label>
          </div>
          <div>
            <label className="form-label">50 Kurwinox Coinów</label>
            <button onClick={mineBlock} className="btn btn-outline-primary mx-5">
              <img src="https://data2.cupsell.pl/upload/generator/84002/640x420/1016109_print-trimmed-1.png" alt="Pickaxe" height="32"/>
            </button>
          </div>
        </div>        
      </div>
    </div>
  );
}

export default ProfileBlock;
