const input = document.getElementById('input');
const documentInput = document.getElementById('carga');

documentInput.addEventListener('change', (e)=> {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.readAsText(file);
    reader.addEventListener('load', (e) => {
      input.innerHTML = reader.result;
    });
  });

let headers = new Headers()
headers.append('Content-Type', 'application/json');
headers.append('Accept', 'application/json');
headers.append('Access-Control-Allow-Origin', 'http://localhost:5000');
headers.append('Access-Control-Allow-Credentials', 'true');
headers.append('GET', 'POST', 'OPTIONS','PUT','DELETE');

//carga masiva de datos
function cargar(){
  let file = document.getElementById("carga").files[0];
  if (file) {
      let reader = new FileReader();
      reader.readAsText(file, "UTF-8");
      reader.onload = function (evt) {
          let cuerpo = {
              data:evt.target.result
          }

          console.log(JSON.stringify(cuerpo))
          fetch('http://localhost:5000/cargar', {
          method: 'POST',
          headers,
          body: JSON.stringify(cuerpo),
          })
          .then(response => response.json())
          .then(result => {
              console.log('Success:', result);
              alert('Datos cargados exitosamente')
          })
          .catch(error => {
              console.error('Error:', error);
              alert('Ya Valio!!!')
          });

      }
      reader.onerror = function (evt) {
          
      }
  }
}