'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { JsonViewer } from '@/components/JsonViewer'
import { fetchCompanyResearch } from '@/lib/api'
import { ResearchResult, ResearchResults } from '@/lib/types'

export default function Home() {
  const [company, setCompany] = useState('')
  const [companyLoc, setCompanyLoc] = useState('')
  const [results, setResults] = useState<ResearchResults>({ result1: null, result2: null })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    if (!company.trim()) {
      setError('Please enter company name')
      setLoading(false)
      return
    }
    
    try {
      const data = await fetchCompanyResearch(company, companyLoc)
      setResults(data)
      setCompany('')
      setCompanyLoc('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container mx-auto p-4 max-w-6xl">
      <h1 className="text-3xl font-bold mb-6">Company Research</h1>
      <form onSubmit={handleSubmit} className="space-y-4 mb-8">
        <div className="flex gap-4">
          <Input
            id="Company"
            type="text"
            placeholder="Company Name"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="flex-1"
            disabled={loading}
          />
          <Input
            id="CompanyLoc"
            type="text"
            placeholder="Company Location"
            value={companyLoc}
            onChange={(e) => setCompanyLoc(e.target.value)}
            className="flex-1"
            disabled={loading}
          />
          <Button id="Research" type="submit" disabled={loading}>
            {loading ? 'Researching...' : 'Research'}
          </Button>
        </div>
      </form>
      
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-6">
          {error}
        </div>
      )}
      
      <div className="space-y-6">
        {results.result1 && (
          <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
            <h2 className="text-xl font-semibold mb-4">Research Results 1 for {results.result1.Company}</h2>
            <div className="overflow-auto max-h-[400px]">
              <JsonViewer data={results.result1} />
            </div>
          </div>
        )}
        
        {results.result2 && (
          <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
            <h2 className="text-xl font-semibold mb-4">Research Results 2 for {results.result2.Company}</h2>
            <div className="overflow-auto max-h-[400px]">
              <JsonViewer data={results.result2} />
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
