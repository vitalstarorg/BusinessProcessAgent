'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { JsonViewer } from '@/components/JsonViewer'
import { fetchCompanyResearch } from '@/lib/api'
import { ResearchResult } from '@/lib/types'

export default function Home() {
  const [company, setCompany] = useState('')
  const [result, setResult] = useState<ResearchResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    if (!company.trim()) {
      setError('Please enter a company name')
      setLoading(false)
      return
    }
    
    try {
      const data = await fetchCompanyResearch(company)
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">Company Research</h1>
      <form onSubmit={handleSubmit} className="space-y-4 mb-8">
        <div className="flex gap-4">
          <Input
            type="text"
            placeholder="Enter company name"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="flex-1"
            disabled={loading}
          />
          <Button type="submit" disabled={loading}>
            {loading ? 'Researching...' : 'Research'}
          </Button>
        </div>
      </form>
      
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
          {error}
        </div>
      )}
      
      {result && (
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <h2 className="text-xl font-semibold mb-4">Research Results for {result.Company}</h2>
          <div className="overflow-auto max-h-[600px]">
            <JsonViewer data={result} />
          </div>
        </div>
      )}
    </main>
  )
}
