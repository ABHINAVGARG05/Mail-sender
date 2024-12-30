const loginForm = document.getElementById('loginForm');
const uploadForm = document.getElementById('uploadForm');
const alertBox = document.getElementById('alert');
const loginDiv = document.getElementById('login-form');
const uploadDiv = document.getElementById('upload-form');
const htmlTemplateInput = document.getElementById('HTML'); // For HTML template input
const previewContainer = document.getElementById('preview-container'); // For preview container
const previewContent = document.getElementById('previewContent'); // For live preview

function showAlert(message, type = 'success') {
    alertBox.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
}

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const userId = document.getElementById('userId').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: userId, password })
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('authToken', data.token);
            showAlert('Login successful!', 'success');
            loginDiv.style.display = 'none';
            uploadDiv.style.display = 'block';
        } else {
            showAlert(data.error || 'Login failed', 'danger');
        }
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'danger');
    }
});

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const file = document.getElementById('file').files[0];
    const email = document.getElementById('Email').value;
    const passwordEmail = document.getElementById('Password-Email').value;
    const message = document.getElementById('HTML').value;

    if (!file) {
        showAlert('Please select a file to upload', 'danger');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('Email', email);
    formData.append('Password-Email', passwordEmail);
    formData.append('Subject', message);

    try {
        const token = localStorage.getItem('authToken');
        const response = await fetch('/upload', {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${token}`
            },
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            showAlert('File uploaded and emails sent!', 'success');
        } else {
            showAlert(data.error || 'Upload failed', 'danger');
        }
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'danger');
    }
});

htmlTemplateInput.addEventListener('input', () => {
    const template = htmlTemplateInput.value;

    const highlightedTemplate = template.replace(/{{\s*([^}]+)\s*}}/g, `<span style="background-color: yellow;">{{$1}}</span>`);

    previewContent.innerHTML = highlightedTemplate;

    previewContainer.style.display = template.trim() ? 'block' : 'none';
});
