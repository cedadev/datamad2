$(".claim-btn").click(function (event) {

    // Set needed variables
    let btn_value;
    let action;

    const claim_key = "claimed";

    // Get values from the data attributes on the button
    var claimed = event.target.classList.contains(claim_key);
    let id = event.target.dataset.id;

    // Prepare values for the URL and button after the fact
    if (claimed) {
        btn_value = 'CLAIM';
        action = 'unclaim';

    } else {
        btn_value = 'UNCLAIM';
        action = 'claim';
    }

    $.ajax({
        type: "GET",
        url: ['/grant', id, action].join('/'),

        // handle a successful response
        success: function () {
            event.target.innerHTML = btn_value;

            if (claimed){
                event.target.classList.remove(claim_key);
            } else {
                event.target.classList.add(claim_key);
            }
        },
        // handle a non-successful response
        error: function () {
            alert('Failed');
        }
    });
});
