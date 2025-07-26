// Initialize Quill editor with snow theme
const quill = new Quill('#note-creator', {
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
    }});
        
    // Reference to form and hidden textarea
    const form = document.getElementById('note-form');
    const hiddenField = document.getElementById('flask-form-note');

    // On form submit, copy Quill editor HTML to hidden textarea
    form.addEventListener('submit', function (e) {
        hiddenField.value = quill.root.innerHTML;
    });