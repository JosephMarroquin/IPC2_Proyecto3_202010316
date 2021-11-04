//Rango



function graficarRango(){

    var fechaI = document.getElementById("fechaI");
    var fechaF = document.getElementById("fechaF");

    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
  
  
    if(fechaI.value==''){
        alert('Debe llenar todos los campos')
        return
    }
  
    fetch('http://localhost:5000/graficaRango',
    {
        method:'POST',
        headers,
        body: `{
                "fechaI":"${fechaI.value}",
                "fechaF":"${fechaF.value}"
                }`
    })
    .then(response => response.json())
    .then(
        result => {
            console.log('Success:', result);
            alert('Graficando')
          }
    )
    .catch(
        error => {
            console.error('Error:', error);
            alert('Error!!!')
          }
    )
  
  }
