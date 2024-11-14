$(document).ready(function() {
    $('#fileDetailModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var fileId = button.data('file');
        
        $.ajax({
            url: '/myfile/file_details/' + fileId,
            success: function(data) {
                $('#fileDetailModal .modal-body').html(data);
            }
        });
    });
});