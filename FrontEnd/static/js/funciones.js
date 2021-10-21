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