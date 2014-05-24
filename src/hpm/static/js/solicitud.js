function eliminarSolicitud(id, url){
	console.log("Eliminar Solicitud");
	console.log(id);
	console.log(url);

	$("#nombre-solicitud").text(id);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}

function enviarSolicitud(id, url){
	console.log("Enviar Solicitud");
	console.log(id);
	console.log(url);

	$("#nombre-solicitud-enviar").text(id);
	$("#modal-enviar").modal('show');
	$("#btn-enviar").attr('href', url);

}


function modificarSolicitud(id, item, nombre, descripcion, accion){
	console.log("MODIFICAR Solicitud");
	console.log(nombre);
	console.log(descripcion);
	console.log("------------------");

	$("#m-id").val(id);
	$("#m-nombre").val(nombre);
	$("#m-descripcion").val(descripcion);
	$("#m-accion").val(accion);
	$("#m-item").val(item);
	
	$("#modal-modificar").modal('show');

}