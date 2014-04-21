function eliminarRol(id, url){
	console.log("Eliminar Rol");
	console.log(id);
	console.log(url);

	$("#nombre-rol").text(id);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}


function modificarRol(id, nombre, descripcion , proyecto){
	console.log("MODIFICAR ROL");
	console.log(nombre);
	console.log(descripcion);
	console.log(proyecto);
	console.log("------------------");

	$("#m-id").val(id);
	$("#m-nombre").val(nombre);
	$("#m-descripcion").val(descripcion);
	//$("#m-permisos").val(permisos);
	$("#m-nombre").prop('readonly', true);
	if (proyecto == "" ) {
		$("#m-nombre").prop('readonly', false);
		proyecto = "0";
	}
	console.log(proyecto);
	$("#m-proyecto").val(proyecto);

	$("#modal-modificar").modal('show');

}