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
  const url = $(this).attr("data-url").slice(0, -2) + cliente_selec + "/";

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

  while (actionForm[actionForm.length-1] != "/") {
    actionForm = actionForm.slice(0, -1)
  }
  
  actionForm = actionForm + recipient + "/";

  $("#formEditarModal").attr("action", actionForm);

  var modalTitle = $(this).find(".modal-title");
  modalTitle.text("Cliente ID: " + recipient);

  $.getJSON( actionForm, function( data ) {
    var campos = data[0].fields;
    $("#formEditarModal #id_nombreCompleto").val(campos['nombreCompleto']);
    $("#formEditarModal #id_rut").val(campos['rut']);
    $("#formEditarModal #id_email").val(campos['email']);
  });
});

$("#btnEditarModal").on("click", function () {
  $("#formEditarModal input").prop("readonly", false);
  $("#formEditarModal input").prop("disabled", false);
  $("#btnGuardarCambiosModal").removeClass("d-none");
  $(this).addClass("d-none");
});