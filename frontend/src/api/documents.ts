import api from './client';

export type UploadResponse = {
  message: string;
  file_id: string;
  task_id: string;
};

export type JobStatus = {
  task_id: string;
  status: string;
  done: boolean;
  result?: unknown;
  error?: string;
};

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const form = new FormData();
  form.append('file', file);

  const response = await api.post('/documents/upload/', form, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
}

export async function getJobStatus(taskId: string): Promise<JobStatus> {
  const response = await api.get(`/documents/jobs/${taskId}/`);
  return response.data;
}
