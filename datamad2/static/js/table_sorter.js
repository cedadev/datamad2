function display_hidden_facets(event, el, prefix, facet) {
    let hidden = $(el + '[id='+ prefix + facet + ']')
    hidden.toggleClass('d-none')

    let e = $(event)
    let message = e.attr('data-label')
    if (e.html() === message ){
        e.html("Hide")
    } else {
        e.html(message)
    }
}

$('.clear-facets').click(function (event) {
    event.preventDefault();
    let facet = $(this).attr('data-facet')
    let urlParams = new URLSearchParams(window.location.search)
    let selectedFacets = urlParams.getAll('selected_facets')

    // Search to see if the facet is in the list
    let findex = -1;
    for (let i = 0; i < selectedFacets.length; i++) {
        if (selectedFacets[i].startsWith(facet)) {
            findex = i;
            break;
        }
    }

    // Delete the facet
    if (findex > -1) {
        selectedFacets.splice(findex, 1);
    }

    // Delete all selected facets
    urlParams.delete('selected_facets')

    // Re-add any remaining facets
    selectedFacets.forEach(function (facet) {
        urlParams.append('selected_facets', facet)
    })

    // Handle adding the search character
    let new_qs = urlParams.toString();
    if (new_qs) {
        new_qs = '?' + new_qs
    }

    // Reload page with changes
    window.location.href = window.location.origin + new_qs;

})

$(function () {
    $('[data-toggle="tooltip"]').tooltip();
})


$(".claim-btn").click(function () {
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
