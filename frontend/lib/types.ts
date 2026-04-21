export interface VideoFile {
  name: string
  size: number
  extension: string
}

export interface Job {
  job_id: string
  filename: string
  status: 'pending' | 'processing' | 'done' | 'error'
  output_path?: string
  error?: string
}

export interface TranscricaoDate {
  date: string
  files: Array<{ name: string; size: number; path: string }>
}
