
function hoy(){
	/*
		as saw in http://stackoverflow.com/a/4929629
	*/

	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1; //January is 0!
	var yyyy = today.getFullYear();

	if(dd<10) {
	dd='0'+dd
	} 

	if(mm<10) {
	mm='0'+mm
	} 

	today = mm+'/'+dd+'/'+yyyy;

	return today
}


function eliminarProyecto(nombre, url){
	console.log("Eliminar Proyecto");
	console.log(nombre);
	console.log(url);

	$("#nombre-proyecto").text(nombre);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}


function modificarProyecto(id,nombre,descripcion,fecha_creacion,complejidad_total,estado){
	
	console.log("Modificar Proyecto");
	console.log(id);
	console.log(nombre);
	console.log(descripcion);
	console.log(fecha_creacion);
	console.log(complejidad_total);
	console.log(estado);
	console.log("---------__-------")


	$("#m-id").val(id);
	$("#m-nombre").val(nombre);
	$("#m-descripcion").val(descripcion);
	$("#m-fecha_creacion").val(fecha_creacion);
	$("#m-complejidad_total").val(complejidad_total);
	$("#m-estado").val(estado);
	
	$('#m-fecha_creacion').datepicker({
	    format: 'dd/mm/yyyy'
	});
	$('#m-fecha_creacion').datepicker('update', fecha_creacion);

	$("#modal-modificar").modal('show');

}