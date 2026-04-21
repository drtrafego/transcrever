'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { apiPost } from '@/lib/api'
import { formatBytes } from '@/lib/utils'
import type { VideoFile, Job } from '@/lib/types'

interface Props {
  videos: VideoFile[]
}

const EXT_COLORS: Record<string, 'default' | 'secondary' | 'outline'> = {
  '.mp4': 'default',
  '.mp3': 'secondary',
  '.m4a': 'secondary',
  '.ogg': 'outline',
  '.wav': 'outline',
  '.webm': 'outline',
}

export function VideoList({ videos }: Props) {
  const [selected, setSelected] = useState<Set<string>>(new Set())
  const [language, setLanguage] = useState('pt')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  function toggle(name: string) {
    setSelected(prev => {
      const next = new Set(prev)
      if (next.has(name)) next.delete(name)
      else next.add(name)
      return next
    })
  }

  function toggleAll() {
    if (selected.size === videos.length) {
      setSelected(new Set())
    } else {
      setSelected(new Set(videos.map(v => v.name)))
    }
  }

  async function handleTranscrever() {
    if (selected.size === 0) return
    setLoading(true)
    setError(null)
    try {
      await apiPost<{ jobs: Job[] }>('/jobs', {
        files: Array.from(selected),
        language,
      })
      router.push('/jobs')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Erro ao criar jobs')
      setLoading(false)
    }
  }

  if (videos.length === 0) {
    return (
      <p className="text-sm text-zinc-500 py-4">
        Nenhum video encontrado na pasta videos/.
      </p>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <label className="flex items-center gap-2 text-sm text-zinc-600 cursor-pointer">
          <Checkbox
            checked={selected.size === videos.length && videos.length > 0}
            onCheckedChange={toggleAll}
          />
          Selecionar todos
        </label>
        <select
          value={language}
          onChange={e => setLanguage(e.target.value)}
          className="ml-auto text-sm border border-zinc-200 rounded-md px-3 py-1.5 bg-white text-zinc-700 focus:outline-none focus:ring-1 focus:ring-zinc-400"
        >
          <option value="pt">Portugues</option>
          <option value="en">Ingles</option>
          <option value="es">Espanhol</option>
        </select>
        <Button
          onClick={handleTranscrever}
          disabled={selected.size === 0 || loading}
        >
          {loading ? 'Enviando...' : `Transcrever (${selected.size})`}
        </Button>
      </div>

      {error && (
        <p className="text-sm text-red-500 bg-red-50 border border-red-200 rounded-md px-3 py-2">
          {error}
        </p>
      )}

      <div className="divide-y divide-zinc-100 border border-zinc-200 rounded-lg bg-white">
        {videos.map(video => (
          <label
            key={video.name}
            className="flex items-center gap-4 px-4 py-3 cursor-pointer hover:bg-zinc-50 transition-colors"
          >
            <Checkbox
              checked={selected.has(video.name)}
              onCheckedChange={() => toggle(video.name)}
            />
            <span className="flex-1 text-sm text-zinc-800 font-medium truncate">
              {video.name}
            </span>
            <span className="text-xs text-zinc-400">{formatBytes(video.size)}</span>
            <Badge variant={EXT_COLORS[video.extension] ?? 'outline'}>
              {video.extension}
            </Badge>
          </label>
        ))}
      </div>
    </div>
  )
}
