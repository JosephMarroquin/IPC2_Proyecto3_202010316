//Resumen



function graficarResumen(){

    var fecha = document.getElementById("fecha");

    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
  
  
    if(fecha.value==''){
        alert('Debe llenar todos los campos')
        return
    }
  
    fetch('http://localhost:5000/graficaR',
    {
        method:'POST',
        headers,
        body: `{
                "fecha":"${fecha.value}"
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

function generatePDF(){
    const element=document.getElementById("resumenPDF");
    html2pdf().from(element).set({
          margin: 1,
          filename: 'reporte resumen.pdf',
          html2canvas: { scale: 2 },
          jsPDF: {orientation: 'portrait', unit: 'in', format: 'letter', compressPDF: true}
        })
    .save();
}