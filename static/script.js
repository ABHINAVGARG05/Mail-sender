// Select DOM elements
const loginForm = document.getElementById('loginForm');
const uploadForm = document.getElementById('uploadForm');
const alertBox = document.getElementById('alert');
const loginDiv = document.getElementById('login-form');
const uploadDiv = document.getElementById('upload-form');

// Helper function to show alerts
function showAlert(message, type = 'success') {
    alertBox.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
}

// Login Form Submission
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

// File Upload Form Submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const file = document.getElementById('file').files[0];
    const email = document.getElementById('Email').value; // Get Email field value
    const passwordEmail = document.getElementById('Password-Email').value; // Get Password-Email field value
    const message = document.getElementById('Subject').value;

    if (!file) {
        showAlert('Please select a file to upload', 'danger');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('Email', email);
    formData.append('Password-Email', passwordEmail);
    formData.append('Subject',message);

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
