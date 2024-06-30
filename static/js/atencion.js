$(document).ready(function() {
    $("#agendaTable tbody tr").on("click", function() {
        // Remover la clase 'selected' de todas las filas
        $("#agendaTable tbody tr").removeClass("selected");
        // Agregar la clase 'selected' a la fila clickeada
        $(this).addClass("selected");
        
        // Habilitar el botón 'btnBoleta' si hay una fila seleccionada
        if ($(this).hasClass("selected")) {
            $("#btnBoleta").removeClass("disabled");
        } else {
            $("#btnBoleta").addClass("disabled");
        }
    });

    $("#btnBoleta").on("click", function() {
        // Obtener la fila seleccionada
        var selectedRow = $("#agendaTable tbody tr.selected");

        // Verificar si hay una fila seleccionada
        if (selectedRow.length === 0) {
            return false; // Salir si no hay ninguna fila seleccionada
        }

        // Obtener los datos de la fila seleccionada
        var atencionId = selectedRow.find("td:first").attr("id");
        var cliente = selectedRow.find("td:nth-child(1)").text();
        var vehiculo = selectedRow.find("td:nth-child(2)").text();
        var fechaAtencion = selectedRow.find("td:nth-child(3)").text();
        var descripcion = selectedRow.find("td:nth-child(4)").text();

        // Enviar los datos con una petición AJAX
        $.ajax({
            url: "/boleta/",
            type: "POST",
            data: {
                'atencion_id': atencionId,
                'cliente': cliente,
                'vehiculo': vehiculo,
                'fecha_atencion': fechaAtencion,
                'descripcion': descripcion,
                'csrfmiddlewaretoken': '{{ csrf_token }}' // Asegúrate de que tienes el token CSRF en tu plantilla
            },
            success: function(response) {
                // Manejar la respuesta del servidor
                console.log(response);
                // Aquí puedes agregar cualquier lógica adicional que necesites
            },
            error: function(xhr, errmsg, err) {
                // Manejar errores
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });

        return false;
    });
});