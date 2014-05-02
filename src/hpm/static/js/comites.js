

function eliminarMiembro(nombre, url){
	console.log("Eliminar Miembro Comite");
	console.log(nombre);
	console.log(url);

	$("#nombre-usuario").text(nombre);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}