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
  const url = $(this).attr("data-url").slice(0, -1) + cliente_selec;

  data = {
    csrfmiddlewaretoken: getCookie("csrftoken"),
  };
  $.ajax({
    url: url,
    cache: "false",
    dataType: "json",
    method: "POST",
    type: "POST",
    data: data,
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      location.reload();
    },
  });
  return false;
});

// Cambiar contenido del Modal

const modalCliente = document.getElementById("clienteModal");
if (modalCliente) {
  modalCliente.addEventListener("show.bs.modal", (event) => {
    const recipient =
      document.getElementsByClassName("selected")[0].children[0].id;
    // Update the modal's content.
    const modalTitle = modalCliente.querySelector(".modal-title");
    // const modalBodyInput = myModal.querySelector('.modal-body input')

    modalTitle.textContent = `Cliente ID: ${recipient}`;
    // modalBodyInput.value = recipient
  });
}
