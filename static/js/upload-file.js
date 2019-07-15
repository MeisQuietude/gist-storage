const fileInput = document.querySelector('input[type=file]');

if (window.File && window.FileReader && window.FileList && window.Blob) {
    fileInput.onchange = () => {
        const codeArea = document.querySelector('textarea[name=code]');
        const filenameArea = document.querySelector('input[name=filename]');
        const file = fileInput.files[0];
        const reader = new FileReader();

        if (file.type.match(/text.*/)) {
            reader.onload = (event) => {
                filenameArea.value = file.name;
                codeArea.innerHTML = event.target.result;
            }
        } else {
            alert("Unsupported file type! ");
        }

        reader.readAsText(file);
    }
} else {
    fileInput.disable()
}