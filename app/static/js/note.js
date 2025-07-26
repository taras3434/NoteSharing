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

let quill = new Quill('#note-editor', {
    theme: 'bubble',
    readOnly: true,
    modules: { toolbar: false }
});

function editTitle(editTitleInput, titleBtn, saveTitleBtn) {
    editTitleInput.style.display = "inline-block";
    editTitleInput.focus();

    titleBtn.style.display = "none";
    saveTitleBtn.style.display = "inline-block";
}


function editeNote(editBtn, noteForm) {
    quill = new Quill('#note-editor', default_quill);

    editBtn.style.display = 'none';
    noteForm.classList.remove('hidden');
    
}

const noteForm = document.getElementById('note-form');
noteForm.addEventListener('submit', function (e) {
    const hiddenField = document.getElementById('flask-form-note');
    hiddenField.value = quill.root.innerHTML;
});