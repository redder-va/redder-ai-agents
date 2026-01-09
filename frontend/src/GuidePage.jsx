import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './GuidePage.css';

function GuidePage() {
  const [activeSection, setActiveSection] = useState('');

  // Table of Contents structure
  const tableOfContents = [
    {
      id: 'introducere',
      title: '🎯 Introducere',
      subsections: [
        { id: 'acces', title: 'Cum să Accesezi Aplicația' }
      ]
    },
    {
      id: 'customer-experience',
      title: '👥 Agenți Customer Experience',
      subsections: [
        { id: 'serviciu-clienti', title: '1. Agent Serviciu Clienți' },
        { id: 'recenzii', title: '2. Agent Gestionare Recenzii' },
        { id: 'fidelizare', title: '3. Agent Fidelizare Clienți' },
        { id: 'upsell', title: '4. Agent Cross-sell & Upsell' }
      ]
    },
    {
      id: 'continut-marketing',
      title: '📝 Agenți Conținut & Marketing',
      subsections: [
        { id: 'creare-continut', title: '5. Agent Creare Conținut' },
        { id: 'marketing', title: '6. Agent Marketing' },
        { id: 'email-marketing', title: '7. Agent Email Marketing' },
        { id: 'social-media', title: '8. Agent Social Media' }
      ]
    },
    {
      id: 'operatiuni',
      title: '📦 Agenți Operațiuni & Logistică',
      subsections: [
        { id: 'comenzi', title: '9. Agent Gestionare Comenzi' },
        { id: 'transport', title: '10. Agent Transport & Livrări' },
        { id: 'vanzari', title: '11. Agent Analiză Vânzări' },
        { id: 'stoc', title: '12. Agent Gestionare Stoc' }
      ]
    },
    {
      id: 'workflows',
      title: '🔄 Workflow-uri Complete',
      subsections: []
    },
    {
      id: 'scenarii',
      title: '🎓 Training Practic: Scenarii Reale',
      subsections: []
    },
    {
      id: 'faq',
      title: '❓ Întrebări Frecvente',
      subsections: []
    }
  ];

  // Scroll to section handler
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setActiveSection(sectionId);
    }
  };

  // Track active section on scroll
  useEffect(() => {
    const handleScroll = () => {
      const sections = document.querySelectorAll('.guide-section');
      let current = '';

      sections.forEach((section) => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= sectionTop - 100) {
          current = section.getAttribute('id');
        }
      });

      setActiveSection(current);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="guide-page">
      {/* Header */}
      <header className="guide-header">
        <div className="guide-header-content">
          <h1>📚 Ghid Complet de Utilizare</h1>
          <p>Agenți AI Redder.ro - Documentație Detaliată</p>
        </div>
      </header>

      <div className="guide-container">
        {/* Sidebar Table of Contents */}
        <aside className="guide-toc">
          <div className="toc-sticky">
            <h2>📑 Cuprins</h2>
            <nav>
              {tableOfContents.map((section) => (
                <div key={section.id} className="toc-section">
                  <button
                    className={`toc-link ${activeSection === section.id ? 'active' : ''}`}
                    onClick={() => scrollToSection(section.id)}
                  >
                    {section.title}
                  </button>
                  {section.subsections.length > 0 && (
                    <div className="toc-subsections">
                      {section.subsections.map((subsection) => (
                        <button
                          key={subsection.id}
                          className={`toc-sublink ${activeSection === subsection.id ? 'active' : ''}`}
                          onClick={() => scrollToSection(subsection.id)}
                        >
                          {subsection.title}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </nav>
          </div>
        </aside>

        {/* Main Content */}
        <main className="guide-content">
          
          {/* Introducere */}
          <section id="introducere" className="guide-section">
            <h2>🎯 Introducere</h2>
            <div className="guide-intro">
              <p>
                Sistemul de agenți AI Redder.ro este o platformă completă de automatizare business 
                pentru magazinul online de cocktail-uri și accesorii de bar. Sistemul include{' '}
                <strong>12 agenți specializați</strong> care lucrează 24/7 pentru a optimiza 
                operațiunile, crește vânzările și îmbunătăți experiența clienților.
              </p>
              
              <div className="screenshot-real">
                <img 
                  src="/images/homepage-principal.png" 
                  alt="Dashboard Principal Redder.ro - 12 Agenți AI"
                  className="guide-screenshot"
                  onClick={() => window.open('/images/homepage-principal.png', '_blank')}
                  title="Click pentru a vedea în mărime completă"
                />
                <p className="screenshot-caption">Dashboard Principal cu 12 Agenți AI (Click pentru zoom)</p>
              </div>
            </div>

            <div id="acces" className="subsection">
              <h3>🚀 Cum să Accesezi Aplicația</h3>
              
              <div className="step-box">
                <h4>Pas 1: Pornește Backend-ul</h4>
                <pre><code>{`# Deschide terminal în folderul proiectului
cd "F:\\REDDER.RO\\Agenti AI"

# Activează mediul virtual
.\\venv311\\Scripts\\activate

# Pornește serverul
python main.py`}</code></pre>
                <p className="success-message">✅ Verificare: Vei vedea mesajul "[HTTPS] Starting with HTTPS on https://127.0.0.1:5000"</p>
              </div>

              <div className="step-box">
                <h4>Pas 2: Pornește Frontend-ul</h4>
                <pre><code>{`# În alt terminal sau dublu-click pe
run_frontend.bat`}</code></pre>
                <p className="success-message">✅ Verificare: Browser-ul se va deschide automat la https://localhost:3000</p>
              </div>

              <div className="screenshot-placeholder">
                <div className="screenshot-box">
                  <span className="screenshot-icon">🖼️</span>
                  <p>Screenshot: Terminale cu Backend și Frontend pornite</p>
                </div>
              </div>
            </div>
          </section>

          {/* Customer Experience */}
          <section id="customer-experience" className="guide-section">
            <h2>👥 PARTEA 1: Agenți Customer Experience</h2>

            {/* Agent Serviciu Clienți */}
            <div id="serviciu-clienti" className="subsection agent-section">
              <h3>1️⃣ Agent Serviciu Clienți</h3>
              
              <div className="agent-description">
                <h4>🎯 Scopul Agentului</h4>
                <p>
                  Răspunde automat la întrebările clienților 24/7, oferă suport tehnic și învață 
                  din fiecare interacțiune pentru a îmbunătăți calitatea răspunsurilor.
                </p>
              </div>

              <div className="screenshot-placeholder">
                <div className="screenshot-box">
                  <span className="screenshot-icon">🖼️</span>
                  <p>Screenshot: Agent Serviciu Clienți în acțiune</p>
                </div>
              </div>

              <div className="example-box">
                <h4>📖 Exemplul 1: Întrebare despre Produs</h4>
                <div className="example-input">
                  <strong>Întrebare:</strong> "Ce diferență este între Vodca Kumaniok Original și Vodca Valahia Gold?"
                </div>
                <div className="example-output">
                  <strong>Răspuns AI:</strong>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{`
Bună! Iată diferențele principale:

## Vodca Kumaniok Original 38%
- **Origine:** Producție tradițională rusească
- **Tărie:** 38% alcool
- **Gust:** Curat, echilibrat, note clasice
- **Preț:** 24 RON (verifică disponibilitate)
- **Perfect pentru:** Cocktail-uri tradiționale, shots

## Vodca Valahia Gold 40%
- **Origine:** Producție premium românească
- **Tărie:** 40% alcool
- **Gust:** Rafinat, moale, calitate superioară
- **Preț:** 24 RON (în stoc)
- **Perfect pentru:** Ocazii speciale, degustare pură

### Recomandarea Mea
Pentru cocktail-uri clasice → **Kumaniok Original**
Pentru calitate premium românească → **Valahia Gold**

Pot să-ți recomand o rețetă pentru oricare dintre ele! 🍸
                  `}</ReactMarkdown>
                </div>
              </div>

              <div className="tips-box">
                <h4>💡 Tips & Tricks</h4>
                <ul>
                  <li><strong>Fii specific:</strong> Cu cât întrebarea e mai detaliată, cu atât răspunsul e mai bun</li>
                  <li><strong>Context:</strong> Menționează preferințe, buget, ocazie</li>
                  <li><strong>Follow-up:</strong> Poți pune întrebări suplimentare în aceeași conversație</li>
                  <li><strong>Învață:</strong> Agentul își amintește interacțiunile anterioare</li>
                </ul>
              </div>
            </div>

            {/* Agent Recenzii */}
            <div id="recenzii" className="subsection agent-section">
              <h3>2️⃣ Agent Gestionare Recenzii</h3>
              
              <div className="agent-description">
                <h4>🎯 Scopul Agentului</h4>
                <p>
                  Răspunde profesionist la recenziile clienților (pozitive și negative), analizează 
                  sentimentul clienților și transformă feedback-ul în oportunități de îmbunătățire.
                </p>
              </div>

              <div className="example-box">
                <h4>📖 Exemplul 1: Recenzie Pozitivă</h4>
                <div className="example-input">
                  <strong>Input:</strong> "Super produse, livrare rapidă! Mojito-ul a ieșit perfect. Recomand!"
                </div>
                <div className="example-output">
                  <strong>Răspuns AI:</strong>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{`
## Răspuns la Recenzie

### Analiza Recenziei
**Sentiment:** ⭐⭐⭐⭐⭐ Foarte Pozitiv
**Categorie:** Produs + Livrare

### Răspunsul Recomandat
"Mulțumim din suflet pentru recenzie! 🎉

Ne bucurăm enorm că Mojito-ul a ieșit perfect și că livrarea a fost promptă!

Îți mulțumim pentru încredere!
Echipa Redder.ro 🌟"
                  `}</ReactMarkdown>
                </div>
              </div>

              <div className="screenshot-placeholder">
                <div className="screenshot-box">
                  <span className="screenshot-icon">🖼️</span>
                  <p>Screenshot: Analiză sentiment recenzii cu grafice</p>
                </div>
              </div>
            </div>

            {/* Agent Fidelizare */}
            <div id="fidelizare" className="subsection agent-section">
              <h3>3️⃣ Agent Fidelizare Clienți</h3>
              
              <div className="agent-description">
                <h4>🎯 Scopul Agentului</h4>
                <p>
                  Gestionează programul de loialitate, calculează puncte, creează programe VIP 
                  și transformă clienții ocazionali în ambasadori ai brandului.
                </p>
              </div>

              <div className="vip-levels">
                <h4>👑 Niveluri Program VIP</h4>
                <div className="vip-grid">
                  <div className="vip-card bronze">
                    <h5>🥉 Bronze</h5>
                    <p>5% discount</p>
                    <p>1 punct / 10 RON</p>
                  </div>
                  <div className="vip-card silver">
                    <h5>🥈 Silver</h5>
                    <p>10% discount</p>
                    <p>2 puncte / 10 RON</p>
                  </div>
                  <div className="vip-card gold">
                    <h5>🥇 Gold</h5>
                    <p>15% discount</p>
                    <p>3 puncte / 10 RON</p>
                  </div>
                  <div className="vip-card platinum">
                    <h5>💎 Platinum</h5>
                    <p>20% discount</p>
                    <p>5 puncte / 10 RON</p>
                  </div>
                </div>
              </div>

              <div className="screenshot-placeholder">
                <div className="screenshot-box">
                  <span className="screenshot-icon">🖼️</span>
                  <p>Screenshot: Dashboard puncte loialitate client</p>
                </div>
              </div>
            </div>

            {/* Agent Upsell */}
            <div id="upsell" className="subsection agent-section">
              <h3>4️⃣ Agent Cross-sell & Upsell</h3>
              
              <div className="agent-description">
                <h4>🎯 Scopul Agentului</h4>
                <p>
                  Generează recomandări inteligente pentru creșterea valorii coșului prin 
                  sugestii de upgrade și produse complementare.
                </p>
              </div>
            </div>
          </section>

          {/* Conținut & Marketing */}
          <section id="continut-marketing" className="guide-section">
            <h2>📝 PARTEA 2: Agenți Conținut & Marketing</h2>

            <div id="creare-continut" className="subsection agent-section">
              <h3>5️⃣ Agent Creare Conținut</h3>
              
              <div className="agent-description">
                <h4>🎯 Scopul Agentului</h4>
                <p>
                  Generează rețete de cocktail-uri creative, descrieri captivante de produse 
                  și conținut pentru blog/social media.
                </p>
              </div>

              <div className="example-box">
                <h4>📖 Exemplul: Rețetă Cocktail Completă</h4>
                <div className="example-input">
                  <strong>Input:</strong> "Vodca Pshenoff Clasic, suc de lămâie, zmeură, mentă"
                </div>
                <div className="example-output">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{`
## 🍹 Raspberry Mint Pshenoff Cooler

### Ingrediente
- 50ml Vodca Pshenoff Clasic 40%
- 30ml suc proaspăt de lămâie
- 8-10 zmeură proaspete
- 6-8 frunze mentă
- Gheață cuburi

### Mod de Preparare
1. **Muddle** zmeură și mentă în shaker
2. **Adaugă** vodca Pshenoff și suc de lămâie
3. **Shake** puternic 10-15 secunde
4. **Servește** într-un pahar highball cu gheață

**Dificultate:** 🔵🔵⚪⚪⚪ Ușor
**Timp:** 5 minute
                  `}</ReactMarkdown>
                </div>
              </div>

              <div className="screenshot-placeholder">
                <div className="screenshot-box">
                  <span className="screenshot-icon">🖼️</span>
                  <p>Screenshot: Rețetă generată cu imagine cocktail</p>
                </div>
              </div>
            </div>

            <div id="marketing" className="subsection agent-section">
              <h3>6️⃣ Agent Marketing</h3>
              <p>Creează campanii personalizate și strategii de marketing.</p>
            </div>

            <div id="email-marketing" className="subsection agent-section">
              <h3>7️⃣ Agent Email Marketing</h3>
              <p>Generează campanii email și newsletter-e automate.</p>
            </div>

            <div id="social-media" className="subsection agent-section">
              <h3>8️⃣ Agent Social Media</h3>
              <p>Creează postări pentru Instagram, Facebook și TikTok.</p>
            </div>
          </section>

          {/* Operațiuni */}
          <section id="operatiuni" className="guide-section">
            <h2>📦 PARTEA 3: Agenți Operațiuni & Logistică</h2>

            <div id="comenzi" className="subsection agent-section">
              <h3>9️⃣ Agent Gestionare Comenzi</h3>
              <p>Procesare automată comenzi, tracking și detectare probleme.</p>
              
              <div className="screenshot-placeholder">
                <div className="screenshot-box">
                  <span className="screenshot-icon">🖼️</span>
                  <p>Screenshot: Timeline procesare comandă</p>
                </div>
              </div>
            </div>

            <div id="transport" className="subsection agent-section">
              <h3>🔟 Agent Transport & Livrări</h3>
              <p>Calcul costuri transport, optimizare rute, tracking AWB.</p>
            </div>

            <div id="vanzari" className="subsection agent-section">
              <h3>1️⃣1️⃣ Agent Analiză Vânzări</h3>
              <p>Rapoarte detaliate, predicții și insights business.</p>
              
              <div className="screenshot-placeholder">
                <div className="screenshot-box">
                  <span className="screenshot-icon">🖼️</span>
                  <p>Screenshot: Dashboard analiză vânzări cu grafice</p>
                </div>
              </div>
            </div>

            <div id="stoc" className="subsection agent-section">
              <h3>1️⃣2️⃣ Agent Gestionare Stoc</h3>
              <p>Monitoring stoc, alerte și sugestii comenzi furnizori.</p>
            </div>
          </section>

          {/* Workflows */}
          <section id="workflows" className="guide-section">
            <h2>🔄 Workflow-uri Complete</h2>
            
            <div className="workflow-box">
              <h3>Workflow 1: De la Comandă la Livrare</h3>
              <div className="workflow-steps">
                <div className="workflow-step">1. Client plasează comandă</div>
                <div className="workflow-arrow">↓</div>
                <div className="workflow-step">2. Agent Comenzi → Procesează</div>
                <div className="workflow-arrow">↓</div>
                <div className="workflow-step">3. Agent Stoc → Verifică</div>
                <div className="workflow-arrow">↓</div>
                <div className="workflow-step">4. Agent Transport → Calculează curier</div>
                <div className="workflow-arrow">↓</div>
                <div className="workflow-step">5. Agent Email → Confirmare</div>
                <div className="workflow-arrow">↓</div>
                <div className="workflow-step">6. Agent Fidelizare → Acordă puncte</div>
              </div>
            </div>

            <div className="screenshot-placeholder">
              <div className="screenshot-box">
                <span className="screenshot-icon">🖼️</span>
                <p>Screenshot: Workflow vizual cu toți agenții conectați</p>
              </div>
            </div>
          </section>

          {/* Scenarii */}
          <section id="scenarii" className="guide-section">
            <h2>🎓 Training Practic: Scenarii Reale</h2>
            
            <div className="scenario-box">
              <h3>Scenariul 1: Organizare Eveniment</h3>
              <p><strong>Situație:</strong> Client vrea să organizeze o nuntă pentru 100 persoane</p>
              
              <div className="scenario-agents">
                <h4>Agenți folosiți:</h4>
                <ol>
                  <li>Agent Serviciu Clienți - Colectare cerințe</li>
                  <li>Agent Creare Conținut - 5 rețete cocktail-uri</li>
                  <li>Agent Gestionare Stoc - Verificare disponibilitate</li>
                  <li>Agent Cross-sell - Sugestii accesorii</li>
                  <li>Agent Transport - Optimizare livrare</li>
                  <li>Agent Fidelizare - Puncte bonus + discount</li>
                </ol>
                <p className="scenario-result">✅ <strong>Rezultat:</strong> Ofertă completă în &lt;30 minute</p>
              </div>
            </div>

            <div className="scenario-box">
              <h3>Scenariul 2: Creștere Vânzări Produse Slow-moving</h3>
              <p><strong>Situație:</strong> 30 sticle ORO del Sole Muscat stagnează în stoc</p>
              
              <div className="scenario-agents">
                <h4>Soluție multi-agent:</h4>
                <ol>
                  <li>Agent Analiză Vânzări - Identificare cauză</li>
                  <li>Agent Creare Conținut - 3 rețete cocktail cu vin spumant</li>
                  <li>Agent Marketing - Campanie "Summer Sparkle"</li>
                  <li>Agent Email Marketing - Newsletter țintit</li>
                  <li>Agent Social Media - 7 postări Instagram</li>
                  <li>Agent Cross-sell - Bundle-uri cu Muscat</li>
                </ol>
                <p className="scenario-result">✅ <strong>Rezultat:</strong> Vânzări +180% în 2 săptămâni</p>
              </div>
            </div>
          </section>

          {/* FAQ */}
          <section id="faq" className="guide-section">
            <h2>❓ Întrebări Frecvente</h2>
            
            <div className="faq-item">
              <h3>Q: Pot folosi mai mulți agenți simultan?</h3>
              <p><strong>A:</strong> Da! Agenții sunt proiectați să lucreze împreună. De exemplu, 
              poți cere Agent Serviciu Clienți să te ajute, iar el va consulta automat Agent 
              Gestionare Stoc pentru disponibilitate.</p>
            </div>

            <div className="faq-item">
              <h3>Q: Agenții învață din interacțiunile mele?</h3>
              <p><strong>A:</strong> Da! Fiecare agent folosește tehnologie de învățare. Cu cât îl 
              folosești mai mult, cu atât răspunsurile devin mai personalizate.</p>
            </div>

            <div className="faq-item">
              <h3>Q: Cât durează să primesc un răspuns?</h3>
              <p><strong>A:</strong> Majoritatea răspunsurilor vin în 2-5 secunde. Analize complexe 
              pot dura 10-15 secunde.</p>
            </div>

            <div className="faq-item">
              <h3>Q: Pot exporta rapoartele generate?</h3>
              <p><strong>A:</strong> Da! Poți copia textul (Markdown formatat) și îl poți 
              salva/împărtăși.</p>
            </div>
          </section>

          {/* Footer */}
          <footer className="guide-footer">
            <div className="footer-content">
              <h3>📞 Suport & Contact</h3>
              <div className="contact-grid">
                <div className="contact-item">
                  <h4>Pentru Probleme Tehnice</h4>
                  <p>Email: support@redder.ro</p>
                  <p>Telefon: 0721 XXX XXX</p>
                </div>
                <div className="contact-item">
                  <h4>Pentru Feedback despre Agenți</h4>
                  <p>Email: ai-feedback@redder.ro</p>
                  <p>Folosește butonul "Trimite Feedback" din aplicație</p>
                </div>
              </div>
              
              <div className="footer-meta">
                <p><strong>Versiune ghid:</strong> 1.0 | <strong>Data:</strong> Ianuarie 2026</p>
                <p>Actualizat pentru: 12 Agenți AI Redder.ro</p>
              </div>
            </div>
          </footer>

        </main>
      </div>
    </div>
  );
}

export default GuidePage;
