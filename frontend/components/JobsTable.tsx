'use client'

import { useState, useEffect } from 'react'
import { Download } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { apiGet, downloadUrl } from '@/lib/api'
import type { Job } from '@/lib/types'

function StatusBadge({ status }: { status: Job['status'] }) {
  if (status === 'pending') return <Badge variant="secondary">Pendente</Badge>
  if (status === 'processing') return (
    <Badge variant="processing" className="animate-pulse">Processando</Badge>
  )
  if (status === 'done') return <Badge variant="success">Concluido</Badge>
  return <Badge variant="destructive">Erro</Badge>
}

function parseOutputPath(outputPath: string): { date: string; filename: string } | null {
  const parts = outputPath.replace(/\\/g, '/').split('/')
  const transcricaoIdx = parts.findIndex(p => p === 'transcrição' || p === 'transcricao')
  if (transcricaoIdx === -1 || parts.length < transcricaoIdx + 3) return null
  return {
    date: parts[transcricaoIdx + 1],
    filename: parts[transcricaoIdx + 2],
  }
}

export function JobsTable() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true

    async function poll() {
      try {
        const data = await apiGet<Job[]>('/jobs')
        if (active) {
          setJobs(data)
          setError(null)
        }
      } catch (e) {
        if (active) setError(e instanceof Error ? e.message : 'Erro ao buscar jobs')
      }
    }

    poll()
    const interval = setInterval(poll, 3000)
    return () => {
      active = false
      clearInterval(interval)
    }
  }, [])

  if (error) {
    return (
      <p className="text-sm text-red-500 bg-red-50 border border-red-200 rounded-md px-3 py-2">
        {error}
      </p>
    )
  }

  if (jobs.length === 0) {
    return (
      <p className="text-sm text-zinc-500 py-4">
        Nenhum job encontrado. Selecione videos na pagina inicial para iniciar.
      </p>
    )
  }

  return (
    <div className="border border-zinc-200 rounded-lg overflow-hidden bg-white">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-zinc-200 bg-zinc-50">
            <th className="text-left px-4 py-3 font-medium text-zinc-600">Arquivo</th>
            <th className="text-left px-4 py-3 font-medium text-zinc-600">Status</th>
            <th className="text-left px-4 py-3 font-medium text-zinc-600">Acao</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-zinc-100">
          {jobs.map(job => {
            const parsed = job.output_path ? parseOutputPath(job.output_path) : null
            return (
              <tr key={job.job_id} className="hover:bg-zinc-50 transition-colors">
                <td className="px-4 py-3 text-zinc-800 font-medium max-w-xs truncate">
                  {job.filename}
                </td>
                <td className="px-4 py-3">
                  <StatusBadge status={job.status} />
                </td>
                <td className="px-4 py-3">
                  {job.status === 'done' && parsed && (
                    <a href={downloadUrl(parsed.date, parsed.filename)} download>
                      <Button variant="outline" size="sm" className="gap-1.5">
                        <Download size={14} />
                        Download
                      </Button>
                    </a>
                  )}
                  {job.status === 'error' && job.error && (
                    <span className="text-xs text-red-500 max-w-xs truncate block" title={job.error}>
                      {job.error}
                    </span>
                  )}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
