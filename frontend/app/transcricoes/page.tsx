import { Download } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { apiGet, downloadUrl } from '@/lib/api'
import { formatBytes, formatDate } from '@/lib/utils'
import type { TranscricaoDate } from '@/lib/types'

export default async function TransricoesPage() {
  let transcricoes: TranscricaoDate[] = []
  try {
    transcricoes = await apiGet<TranscricaoDate[]>('/transcricoes')
  } catch {
    // api offline
  }

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold text-zinc-900">Transcricoes</h1>
        <p className="text-sm text-zinc-500 mt-1">
          Arquivos de texto gerados, organizados por data.
        </p>
      </div>

      {transcricoes.length === 0 ? (
        <p className="text-sm text-zinc-500 py-4">
          Nenhuma transcricao encontrada ainda.
        </p>
      ) : (
        <div className="space-y-4">
          {transcricoes.map(grupo => (
            <Card key={grupo.date}>
              <CardHeader>
                <CardTitle className="text-base">{formatDate(grupo.date)}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="divide-y divide-zinc-100">
                  {grupo.files.map(file => (
                    <div
                      key={file.path}
                      className="flex items-center justify-between py-2.5"
                    >
                      <div>
                        <p className="text-sm font-medium text-zinc-800">{file.name}</p>
                        <p className="text-xs text-zinc-400">{formatBytes(file.size)}</p>
                      </div>
                      <a href={downloadUrl(grupo.date, file.name)} download>
                        <Button variant="outline" size="sm" className="gap-1.5">
                          <Download size={14} />
                          Download
                        </Button>
                      </a>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
