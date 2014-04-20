function eliminarUsuario(id, url){
	console.log("Eliminar Usuario");
	console.log(id);
	console.log(url);

	$("#nombre-usuario").text(id);
	$("#modal-eliminar").modal('show');
	$("#btn-eliminar").attr('href', url);

}


function modificarUsuario(id,username,nombre,apellido,email,telefono,ci,password){
	console.log("MODIFICAR USUARIO");
	console.log(id);
	console.log(username);
	console.log(nombre);
	console.log(apellido);
	console.log(telefono);
	console.log(ci);
	console.log(password)
	console.log("------------------");


	$("#m-id").val(id);
	$("#m-username").val(username);
	$("#m-nombre").val(nombre);
	$("#m-apellido").val(apellido);
	$("#m-email").val(email);
	$("#m-telefono").val(telefono);
	$("#m-ci").val(ci);
	$("#m-password").val(password);

	$("#modal-modificar").modal('show');

}