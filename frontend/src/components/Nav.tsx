import { NavLink } from 'react-router-dom';

export function Nav() {
  return (
    <nav className="nav">
      <div className="nav__inner">
        <NavLink to="/" className="nav__logo">
          <div className="nav__logo-mark">🌿</div>
          <span style={{ fontFamily: 'var(--font-serif)', fontWeight: 700, fontSize: '1.1rem' }}>
            AyuPulse
          </span>
        </NavLink>
        <div className="nav__links">
          <NavLink to="/assessment" className={({ isActive }) => `nav__link ${isActive ? 'active' : ''}`}>
            Assess
          </NavLink>
          <NavLink to="/plan" className={({ isActive }) => `nav__link ${isActive ? 'active' : ''}`}>
            My Plan
          </NavLink>
          <NavLink to="/dashboard" className={({ isActive }) => `nav__link ${isActive ? 'active' : ''}`}>
            Dashboard
          </NavLink>
          <NavLink to="/checkin" className={({ isActive }) => `nav__link ${isActive ? 'active' : ''}`}>
            Check-in
          </NavLink>
        </div>
      </div>
    </nav>
  );
}
