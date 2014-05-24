function eliminarMensaje(asunto, url){
	console.log("Eliminar Proyecto");
	console.log(asunto);
	console.log(url);

	$("#asunto-mensaje").text(asunto);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}