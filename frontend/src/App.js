import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './App.css';

function App() {
  const API_BASE = (() => {
    // Force HTTPS for backend (use localhost hostname so it works in container/hosts)
    const host = window.location.hostname || 'localhost';
    const backendProto = window.location.protocol === 'https:' ? window.location.protocol : 'https:';
    return `${backendProto}//${host}:5000`;
  })();
  const [activeAgent, setActiveAgent] = useState('customer_service');
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [feedback, setFeedback] = useState({ agent: '', text: '', rating: 5 });

  const agents = {
    customer_service: { name: 'Agent Serviciu Clienți', endpoint: '/chat/customer_service' },
    content_creator: { name: 'Agent Creare Conținut', endpoint: '/generate/recipe' },
    sales_analyst: { name: 'Agent Analiză Vânzări', endpoint: '/analyze/sales' },
    marketing: { name: 'Agent Marketing', endpoint: '/create/campaign' },
    inventory_manager: { name: 'Agent Gestionare Stoc', endpoint: '/check/stock' },
    email_marketing: { name: 'Agent Email Marketing', endpoint: '/email/campaign' },
    social_media: { name: 'Agent Social Media', endpoint: '/social/post' },
    review_manager: { name: 'Agent Gestionare Recenzii', endpoint: '/review/respond' },
    order_manager: { name: 'Agent Gestionare Comenzi', endpoint: '/order/process' },
    shipping_manager: { name: 'Agent Transport & Livrări', endpoint: '/shipping/calculate' },
    loyalty_manager: { name: 'Agent Fidelizare Clienți', endpoint: '/loyalty/points' },
    upsell_manager: { name: 'Agent Cross-sell & Upsell', endpoint: '/upsell/suggest' }
  };

  const sendMessage = async () => {
    try {
      const res = await axios.post(`${API_BASE}${agents[activeAgent].endpoint}`, { text: message });
      // Extract the actual response text from the JSON
      const responseData = res.data;
      let formattedResponse = '';
      
      if (responseData.response) {
        formattedResponse = responseData.response;
      } else if (responseData.recipe) {
        formattedResponse = responseData.recipe;
      } else if (responseData.campaign) {
        formattedResponse = responseData.campaign;
      } else if (responseData.analysis) {
        formattedResponse = responseData.analysis;
      } else if (responseData.stock) {
        formattedResponse = responseData.stock;
      } else if (responseData.post) {
        formattedResponse = responseData.post;
      } else if (responseData.newsletter) {
        formattedResponse = responseData.newsletter;
      } else if (responseData.calendar) {
        formattedResponse = responseData.calendar;
      } else if (responseData.result) {
        formattedResponse = responseData.result;
      } else if (responseData.tracking) {
        formattedResponse = responseData.tracking;
      } else if (responseData.shipping) {
        formattedResponse = responseData.shipping;
      } else if (responseData.points) {
        formattedResponse = responseData.points;
      } else if (responseData.program) {
        formattedResponse = responseData.program;
      } else if (responseData.suggestions) {
        formattedResponse = responseData.suggestions;
      } else {
        formattedResponse = JSON.stringify(responseData, null, 2);
      }
      
      setResponse(formattedResponse);
    } catch (error) {
      setResponse('Eroare: ' + error.message);
    }
  };

  const submitFeedback = async () => {
    try {
      await axios.post(`${API_BASE}/feedback`, feedback);
      alert('Feedback trimis cu succes!');
    } catch (error) {
      alert('Eroare la trimiterea feedback-ului');
    }
  };

  const runWorkflow = async () => {
    try {
      const res = await axios.post(`${API_BASE}/workflow/automate_business`);
      setResponse(JSON.stringify(res.data));
    } catch (error) {
      setResponse('Error: ' + error.message);
    }
  };

  return (
    <div className="App">
      <h1>Panou Agenți AI - Redder.ro</h1>
      
      {/* Guide Button */}
      <div className="guide-button-container">
        <button 
          className="guide-button"
          onClick={() => window.open('/guide', '_blank')}
        >
          📚 Ghid de Utilizare Complet
        </button>
      </div>

      <div>
        <h2>Selectează Agentul</h2>
        {Object.keys(agents).map(key => (
          <button key={key} onClick={() => setActiveAgent(key)}>
            {agents[key].name}
          </button>
        ))}
      </div>
      <div>
        <h2>Conversație cu {agents[activeAgent].name}</h2>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Introdu mesajul tău..."
        />
        <button onClick={sendMessage}>Trimite</button>
        {response && (
          <div className="response-container">
            <h3>Răspuns:</h3>
            <div className="formatted-response">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {response}
              </ReactMarkdown>
            </div>
          </div>
        )}
      </div>
      <div>
        <h2>Feedback</h2>
        <select value={feedback.agent} onChange={(e) => setFeedback({...feedback, agent: e.target.value})}>
          <option value="">Selectează Agent</option>
          {Object.keys(agents).map(key => <option key={key} value={key}>{agents[key].name}</option>)}
        </select>
        <textarea
          value={feedback.text}
          onChange={(e) => setFeedback({...feedback, text: e.target.value})}
          placeholder="Scrie feedback-ul tău..."
        />
        <input
          type="number"
          min="1"
          max="5"
          value={feedback.rating}
          onChange={(e) => setFeedback({...feedback, rating: parseInt(e.target.value)})}
        />
        <button onClick={submitFeedback}>Trimite Feedback</button>
      </div>
      <div>
        <h2>Automatizări</h2>
        <button onClick={runWorkflow}>Rulează Automatizare Business</button>
      </div>
    </div>
  );
}

export default App;