import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { VideoList } from '@/components/VideoList'
import { VideoUpload } from '@/components/VideoUpload'
import { apiGet } from '@/lib/api'
import type { VideoFile } from '@/lib/types'

export default async function VideosPage() {
  let videos: VideoFile[] = []
  try {
    videos = await apiGet<VideoFile[]>('/videos')
  } catch {
    // api offline ou sem videos
  }

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold text-zinc-900">Videos</h1>
        <p className="text-sm text-zinc-500 mt-1">
          Selecione os arquivos para transcrever ou faca upload de novos.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Upload de Video</CardTitle>
        </CardHeader>
        <CardContent>
          <VideoUpload />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Arquivos Disponiveis ({videos.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <VideoList videos={videos} />
        </CardContent>
      </Card>
    </div>
  )
}
