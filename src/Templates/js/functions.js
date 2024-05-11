function request(metod, url, params = []) {
    var result = null;    
    let query;

    if(params.length > 1)
    {        
        for (let i = 0; i < params.length; i++) {            
            query = '';
            
            if (i == 0) {
                query += '?';
            } else {
                query += '&';
            }
            url += query + encodeURIComponent(params[i].name) + '=' + encodeURIComponent(params[i].value);            
        }
    }

    $.ajax({
      url: url,
      type: metod,
      async: false,
      success: function(data, textStatus, xhr) {
        result = { data: data, status: xhr.status };
      },
      error: function(xhr, textStatus, errorThrown) {
        result = { data: null, status: xhr.status };
      }
    });

    return result;
  }

 function sendFile(file, url, callbackSuccess, callbackError) {
    var formData = new FormData();
    formData.append('file', file);

    $.ajax({
        url: url,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (typeof callbackSuccess === 'function') {
                callbackSuccess(response.message);
            }
            else{
                console.log('Arquivo foi enviado com sucesso.')
            }
        },
        error: function(xhr, status, error) {
            if (typeof callbackError === 'function') {
                response = xhr.responseJSON.detail
                callbackError(response);
            }
            else{
                console.error('Erro ao enviar arquivo:', error);
            }
        }
    });
}

function showAlertForm(alertElementId, response, isError){
    alertElement = $('#'+alertElementId)
    if(!$(alertElement).length){
        return;
    }
    if(isError){
        $(alertElement).addClass('alert-danger');
        $(alertElement).removeClass('alert-success');
    }
    else{
        $(alertElement).addClass('alert-success');
        $(alertElement).removeClass('alert-danger');
    }

    $(alertElement).text(response)
    alertElement.css({'display': 'block'})
    if(!isError){
        alertElement.delay(3000).fadeOut('slow');
    }
}