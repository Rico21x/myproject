let inventory = {
    Tomato: 50,
    Potato: 50,
    Broccoli: 50
};


function displayInventory() {
    const inventoryTable = document.querySelector('#inventoryTable tbody');
    inventoryTable.innerHTML = '';

    Object.keys(inventory).forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item}</td>
            <td>${inventory[item]}</td>
            <td><img src="images/${item.toLowerCase()}.jpg" alt="${item}" width="50" height="50"></td>
        `;
        inventoryTable.appendChild(row);
    });
    
    updateLiveCount();
}


function updateLiveCount() {
    const itemType = document.querySelector('#itemType').value;
    document.querySelector('#liveCount').textContent = `Available: ${inventory[itemType]}`;
}


document.querySelector('#orderForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const quantity = parseInt(document.querySelector('#quantity').value);
    const itemType = document.querySelector('#itemType').value;

    if (isNaN(quantity) || quantity <= 0) {
        alert('Please enter a valid quantity.');
        return;
    }

    if (inventory[itemType] >= quantity) {
        inventory[itemType] -= quantity;
        alert('Thank you for the order!');
        displayInventory();
    } else {
        alert('Not enough stock available.');
    }
});


document.querySelector('#itemType').addEventListener('change', updateLiveCount);


displayInventory();
