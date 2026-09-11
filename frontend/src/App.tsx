import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Nav } from './components/Nav';
import { LandingPage } from './pages/LandingPage';
import { AssessmentPage } from './pages/AssessmentPage';
import { ResultPage } from './pages/ResultPage';
import { PlanPage } from './pages/PlanPage';
import { DashboardPage } from './pages/DashboardPage';
import { CheckInPage } from './pages/CheckInPage';
import { CheckInResultPage } from './pages/CheckInResultPage';

export default function App() {
  return (
    <BrowserRouter>
      <Nav />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/assessment" element={<AssessmentPage />} />
        <Route path="/assessment/result" element={<ResultPage />} />
        <Route path="/plan" element={<PlanPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/checkin" element={<CheckInPage />} />
        <Route path="/checkin/result" element={<CheckInResultPage />} />
      </Routes>
    </BrowserRouter>
  );
}
