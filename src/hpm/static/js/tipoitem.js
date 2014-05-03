function eliminarTipoItem(id, url){
	console.log("Eliminar Fase");
	console.log(id);
	console.log(url);

	$("#nombre-tipoitem").text(id);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}


function modificarTipoItem(id, codigo, nombre, descripcion){
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

function mostrarInfoTipoItem(){

	var idti = $("#id-tipo").val();
	$.get( "/tipoitem/get/" + idti, function( data ) {
     	console.log( "Load was performed." + data);
     	var datos = JSON.parse(data);

     	if( datos ){
     		var item = datos;

     		$("#info-tipo-item").empty();

     		$("#info-tipo-item").append("<b>Atributos :</b> ");

     		if(item.atributos.length == 0){
     			$("#info-tipo-item").append("ninguno...");
     		}
     		for(var i=0; i < item.atributos.length; i++){
				var a = item.atributos[i];
				$("#info-tipo-item").append("<p>" + a.nombre + " - tipo : " + a.tipo + " def : " + a.valor_por_defecto +"</p>" );
     		}

     	}

	});
	

}