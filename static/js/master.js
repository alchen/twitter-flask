$(function() {
    $(document).on('click', '#more-link', function() {
        var url = this.href;
        var a = $(this);
        $.ajax({
            url: url,
            type: 'get',
            success: function (serverResponse) {
                if (serverResponse.success===true) {
                    $('#more').replaceWith(serverResponse.data);
                }
            },
            error: function () {
                // fail silently : p
            }
        });
        return false;
    });
});
