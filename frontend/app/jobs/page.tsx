import { JobsTable } from '@/components/JobsTable'

export default function JobsPage() {
  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold text-zinc-900">Jobs</h1>
        <p className="text-sm text-zinc-500 mt-1">
          Acompanhe o progresso das transcricoes. Atualiza automaticamente a cada 3 segundos.
        </p>
      </div>
      <JobsTable />
    </div>
  )
}
