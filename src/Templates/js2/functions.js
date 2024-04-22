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
  
result = request('GET', '/report-sickness-grouped', [
    {
        'name': 'group', 'value': 'state_name'
    }, 
    {
        'name': 'start_date', 'value': '2022-02-02'
    },
    {
        'name': 'end_date', 'value': '2024-05-04'
    }
])

console.log(result)