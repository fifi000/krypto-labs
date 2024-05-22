import React, { useState } from 'react';

function Contacts() {
    const contacts = [
        { id: 1, name: 'Chorąży Torpeda', avatar: 'https://samequizy.pl/wp-content/uploads/2021/01/images_27eabf0fa170.jpeg' },
        { id: 2, name: 'Greg lepkie rączki', avatar: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5NeYs8QFuyG2SyoLbJAecqiMFbDOTfaboOnKu2-gNMg&s' },
    ]

    const [amounts, setAmounts] = useState({});
    
    // Update amount for a specific contact
    const updateAmount = (id, value) => {
        setAmounts(prev => ({ ...prev, [id]: value }));
    };

    const createTransaction = async (sender, recipient, amount) => {
        const transaction = { sender, recipient, amount };
        const response = await fetch('http://localhost:5000/transactions/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(transaction),
        });
        const data = await response.json();
        alert(data.message);
    };

    return (
        <div className="card mb-3">
            <div className="card-body">
                <h5 className="card-title">Contacts</h5>
                {contacts.map(contact => (
                    <div key={contact.id} className="d-flex justify-content-between align-items-center">
                        <div>
                            <img src={contact.avatar} alt={contact.name} height="64" className='me-3'/>
                            <label className="form-label">{contact.name}</label>
                        </div>
                        <div>
                            <input type="number"
                                value={amounts[contact.id] || ''}
                                onChange={(e) => updateAmount(contact.id, e.target.value)}
                            />
                            <button
                                onClick={() => createTransaction(contact.id, amounts[contact.id])}
                                className="btn btn-success mx-3"
                            >
                                Send
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Contacts;
