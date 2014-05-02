function eliminarFase(id, url){
	console.log("Eliminar Fase");
	console.log(id);
	console.log(url);

	$("#nombre-fase").text(id);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}


function modificarFase(id, nro, nombre, descripcion, estado){
	console.log("MODIFICAR FASE");
	console.log(nro)
	console.log(nombre);
	console.log(descripcion);
	console.log("------------------");

	$("#m-id").val(id);
	$("#m-numero").val(nro)
	$("#m-nombre").val(nombre);
	$("#m-descripcion").val(descripcion);
	$("#m-estado").val(estado);
	
	$("#modal-modificar").modal('show');

}