window.onload = () => {
    const gists = document.querySelector('#gists');
    const submitBtns = document.querySelectorAll('button[type=submit]');

    const addBtn = document.querySelector('#addBtn');
    addBtn.onclick = () => {
        const gist = getGistHTML();
        gists.appendChild(gist);
    };

    const getGistHTML = () => {
        const setAttributes = (el, attrs) => {
            for (let attr in attrs) {
                const val = attrs[attr];
                el.setAttribute(attr, val)
            }
        };

        const gist = document.createElement('section');
        const filename = document.createElement('input');
        const delBtn = document.createElement('input');
        const codeArea = document.createElement('textarea');
        const actionSection = document.createElement('section');
        const uploadLinkBtn = document.createElement('input');
        const uploadFileBtnWrap = document.createElement('button');
        const uploadFileBtn = document.createElement('input');

        gist.appendChild(filename);
        gist.appendChild(delBtn);
        gist.appendChild(codeArea);
        gist.appendChild(actionSection);

        actionSection.appendChild(uploadLinkBtn);
        actionSection.appendChild(uploadFileBtnWrap);
        uploadFileBtnWrap.appendChild(document.createTextNode('Upload file'));
        actionSection.appendChild(uploadFileBtn);

        setAttributes(gist, {
            'class': 'gist'
        });
        setAttributes(filename, {
            type: 'text',
            class: 'filename',
            name: 'filename',
            maxlength: 80,
            placeholder: 'Filename including extension...',
            required: true
        });
        setAttributes(delBtn, {
            type: 'button',
            class: 'delBtn',
            value: 'Delete this fragment'
        });

        setAttributes(codeArea, {
            class: 'codearea',
            name: 'code',
            autocomplete: 'off',
            spellcheck: false,
            required: true
        });
        setAttributes(actionSection, {
            class: 'additional-ways-enter-code'
        });
        setAttributes(uploadLinkBtn, {
            type: 'button',
            class: 'upload-link',
            value: 'External link'
        });
        setAttributes(uploadFileBtnWrap, {
            type: 'button',
            class: 'upload-file-btn-wrap'
        });
        setAttributes(uploadFileBtn, {
            type: 'file',
            class: 'upload-file-btn',
            id: 'upload-file'
        });

        uploadFileBtnWrap.addEventListener("click", () => {
            const clickEvent = document.createEvent('MouseEvents');
            clickEvent.initMouseEvent('click', true, true, window,
                0, 0, 0, 0, 0,
                false, false, false, false, 0, null);
            uploadFileBtn.dispatchEvent(clickEvent);
        });


        uploadFileBtn.addEventListener("change", () => {
            const file = uploadFileBtn.files[0];
            if (!file) return;

            const maxFileSize = 1024 * 64;  // 64 KB
            if (file.size > maxFileSize) {
                return alert(`Max file size is ${maxFileSize / 1024} KB`);
            }

            const reader = new FileReader();

            if (file.type.match(/text.*/)) {
                reader.onloadstart = () => {
                    submitBtns.forEach(btn => btn.setAttribute('disabled', '1'));
                };
                reader.onloadend = () => {
                    submitBtns.forEach(btn => btn.removeAttribute('disabled'));
                };
                reader.onload = (event) => {
                    filename.value = file.name;
                    codeArea.innerHTML = event.target.result;
                }
            } else {
                return alert("Unsupported file type! ");
            }

            reader.readAsText(file);
        });

        uploadLinkBtn.addEventListener("click", async () => {
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
            const isValidURL = url =>
                /^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:[/?#]\S*)?$/i
                    .test(url);

            const url = await prompt('Enter your url');
            if (!url) return;
            if (!isValidURL(url)) return alert('URL is not valid!');

            submitBtns.forEach(btn => btn.setAttribute('disabled', '1'));
            const response = await getRequest(url);
            submitBtns.forEach(btn => btn.removeAttribute('disabled'));

            filename.value = response.filename;
            codeArea.innerHTML = response.content;
        });

        delBtn.addEventListener("click", () => {
            gists.removeChild(gist);
        });


        return gist;
    };
    addBtn.click();
};