

function loadTable(){

    const TableTxt = document.querySelector("#list tbody")
    TableTxt.style.display = "block";

     if (TableTxt !== ""){
                TableTxt.innerHTML = "";
    }

     var myarr = document.getElementById("choices-text-preset-values").value.split(",");
          if(myarr.length>10){
              alert("Proszę wybrać do 10 produktów");
          }else {
              var mydiv = document.getElementById("list");
              mydiv.style.display = "block";
              const params = {params: document.getElementById("choices-text-preset-values").value};
              fetch('http://127.0.0.1:5000/ceneo', {
                  method: 'POST', headers: {
                      "Content-Type":
                          'application/json'
                  }, body: JSON.stringify(params),
              }).then((response) => response.json().then((mydict) => {
                      console.log(mydict);
                      for (const [key, value] of Object.entries(mydict)) {
                          console.log(value);

                          let product = `<tr class="prod">
                        <td>${value}</td>
                        <td>tbd</td>
                        <td>tbd</td>
                        </tr>`

                      TableTxt.insertAdjacentHTML("beforeend", product);
                      }
                  }
              )).catch((error) => {
                  console.log(error)
              });
          }



}