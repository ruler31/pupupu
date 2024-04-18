document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.editable');

    cells.forEach(cell => {
        cell.addEventListener('blur', () => {
            const newValue = cell.textContent;
            const tableId = cell.dataset.tableId;
            const rowIndex = cell.dataset.rowIndex;
            const colIndex = cell.dataset.colIndex;
            updateCell(tableId, rowIndex, colIndex, newValue);
        });
    });

    function updateCell(tableId, rowIndex, colIndex, newValue) {
        fetch('/update_cell', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                table_id: tableId,
                row_index: rowIndex,
                col_index: colIndex,
                new_value: newValue
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
        })
        .catch(error => {
            console.error('There was an error!', error);
        });
    }
});
