const gists = document.querySelector('#gists');
const gist = document.querySelector('.gist').cloneNode(true);

const addBtn = document.querySelector('#addBtn');
addBtn.onclick = () => {
    const gistCloned = gist.cloneNode(true);
    gistCloned.querySelector('.delBtn').onclick = (e) => {
        const el = e.target.parentNode;
        el.parentNode.removeChild(el);
    };
    gists.appendChild(gistCloned);
};