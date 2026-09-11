import { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { Menu, X, Activity, ShieldCheck, Users, Compass, FileText, Sparkles } from 'lucide-react';

export function Nav() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const closeMenu = () => setMobileMenuOpen(false);

  return (
    <nav className="nav">
      <div className="nav__inner">
        {/* Logo */}
        <Link to="/" className="nav__logo" onClick={closeMenu}>
          <div className="nav__logo-mark">🌿</div>
          <div>
            <span style={{ fontFamily: 'var(--font-serif)', fontWeight: 700, fontSize: '1.25rem', letterSpacing: '-0.01em' }}>
              AyuPulse
            </span>
            <span style={{ display: 'block', fontSize: '0.65rem', color: 'var(--color-brand)', fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase', marginTop: -2 }}>
              AYUSH · Preventive AI
            </span>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <div className="nav__links desktop-only">
          <NavLink to="/" className={({ isActive }) => `nav__link ${isActive ? 'active' : ''}`} end>
            Home
          </NavLink>
          <NavLink to="/assessment" className={({ isActive }) => `nav__link ${isActive ? 'active' : ''}`}>
            Assessment
          </NavLink>

          {/* Prominent My Daily Pulse */}
          <NavLink
            to="/tracker"
            className={({ isActive }) => `nav__pulse-pill ${isActive ? 'nav__pulse-pill--active' : ''}`}
          >
            <Activity size={16} className="pulse-icon" />
            <span>My Daily Pulse</span>
          </NavLink>

          <NavLink to="/plan" className={({ isActive }) => `nav__link ${isActive ? 'active' : ''}`}>
            Plan
          </NavLink>
          <NavLink to="/connect" className={({ isActive }) => `nav__link ${isActive ? 'active' : ''}`}>
            Connect
          </NavLink>
          <NavLink to="/safety" className={({ isActive }) => `nav__link ${isActive ? 'active' : ''}`}>
            Safety
          </NavLink>
          <NavLink to="/community" className={({ isActive }) => `nav__link ${isActive ? 'active' : ''}`}>
            Community
          </NavLink>
        </div>

        {/* Mobile menu button */}
        <button
          className="mobile-menu-btn mobile-only"
          onClick={() => setMobileMenuOpen(prev => !prev)}
          aria-label={mobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Drawer Navigation */}
      {mobileMenuOpen && (
        <div className="mobile-drawer fade-in">
          <div className="mobile-drawer__inner">
            <NavLink
              to="/tracker"
              className="mobile-nav__pulse-cta"
              onClick={closeMenu}
            >
              <Activity size={18} />
              <span>Open My Daily Pulse</span>
            </NavLink>

            <div className="mobile-nav__links">
              <NavLink to="/" className="mobile-nav__link" onClick={closeMenu} end>
                <Sparkles size={18} />
                <span>Home Command Center</span>
              </NavLink>
              <NavLink to="/assessment" className="mobile-nav__link" onClick={closeMenu}>
                <Compass size={18} />
                <span>Prakriti Assessment</span>
              </NavLink>
              <NavLink to="/plan" className="mobile-nav__link" onClick={closeMenu}>
                <FileText size={18} />
                <span>Personalized Plan & Tasks</span>
              </NavLink>
              <NavLink to="/connect" className="mobile-nav__link" onClick={closeMenu}>
                <Compass size={18} />
                <span>AYUSH Connect & Centres</span>
              </NavLink>
              <NavLink to="/safety" className="mobile-nav__link" onClick={closeMenu}>
                <ShieldCheck size={18} />
                <span>Safety Gate & Guardrails</span>
              </NavLink>
              <NavLink to="/community" className="mobile-nav__link" onClick={closeMenu}>
                <Users size={18} />
                <span>Community Wellness Dashboard</span>
              </NavLink>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
