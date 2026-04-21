import type { Metadata } from 'next'
import { Geist } from 'next/font/google'
import Link from 'next/link'
import { FileVideo, ListChecks, FileText } from 'lucide-react'
import './globals.css'

const geist = Geist({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Transcrever',
  description: 'Transcricao de videos com Whisper',
}

const navLinks = [
  { href: '/', label: 'Videos', icon: FileVideo },
  { href: '/jobs', label: 'Jobs', icon: ListChecks },
  { href: '/transcricoes', label: 'Transcricoes', icon: FileText },
]

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" className={geist.className}>
      <body>
        <div className="flex min-h-screen bg-zinc-50">
          <aside className="w-56 shrink-0 border-r border-zinc-200 bg-white flex flex-col">
            <div className="px-6 py-5 border-b border-zinc-200">
              <span className="text-lg font-bold tracking-tight text-zinc-900">Transcrever</span>
            </div>
            <nav className="flex flex-col gap-1 p-3 flex-1">
              {navLinks.map(({ href, label, icon: Icon }) => (
                <Link
                  key={href}
                  href={href}
                  className="flex items-center gap-3 px-3 py-2 rounded-md text-sm text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900 transition-colors"
                >
                  <Icon size={16} />
                  {label}
                </Link>
              ))}
            </nav>
          </aside>
          <main className="flex-1 p-8 overflow-auto">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
