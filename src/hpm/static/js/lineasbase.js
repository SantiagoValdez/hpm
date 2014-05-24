function eliminarLineaBase(id, url){
	console.log("Eliminar Linea Base");
	console.log(id);
	console.log(url);

	$("#nombre-lineabase").text(id);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}

function eliminarLineaBase(id, url){
	console.log("Eliminar Item Linea Base");
	console.log(id);
	console.log(url);

	$("#nombre-item").text(id);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}

function modificarLineaBase(id, nro, nombre, estado){
	console.log("MODIFICAR LINEA BASE");
	console.log(nro)
	console.log(nombre);
	console.log(estado);
	console.log("------------------");

	$("#m-id").val(id);
	$("#m-numero").val(nro);
	$("#m-nombre").val(nombre);
	$("#m-estado").val(estado);
	
	$("#modal-modificar").modal('show');

}