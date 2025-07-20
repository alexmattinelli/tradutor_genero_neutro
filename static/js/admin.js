// static/js/admin.js
document.getElementById('upload-btn').addEventListener('click', async () => {
    const fileInput = document.getElementById('file-input');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    const response = await fetch('/upload_imagem', {
        method: 'POST',
        body: formData
    });
    
    const data = await response.json();
    if (data.sucesso) {
        alert(`Imagem salva em: ${data.caminho}`);
    }
});