'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function NewTodo() {
  const [title, setTitle] = useState('')
  const router = useRouter()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/todos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
    })
    router.push('/')
  }

  return (
    <main className="p-4">
      <h1 className="text-xl font-bold mb-4">New Todo</h1>
      <form onSubmit={handleSubmit} className="space-y-2">
        <input
          className="border p-2 rounded w-full"
          placeholder="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
          Save
        </button>
      </form>
    </main>
  )
}
