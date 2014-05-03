function eliminarAtributoTipoItem(id, url){
	console.log("Eliminar Fase");
	console.log(id);
	console.log(url);

	$("#nombre-atributotipoitem").text(id);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}


function modificarAtributoTipoItem(id, nombre, tipo, valor_por_defecto){
	console.log("MODIFICAR TIPO ITEM");
	console.log(id)
	console.log(nombre);
	console.log(tipo);
	console.log(valor_por_defecto);
	console.log("------------------");

	$("#m-id").val(id);
	$("#m-nombre").val(nombre);
	$("#m-tipo").val(tipo)
	$("#m-valor_por_defecto").val(valor_por_defecto);
	
	$("#modal-modificar").modal('show');

}