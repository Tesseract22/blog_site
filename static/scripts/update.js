

function add() {
    const row = document.createElement('div');
    row.setAttribute('class', 'form-group row');

    const name_col = document.createElement('div');
    name_col.setAttribute('class', 'col-xs-2')
    const amount_col = document.createElement('div')
    amount_col.setAttribute('class', 'col-xs-2')
    row.appendChild(name_col)
    row.appendChild(amount_col)

    const name = document.createElement('input')
    name.setAttribute('class', 'form-control')
    name.setAttribute('list', 'factorio_items')
    name.setAttribute('placeholder', 'Search for Item')
    name_col.appendChild(name)

    const amount = document.createElement('input')
    amount.setAttribute('class', 'form-control')
    amount.setAttribute('placeholder', 'Enter Amount...')
    amount_col.appendChild(amount)

    f = document.getElementById("items-form")
    f.appendChild(row)
    console.log("aa")
}