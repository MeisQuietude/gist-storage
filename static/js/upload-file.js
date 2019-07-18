const fileInput = document.getElementById('upload-file');
const urlInput = document.getElementById('upload-link');

if (window.File && window.FileReader && window.FileList && window.Blob) {
    const codeArea = document.querySelector('textarea[name=code]');
    const filenameArea = document.querySelector('input[name=filename]');

    fileInput.onchange = () => {
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
    };

    urlInput.onclick = async () => {
        const getRequest = async (url) => {
            try {
                const endpoint = `/api/file/${url}`;
                const response = await fetch(endpoint);
                if (response.ok) {
                    return response.json();
                }
                throw new Error("Can't get response from request to URL")
            } catch (e) {
                console.error(e);
            }
        };

        const url = await prompt('Enter your url');
        const {filename, content} = await getRequest(url);

        filenameArea.value = filename;
        codeArea.innerHTML = content;
    }

} else {
    fileInput.disable();
    urlInput.disable();
}