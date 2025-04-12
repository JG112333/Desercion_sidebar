// Mostrar mensaje de bienvenida cuando la página se carga
$(document).ready(function () {
    if ($('#chat-box').children().length === 0) {
        // Mostrar mensaje de bienvenida solo si no hay otros mensajes en el chat
        $('#chat-box').append('<div class="bot-message">Hola, ¿en qué puedo ayudarte sobre la deserción estudiantil?</div>');
    }
});

$('#chat-form').submit(function (e) {
    e.preventDefault();

    let userMessage = $('#user-message').val();

    // Mostrar el mensaje del usuario en el chat
    $('#chat-box').append('<div class="user-message">Tú: ' + userMessage + '</div>');
    $('#user-message').val('');  // Limpiar el input

    // Mostrar el spinner mientras se espera la respuesta
    $('#loading').show();

    // Enviar el mensaje al servidor
    $.ajax({
        url: '/chatbot',
        type: 'POST',
        data: {
            message: userMessage
        },
        success: function (response) {
            // Mostrar el mensaje del bot en el chat
            $('#chat-box').append('<div class="bot-message">Bot: ' + response.message + '</div>');
            $('#chat-box').find('.bot-message:last').html('Bot: ' + response.message);  // Permite texto en Negrita HTML
            $('#loading').hide();  // Ocultar el spinner
            $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);  // Desplazar hacia abajo
        },
        error: function (xhr, status, error) {
            console.error("Error: " + error);
            $('#loading').hide();  // Ocultar el spinner en caso de error
        }
    });
});

// Evento para el botón de recargar conversación
$('#reset-chat').click(function () {
    // Limpiar el chat
    $('#chat-box').empty();

    // Mostrar mensaje de bienvenida
    $('#chat-box').append('<div class="bot-message">Hola, ¿en qué puedo ayudarte sobre la deserción escolar?</div>');

    // Hacer que el chat se desplace al principio
    $('#chat-box').scrollTop(0);
});


// Evento para pegar en el input
function pasteText(iconElement) {
    const textElement = iconElement.parentElement.querySelector(".copy-text");
    const text = textElement.innerText.trim();

    // Pegamos el texto en el input
    const input = document.getElementById("user-message");
    input.value = text;
    input.focus(); // Enfoca el input, opcional

    // Feedback visual
    iconElement.innerText = "✅ Pegado!";
    setTimeout(() => {
        iconElement.innerText = "📋";
    }, 1500);
}