const default_quill = {
    theme: 'snow',
    readOnly: false,
    modules: {
        toolbar: [
            [{ header: [1, 2, false] }],
            ['bold', 'italic', 'underline', 'strike'],
            ['link', 'blockquote', 'code-block', 'image'],
            [{ list: 'ordered' }, { list: 'bullet' }],
            ['clean']
        ]
    }};

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

function edit_title() {
    const editTitleInput = document.getElementById("flask-form-title");
    const titleBtn = document.getElementById("title");
    const saveTitleBtn = document.getElementById('js-save-title-btn');

    editTitleInput.style.display = "inline-block";
    editTitleInput.focus();

    titleBtn.style.display = "none";
    saveTitleBtn.style.display = "inline-block";
}


function edit_note() {
    quill = new Quill('#note-editor', {
        theme: 'snow',
        readOnly: false,
        modules: {
            toolbar: [
                [{ header: [1, 2, false] }],
                ['bold', 'italic', 'underline', 'strike'],
                ['link', 'blockquote', 'code-block', 'image'],
                [{ list: 'ordered' }, { list: 'bullet' }],
                ['clean']
            ]
        }
    });

    document.getElementById('js-edit-note-btn').style.display = 'none';
    document.getElementById('note-form').classList.remove('hidden');
}