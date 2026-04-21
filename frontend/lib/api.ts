const BACKEND = process.env.API_URL || 'http://31.97.21.249:8765'

function backendUrl(path: string) {
  if (typeof window === 'undefined') {
    return `${BACKEND}${path}`
  }
  return `/api/proxy${path}`
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(backendUrl(path), { cache: 'no-store' })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(backendUrl(path), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export function downloadUrl(date: string, filename: string) {
  return `/api/proxy/transcricoes/${date}/${encodeURIComponent(filename)}`
}
