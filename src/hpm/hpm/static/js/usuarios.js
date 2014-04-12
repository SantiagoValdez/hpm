function eliminarUsuario(id, url){
	console.log("Eliminar Usuario");
	console.log(id);
	console.log(url);

	$("#nombre-usuario").text(id);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}
