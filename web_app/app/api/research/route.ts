import { NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'
import { ResearchResult } from '@/lib/types'

interface RequestBody {
  company: string
  companyLoc: string
  type?: number
}

export async function POST(request: Request) {
  try {
    const body = await request.json() as RequestBody
    const { company, companyLoc, type = 1 } = body

    if (!company?.trim()) {
      return NextResponse.json<ResearchResult>(
        { error: 'Company name is required', Company: '' },
        { status: 400 }
      )
    }

    const data = await runPythonScript(company, companyLoc, type)
    return NextResponse.json<ResearchResult>(data)
  } catch (error) {
    console.error('API error:', error)
    return NextResponse.json<ResearchResult>(
      { error: 'Internal server error', Company: '' },
      { status: 500 }
    )
  }
}

async function runPythonScript(company: string, companyLoc: string, type: number): Promise<ResearchResult> {
  return new Promise((resolve, reject) => {
    const pythonScript = path.join(process.cwd(), 'research_company.py')
    const pythonProcess = spawn('python3', [pythonScript, company, companyLoc, type.toString()])

    let result = ''
    let error = ''

    pythonProcess.stdout.on('data', (data) => {
      result += data.toString()
    })

    pythonProcess.stderr.on('data', (data) => {
      error += data.toString()
    })

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        resolve({ 
          error: `Python script failed: ${error}`,
          Company: company 
        })
        return
      }

      try {
        const jsonResult = JSON.parse(result) as ResearchResult
        resolve(jsonResult)
      } catch (e) {
        resolve({ 
          error: 'Failed to parse Python script output as JSON',
          Company: company 
        })
      }
    })
  })
}
