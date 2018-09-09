$(document).ready(() => {
    const $table = $('#message-table').DataTable({
        order: [[0, 'desc']],
        pageLength: 100,
        ajax: '/api/botMessages',
        columns: [
            {title: 'Timestamp', data: 'ts', render: renderTimestamp},
            {title: 'Channel', data: 'channel'},
            {title: 'Message', data: 'text'},
            {title: 'Remove', data: 'delete_url', render: renderMessage},
        ],
        responsive: true,
    });
    $('#message-table_wrapper').addClass('bs-select');

    $(document).on('click', '.delete-btn', deleteMessage);

    async function deleteMessage(e) {
        const url = $(e.currentTarget).data('delete');
        const result = await fetch(url);
        const json = await result.json();

        if (json.ok) {
            const $row = $(this).parents('tr');
            $row.fadeOut(400, deleteRow)
        }
    }

    function deleteRow($row) {
        $table.row($row)
            .remove()
            .draw()
    }

    function renderTimestamp(data) {
        return new Date(data * 1e3).toISOString()
    }

    function renderMessage(data) {
        return `
                <button class="btn btn-sm btn-danger delete-btn" data-delete=${data}>
                    Delete
                </button>`;
    }
});

