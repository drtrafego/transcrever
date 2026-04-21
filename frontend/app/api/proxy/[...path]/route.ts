import { type NextRequest, NextResponse } from 'next/server'

const BACKEND = process.env.API_URL || 'http://localhost:8765'

async function handler(req: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  const { path } = await params
  const backendUrl = `${BACKEND}/${path.join('/')}${req.nextUrl.search}`

  const headers = new Headers()
  req.headers.forEach((value, key) => {
    if (!['host', 'connection'].includes(key)) headers.set(key, value)
  })

  let body: BodyInit | undefined
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    body = await req.arrayBuffer()
  }

  const res = await fetch(backendUrl, {
    method: req.method,
    headers,
    body,
  })

  const resHeaders = new Headers()
  res.headers.forEach((value, key) => {
    if (!['transfer-encoding', 'connection'].includes(key)) resHeaders.set(key, value)
  })

  return new NextResponse(res.body, {
    status: res.status,
    headers: resHeaders,
  })
}

export const GET = handler
export const POST = handler
export const PUT = handler
export const DELETE = handler
export const PATCH = handler
