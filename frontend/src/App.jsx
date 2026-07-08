import { Navigate, Route, Routes } from 'react-router-dom'
import DashboardLayout from './layouts/DashboardLayout'
import ProtectedRoute from './components/ProtectedRoute'
import AuthPage from './pages/AuthPage'
import DashboardPage from './pages/DashboardPage'
import ResumeAnalyzerPage from './pages/ResumeAnalyzerPage'
import AtsCheckerPage from './pages/AtsCheckerPage'
import CoverLetterPage from './pages/CoverLetterPage'
import InterviewCoachPage from './pages/InterviewCoachPage'
import LinkedInPostPage from './pages/LinkedInPostPage'
import JobTrackerPage from './pages/JobTrackerPage'
import SkillGapPage from './pages/SkillGapPage'
import NotFoundPage from './pages/NotFoundPage'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<AuthPage mode="login" />} />
      <Route path="/signup" element={<AuthPage mode="signup" />} />
      <Route path="/" element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
        <Route index element={<DashboardPage />} />
        <Route path="resume-analyzer" element={<ResumeAnalyzerPage />} />
        <Route path="ats-checker" element={<AtsCheckerPage />} />
        <Route path="cover-letter" element={<CoverLetterPage />} />
        <Route path="interview-coach" element={<InterviewCoachPage />} />
        <Route path="linkedin-post" element={<LinkedInPostPage />} />
        <Route path="job-tracker" element={<JobTrackerPage />} />
        <Route path="skill-gap" element={<SkillGapPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
      <Route path="/404" element={<NotFoundPage />} />
    </Routes>
  )
}
