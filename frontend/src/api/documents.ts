import api from './client';

export async function uploadDocument(file: File): Promise<void> {
    const form = new FormData();
    form.append('file', file);

    const response = await api.post('/documents/upload/', form, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    return response.data;
}