'use client'

import { useQuery } from '@tanstack/react-query'
import Link from 'next/link'

async function fetchTodos() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/todos`)
  if (!res.ok) throw new Error('Failed to fetch')
  return res.json()
}

export default function Home() {
  const { data, isLoading } = useQuery({ queryKey: ['todos'], queryFn: fetchTodos })

  if (isLoading) return <div>Loading...</div>

  return (
    <main className="p-4">
      <h1 className="text-xl font-bold mb-4">Todos</h1>
      <Link href="/new" className="underline text-blue-600">New Todo</Link>
      <ul className="mt-4 space-y-2">
        {data?.map((t: any) => (
          <li key={t.id} className="border p-2 rounded">
            {t.title}
          </li>
        ))}
      </ul>
    </main>
  )
}
