function eliminarItem(id, url){
	console.log("Eliminar Fase");
	console.log(id);
	console.log(url);

	$("#nombre-item").text(id);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}

function revertirItem(version, id_version){
	console.log("Revertir item");
	console.log(id_version);


	$("#version-item").text(version);
	$("#id_version").val(id_version);
	$("#modal-revertir").modal('show');
}

function modificarItem(id, codigo, nombre, descripcion){
	console.log("MODIFICAR TIPO ITEM");
	console.log(id)
	console.log(codigo);
	console.log(nombre);
	console.log(descripcion);
	console.log("------------------");

	$("#m-id").val(id);
	$("#m-codigo").val(codigo)
	$("#m-nombre").val(nombre);
	$("#m-descripcion").val(descripcion);
	
	$("#modal-modificar").modal('show');

}

function setUrlNewItem(id_fase){

	var id_tipo = $("#id-tipo").val();
	
	var url = "/item/" + id_fase + "/nuevo/" + id_tipo + "/";

	console.log(url);

	$("#next-new-item").attr("href", url);
	

}

function setListaRelacion(){

	var tipo = $("#tipo").val();
	console.log(tipo)

	if(tipo == 'padre-hijo'){
		console.log("tipo padre-hijo");
		$("#s-hijo").removeClass('hide');
		$("#s-sucesor").addClass('hide');
	}else{
		console.log("tipo antecesor-sucesor");
		$("#s-sucesor").removeClass('hide');
		$("#s-hijo").addClass('hide');
	}

}

function eliminarRelacionItem(url){
	console.log("Eliminar Relacion Item");
	console.log(url);

	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}

function adjuntarArchivo(nombre){
	console.log("Adjuntar archivo a");
	console.log(nombre);

	$("#modal-modificar").modal('show');

}

function showImpacto(url){
	$.get( url, function( data ) {
     	console.log( "Load was performed." + data);
     	var datos = JSON.parse(data);

     	if( datos ){
     		var item = datos;

     		console.log(item);

     		$("#nombre-impacto-item").empty().append(""+item.nombre);
     		$("#impacto-item").empty().append(""+item.impacto);
     		
     		$("#modal-impacto").modal('show');

     	}

	});
}