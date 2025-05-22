function filtrarVisitas() {
    const input = document.getElementById('visita_input').value.toLowerCase();
    const lista = document.getElementById('lista_visitas');
    const items = lista.getElementsByTagName('li');

    // Mostrar la lista si hay texto en el campo de entrada
    lista.style.display = input ? 'block' : 'none';

    for (let i = 0; i < items.length; i++) {
        const texto = items[i].innerText.toLowerCase();
        items[i].style.display = texto.includes(input) ? '' : 'none';
    }
}

function seleccionarVisita(id, nombre) {
    // Asignar el ID seleccionado al campo oculto
    document.getElementById('visita_id').value = id;

    // Mostrar el nombre seleccionado en el campo de entrada
    document.getElementById('visita_input').value = nombre;

    // Ocultar la lista
    document.getElementById('lista_visitas').style.display = 'none';
}