'use client'

import { useState, useRef, DragEvent } from 'react'
import { useRouter } from 'next/navigation'
import { Upload } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { formatBytes } from '@/lib/utils'

const ALLOWED = ['.mp4', '.m4a', '.ogg', '.wav', '.mp3', '.webm']
const UPLOAD_URL = 'https://api.transcrever.casaldotrafego.com/videos/upload'

export function VideoUpload() {
  const [dragging, setDragging] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [success, setSuccess] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const router = useRouter()

  function pickFile(f: File) {
    const ext = '.' + f.name.split('.').pop()?.toLowerCase()
    if (!ALLOWED.includes(ext)) {
      setError(`Extensao nao suportada: ${ext}`)
      return
    }
    setFile(f)
    setError(null)
    setSuccess(null)
  }

  function onDrop(e: DragEvent<HTMLDivElement>) {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files[0]
    if (f) pickFile(f)
  }

  async function handleUpload() {
    if (!file) return
    setUploading(true)
    setError(null)
    setSuccess(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch(UPLOAD_URL, {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setSuccess(`Upload concluido: ${data.filename} (${formatBytes(data.size)})`)
      setFile(null)
      router.refresh()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro no upload')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="space-y-3">
      <div
        onDragOver={e => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        className={`border-2 border-dashed rounded-lg p-8 flex flex-col items-center gap-3 cursor-pointer transition-colors ${
          dragging ? 'border-zinc-400 bg-zinc-50' : 'border-zinc-200 hover:border-zinc-300'
        }`}
      >
        <Upload size={24} className="text-zinc-400" />
        <div className="text-center">
          <p className="text-sm text-zinc-600">
            {file ? file.name : 'Arraste um arquivo ou clique para selecionar'}
          </p>
          {file && (
            <p className="text-xs text-zinc-400 mt-1">{formatBytes(file.size)}</p>
          )}
          {!file && (
            <p className="text-xs text-zinc-400 mt-1">
              {ALLOWED.join(', ')}
            </p>
          )}
        </div>
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          accept={ALLOWED.join(',')}
          onChange={e => {
            const f = e.target.files?.[0]
            if (f) pickFile(f)
          }}
        />
      </div>

      {error && (
        <p className="text-sm text-red-500 bg-red-50 border border-red-200 rounded-md px-3 py-2">
          {error}
        </p>
      )}
      {success && (
        <p className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-md px-3 py-2">
          {success}
        </p>
      )}

      {file && (
        <Button onClick={handleUpload} disabled={uploading} className="w-full">
          {uploading ? 'Enviando...' : 'Fazer Upload'}
        </Button>
      )}
    </div>
  )
}
