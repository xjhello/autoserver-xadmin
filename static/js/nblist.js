
    function init_thead(thead_dic){

        $.each(thead_dic, function(k,v){
            th_str = v.title;
            var th = document.createElement('th');
            th.innerText = th_str;

            $('#thead').append(th);
        });
    }

    function init_tbody(data_list, thead_dic){
        /**
         *  [
         *      {'id': 1, 'hostname': 'c1.com', 'sn': '432t4173t21'},
         *      {'id': 2, 'hostname': 'c2.com', 'sn': 'gfdgfd43432'}
         *  ]
         */
        $.each(data_list, function(k,v){
             var tr = document.createElement('tr');
             $.each(thead_dic, function (k, configitem) {
                 /**
                  * {
                        "field": 'sn',
                        "title": 'sn号',
                    }
                  * @type {HTMLTableDataCellElement}
                  */
                 var td = document.createElement('td');
                 td.innerText = v[configitem['field']];
                 console.log(td);
                 tr.append(td)
             });
             $('#tbody').append(tr);
        });


    }