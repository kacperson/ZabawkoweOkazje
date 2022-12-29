

function loadTable(){
    const TableTxt = document.querySelector("#list tbody")
    TableTxt.style.display = "block";

     if (TableTxt !== ""){
                TableTxt.innerHTML = ""
    }
    fetch('http://127.0.0.1:5000/ceneo')
        .then(response => response.json())
        .then(data => {

            let product = `<tr class="prod">
                        <td></td>
                        <td></td>
                        <td></td>
                        </tr>`
        })

}