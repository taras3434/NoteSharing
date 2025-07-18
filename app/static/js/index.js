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

class TextEditor extends Quill {
    constructor(tag_id, config = default_quill) {
        super(tag_id, config);
        this.config = config;  // store current config
    }
}