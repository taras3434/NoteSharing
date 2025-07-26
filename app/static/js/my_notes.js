function updateFavoriteStatus(checkbox) {
    const noteId = checkbox.dataset.id;
    const isDone = checkbox.checked;

    fetch('/set-favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: noteId,
            is_done: isDone
        })
    })
    .then(res => res.json())
};