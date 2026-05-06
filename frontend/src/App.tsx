import { useState, useEffect } from 'react'
import './App.css'
import { analyzeSkills, matchJob, checkBackendHealth, uploadResume, createJob, analyzeResume } from './lib/api'

function App() {
  const [skills, setSkills] = useState('')
  const [jobTitle, setJobTitle] = useState('')
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState('')
  const [jobRequiredSkills, setJobRequiredSkills] = useState('')
  const [jobSalary, setJobSalary] = useState('')
  
  const [skillsAnalysis, setSkillsAnalysis] = useState<any>(null)
  const [jobMatches, setJobMatches] = useState<any>(null)
  const [resumeData, setResumeData] = useState<any>(null)
  const [jobData, setJobData] = useState<any>(null)
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [backendStatus, setBackendStatus] = useState('Checking...')

  useEffect(() => {
    async function loadHealth() {
      try {
        await checkBackendHealth()
        setBackendStatus('Connected')
      } catch (err) {
        setBackendStatus('Unavailable')
      }
    }

    loadHealth()
  }, [])

  const handleSkillSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      const response = await analyzeSkills(skills)
      setSkillsAnalysis(response)
    } catch (err: any) {
      setError('Failed to analyze skills. Please try again.')
      console.error('Skills analysis error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleJobMatch = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      const response = await matchJob(jobTitle)
      setJobMatches(response)
    } catch (err: any) {
      setError('Failed to find job matches. Please try again.')
      console.error('Job matching error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleResumeUpload = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!resumeFile) {
      setError('Please select a resume file')
      return
    }
    
    setLoading(true)
    setError('')
    
    try {
      const response = await uploadResume(resumeFile)
      setResumeData(response)
      setError('')
    } catch (err: any) {
      setError('Failed to upload resume. Please try again.')
      console.error('Resume upload error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleJobCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      const response = await createJob({
        title: jobTitle,
        description: jobDescription,
        required_skills: jobRequiredSkills.split(',').map(s => s.trim()),
        salary_range: jobSalary
      })
      setJobData(response)
      setError('')
    } catch (err: any) {
      setError('Failed to create job. Please try again.')
      console.error('Job creation error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAnalyzeResume = async () => {
    if (!resumeData || !jobData) {
      setError('Please upload a resume and create a job first')
      return
    }
    
    setLoading(true)
    setError('')
    
    try {
      const response = await analyzeResume(resumeData.resume_id, jobData.job_id)
      setAnalysisResult(response)
    } catch (err: any) {
      setError('Failed to analyze resume. Please try again.')
      console.error('Resume analysis error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <header className="header">
        <h1>SkillBridge AI</h1>
        <p>Bridge Your Skills to Your Dream Career</p>
        <div className="backend-status">Backend: {backendStatus}</div>
      </header>

      <section id="hero">
        <div className="hero-content">
          <h2>Discover Your Career Path</h2>
          <p>Use AI-powered insights to match your skills with the perfect job opportunities and learning paths.</p>
        </div>
      </section>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      <section id="resume-upload">
        <h2>Resume Upload</h2>
        <form onSubmit={handleResumeUpload}>
          <input
            type="file"
            accept=".pdf,.doc,.docx,.txt"
            onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
            required
          />
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Uploading...' : 'Upload Resume'}
          </button>
        </form>
        
        {resumeData && (
          <div className="results">
            <h3>Resume Uploaded</h3>
            <p><strong>File:</strong> {resumeData.filename}</p>
            <p><strong>Resume ID:</strong> {resumeData.resume_id}</p>
            <p>{resumeData.message}</p>
          </div>
        )}
      </section>

      <section id="job-creation">
        <h2>Create Job Posting</h2>
        <form onSubmit={handleJobCreate}>
          <input
            type="text"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            placeholder="Job Title"
            required
          />
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Job Description"
            rows={4}
            required
          />
          <input
            type="text"
            value={jobRequiredSkills}
            onChange={(e) => setJobRequiredSkills(e.target.value)}
            placeholder="Required Skills (comma-separated)"
          />
          <input
            type="text"
            value={jobSalary}
            onChange={(e) => setJobSalary(e.target.value)}
            placeholder="Salary Range (e.g., $100k - $130k)"
          />
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Creating...' : 'Create Job'}
          </button>
        </form>
        
        {jobData && (
          <div className="results">
            <h3>Job Created</h3>
            <p><strong>Job Title:</strong> {jobData.title}</p>
            <p><strong>Job ID:</strong> {jobData.job_id}</p>
            <p>{jobData.message}</p>
          </div>
        )}
      </section>

      {resumeData && jobData && (
        <section id="resume-analysis">
          <h2>Resume Analysis</h2>
          <button onClick={handleAnalyzeResume} className="btn-primary" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Resume vs Job'}
          </button>
          
          {analysisResult && (
            <div className="results">
              <h3>Analysis Results for "{analysisResult.job_title}"</h3>
              <div className="match-score">
                <p><strong>Match Score:</strong> <span className="score-badge">{analysisResult.match_score}%</span></p>
              </div>
              <h4>Feedback:</h4>
              <ul>
                {analysisResult.feedback?.map((item: string, index: number) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
              {analysisResult.required_skills_missing?.length > 0 && (
                <>
                  <h4>Missing Skills:</h4>
                  <p>{analysisResult.required_skills_missing.join(', ')}</p>
                </>
              )}
            </div>
          )}
        </section>
      )}

      <section id="skills-assessment">
        <h2>Skills Assessment</h2>
        <form onSubmit={handleSkillSubmit}>
          <textarea
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            placeholder="Enter your skills (e.g., Python, React, Machine Learning...)"
            rows={4}
            required
          />
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze Skills'}
          </button>
        </form>
        
        {skillsAnalysis && (
          <div className="results">
            <h3>Analysis Results</h3>
            <p><strong>Skills Identified:</strong> {skillsAnalysis.skills.join(', ')}</p>
            <p><strong>Total Skills:</strong> {skillsAnalysis.analysis.total_skills}</p>
            <p><strong>Strengths:</strong> {skillsAnalysis.analysis.strengths.join(', ')}</p>
            <p><strong>Skill Gaps:</strong> {skillsAnalysis.analysis.gaps.join(', ')}</p>
          </div>
        )}
      </section>

      <section id="job-matching">
        <h2>Job Matching</h2>
        <form onSubmit={handleJobMatch}>
          <input
            type="text"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            placeholder="Enter desired job title"
            required
          />
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Finding Matches...' : 'Find Matches'}
          </button>
        </form>
        
        {jobMatches && (
          <div className="results">
            <h3>Job Matches for "{jobMatches.job_title}"</h3>
            {jobMatches.matches.map((match: any, index: number) => (
              <div key={index} className="job-match">
                <h4>{match.title} at {match.company}</h4>
                <div className="match-score">
                  <p><strong>Match Score:</strong> <span className="score-badge">{match.match_score}%</span></p>
                </div>
                <p><strong>Required Skills:</strong> {match.required_skills.join(', ')}</p>
                <p><strong>Salary Range:</strong> {match.salary_range}</p>
              </div>
            ))}
            <h4>Recommendations:</h4>
            <ul>
              {jobMatches.recommendations.map((rec: string, index: number) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}
      </section>

      <section id="learning-paths">
        <h2>Recommended Learning Paths</h2>
        <div className="learning-cards">
          <div className="card">
            <h3>Full Stack Development</h3>
            <p>Learn frontend and backend technologies to build complete web applications.</p>
          </div>
          <div className="card">
            <h3>Data Science</h3>
            <p>Master data analysis, machine learning, and visualization techniques.</p>
          </div>
          <div className="card">
            <h3>AI/ML Engineering</h3>
            <p>Dive into artificial intelligence and machine learning development.</p>
          </div>
        </div>
      </section>

      <footer className="footer">
        <p>&copy; 2026 SkillBridge AI. Powered by FastAPI and React.</p>
      </footer>
    </>
  )
}

export default App

