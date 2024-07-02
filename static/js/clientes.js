var getUrlParameter = function getUrlParameter(sParam) {
  var sPageURL = window.location.search.substring(1),
    sURLVariables = sPageURL.split("&"),
    sParameterName,
    i;

  for (i = 0; i < sURLVariables.length; i++) {
    sParameterName = sURLVariables[i].split("=");

    if (sParameterName[0] === sParam) {
      return sParameterName[1] === undefined
        ? true
        : decodeURIComponent(sParameterName[1]);
    }
  }
  return false;
};

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Script toggle formulario vehiculo

$("#agregarVehiculo").on("click", function () {
  $("#vehiculoCliente").toggleClass("d-none");
});

// Script para sacar el check del checkbox al cargar la pagina

window.onload = function () {
  var checkbox = document.getElementById("agregarVehiculo");
  checkbox.checked = false;
};

// Script mostrar botones

$("tr").on("click", function () {
  if ($(this).hasClass("selected")) {
    $("#btnEliminar").addClass("disabled");
    $("#btnInspeccionar").addClass("disabled");
  } else {
    $("#btnEliminar").removeClass("disabled");
    $("#btnInspeccionar").removeClass("disabled");
  }
});

// Script actualizar btn eliminar

$("#btnEliminar").on("click", function () {
  const cliente_selec =
    document.getElementsByClassName("selected")[0].children[0].id;


    const url = $(this).attr("data-url").slice(0, -1);

  while (url[url.length-1] != "/") {
    url = url.slice(0, -1)
  }
  
  url = url + cliente_selec + "/";

  $.ajax({
    url: url,
    cache: "false",
    dataType: "json",
    method: "POST",
    type: "POST",
    data: {
      csrfmiddlewaretoken: getCookie("csrftoken"),
    },
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      location.reload();
    },
  });
  return false;
});

$(document).on("show.bs.modal", "#clienteModal", function() {
  var recipient = $(".selected").children().attr("id");

  $("input", this).prop("readonly", true);
  $("input", this).prop("disabled", true);
  $("#btnEditarModal").removeClass("d-none");
  $("#btnGuardarCambiosModal").addClass("d-none");

  var actionForm = $("#formEditarModal").attr("action").slice(0, -1);
  var urlVehiculos = $("#listaVehiculos").attr("data-url").slice(0, -1);
  var urlAtenciones = $("#listaAtenciones").attr("data-url").slice(0, -1);

  while (actionForm[actionForm.length-1] != "/") {
    actionForm = actionForm.slice(0, -1)
  }

  while (urlVehiculos[urlVehiculos.length-1] != "/") {
    urlVehiculos = urlVehiculos.slice(0, -1)
  }

  while (urlAtenciones[urlAtenciones.length-1] != "/") {
    urlAtenciones = urlAtenciones.slice(0, -1)
  }
  
  actionForm = actionForm + recipient + "/";
  urlVehiculos = urlVehiculos + recipient + "/";
  urlAtenciones = urlAtenciones + recipient + "/";

  $("#formEditarModal").attr("action", actionForm);

  var modalTitle = $(this).find(".modal-title");
  modalTitle.text("Cliente ID: " + recipient);

  $.getJSON( actionForm, function( data ) {
    var campos = data[0].fields;
    $("#formEditarModal #id_nombreCompleto").val(campos['nombreCompleto']);
    $("#formEditarModal #id_rut").val(campos['rut']);
    $("#formEditarModal #id_email").val(campos['email']);
  });
  
  $.getJSON( urlVehiculos, function( data ) {
    var i;
    $("#listaVehiculos").text("");
    if (data['vehiculos'].length == 0) {
      $("#listaVehiculos").append("<p>No hay vehículos registrados</p>");
    } else {
    for (i = 0; i < data['vehiculos'].length; ++i) {
        $("#listaVehiculos").append("<a href='#' class='list-group-item list-group-item-action'><div class='d-flex w-100 justify-content-between'><h5 class='mb-1'>" + data['vehiculos'][i].nombre + "</h5><small class='text-body-secondary'>" + data['vehiculos'][i].patente + "</small></div><p class='mb-1'>" + data['vehiculos'][i].descripcion + "</p></a>");
    }
  }
  });

  $.getJSON( urlAtenciones, function( data ) {
    var i;
    $("#listaAtenciones").text("");
    if (data['atenciones'].length == 0) {
      $("#listaAtenciones").append("<p>No hay atenciones registrados</p>");
    } else {
    for (i = 0; i < data['atenciones'].length; ++i) {
        if (data['atenciones'][i].estado == "P") { var estado = "Pendiente"; } else { var estado = "Atendida"; }
        var fechaMal = data['atenciones'][i].fechaInicio.split('-');
        var fecha = fechaMal[2] + '-' + fechaMal[1] + '-' + fechaMal[0];
        console.log(fecha);
        $("#listaAtenciones").append("<a href='#' class='list-group-item list-group-item-action'><div class='d-flex w-100 justify-content-between'><h5 class='mb-1'>" + fecha + "</h5><small class='text-body-secondary'>" + estado + "</small></div><p class='mb-1'>" + data['atenciones'][i].descripcion + "</p></a>");
    }
  }
  });
});

$("#btnEditarModal").on("click", function () {
  $("#formEditarModal input").prop("readonly", false);
  $("#formEditarModal input").prop("disabled", false);
  $("#btnGuardarCambiosModal").removeClass("d-none");
  $(this).addClass("d-none");
});