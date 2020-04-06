$(document).ready(function() {
    var table = $('#grants').DataTable( {
        // columnDefs: [{
        //     targets: [4],
        //     render: function (data, type) {
        //         if (data !== null) {
        //             var wrapper = moment(new Date(parseInt(data.substr(6))));
        //             return wrapper.format("M/D/YYYY h:mm:ss A");
        //         }
        //     }
        // }],
        columnDefs: [{ 'targets': 4, type: 'date-euro' }],
        order: [[4, 'desc']],
        stateSave: true
    } );

    new $.fn.dataTable.FixedHeader( table );
} );

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
})


$( ".claim-btn" ).click(function(){
        let btn = $(this);
        let url = 'grant/' + $(this).attr('data-id') + '/claim';
        let cell = btn.parent();

        $.ajax({
            type: "GET",
            url: url,

            // handle a successful response
            success: function () {
                cell.html("CLAIMED");
                cell.attr('id', 'claim');
            },
            // handle a non-successful response
            error: function () {
                alert('Claim failed');
            }
        });
    });

