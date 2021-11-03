

//salida

const output = document.getElementById('output');
const documentVer = document.getElementById('ver');

documentVer.addEventListener('change', (e)=> {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.readAsText(file);
    reader.addEventListener('load', (e) => {
      output.innerHTML = reader.result;
    });
  });




//
