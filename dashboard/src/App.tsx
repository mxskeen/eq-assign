import { useState, useEffect } from 'react';
import type { Trace, Step, Evaluation } from './types/trace';
import traceData from '../../traces/competitor_selection.json';
import './index.css';

function formatStepName(name: string): string {
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

function formatDateTime(isoString: string | null): string {
  if (!isoString) return 'N/A';
  const date = new Date(isoString);
  return date.toLocaleString();
}

function CandidateCard({ evaluation }: { evaluation: Evaluation }) {
  const { candidate_data, filter_results, qualified, metadata } = evaluation;

  return (
    <div className={`candidate-card ${qualified ? 'qualified' : 'disqualified'}`}>
      <div className="candidate-header">
        <div>
          <div className="candidate-title">{candidate_data.title}</div>
          <div className="candidate-id">{candidate_data.asin}</div>
        </div>
        <span className={`candidate-badge ${qualified ? 'qualified' : 'disqualified'}`}>
          {qualified ? 'Qualified' : 'Disqualified'}
        </span>
      </div>

      <div className="candidate-metrics">
        <span className="candidate-metric">
          INR {candidate_data.price?.toLocaleString('en-IN')}
        </span>
        <span className="candidate-metric">
          {candidate_data.rating} stars
        </span>
        <span className="candidate-metric">
          {candidate_data.reviews?.toLocaleString()} reviews
        </span>
        {metadata?.score && (
          <span className="candidate-metric" style={{ color: 'var(--color-accent-cyan)' }}>
            Score: {(metadata.score as number).toFixed(3)}
          </span>
        )}
      </div>

      <div className="filter-results">
        {filter_results.map((fr, idx) => (
          <div key={idx} className="filter-result">
            <span className={`filter-icon ${fr.passed ? 'passed' : 'failed'}`}>
              {fr.passed ? '+' : '-'}
            </span>
            <span style={{ color: 'var(--color-text-muted)', minWidth: '100px' }}>
              {fr.filter_name.replace('_', ' ')}:
            </span>
            <span>{fr.detail}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function StepDetail({ step }: { step: Step }) {
  const [activeTab, setActiveTab] = useState<'input' | 'output' | 'evaluations'>('input');

  const passedCount = step.evaluations.filter(e => e.qualified).length;
  const failedCount = step.evaluations.length - passedCount;
  const hasEvaluations = step.evaluations.length > 0;

  return (
    <div className="step-detail">
      <div className="step-detail-header">
        <h2 className="step-detail-title">{formatStepName(step.name)}</h2>
        <span className="step-detail-type">{step.step_type}</span>
      </div>

      {step.reasoning && (
        <div className="section">
          <h3 className="section-title">Reasoning</h3>
          <div className="reasoning-box">{step.reasoning}</div>
        </div>
      )}

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'input' ? 'active' : ''}`}
          onClick={() => setActiveTab('input')}
        >
          Input
        </button>
        <button
          className={`tab ${activeTab === 'output' ? 'active' : ''}`}
          onClick={() => setActiveTab('output')}
        >
          Output
        </button>
        {hasEvaluations && (
          <button
            className={`tab ${activeTab === 'evaluations' ? 'active' : ''}`}
            onClick={() => setActiveTab('evaluations')}
          >
            Evaluations ({step.evaluations.length})
          </button>
        )}
      </div>

      {activeTab === 'input' && step.input_data && (
        <div className="section">
          <div className="data-block">
            <pre>{JSON.stringify(step.input_data, null, 2)}</pre>
          </div>
        </div>
      )}

      {activeTab === 'output' && step.output_data && (
        <div className="section">
          <div className="data-block">
            <pre>{JSON.stringify(step.output_data, null, 2)}</pre>
          </div>
        </div>
      )}

      {activeTab === 'evaluations' && hasEvaluations && (
        <div className="evaluations-section">
          <div className="evaluations-summary">
            <div className="eval-stat">
              <div className="eval-stat-value">{step.evaluations.length}</div>
              <div className="eval-stat-label">Total Evaluated</div>
            </div>
            <div className="eval-stat">
              <div className="eval-stat-value passed">{passedCount}</div>
              <div className="eval-stat-label">Passed</div>
            </div>
            <div className="eval-stat">
              <div className="eval-stat-value failed">{failedCount}</div>
              <div className="eval-stat-label">Failed</div>
            </div>
          </div>

          <div className="candidate-list">
            {step.evaluations.map((evaluation, idx) => (
              <CandidateCard key={idx} evaluation={evaluation} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function App() {
  const [trace, setTrace] = useState<Trace | null>(null);
  const [selectedStep, setSelectedStep] = useState<number>(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadTrace = async () => {
      try {
        setTrace(traceData as Trace);
      } catch (error) {
        console.error('Failed to load trace:', error);
      } finally {
        setLoading(false);
      }
    };

    loadTrace();
  }, []);

  if (loading) {
    return (
      <div className="app">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading trace...</p>
        </div>
      </div>
    );
  }

  if (!trace) {
    return (
      <div className="app">
        <div className="empty-state">
          <h2 className="empty-state-title">No Trace Found</h2>
          <p>Run the demo to generate a trace file.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">X</div>
            <span className="logo-text">X-Ray Dashboard</span>
          </div>
          <div className="header-subtitle">Decision Trail Debugger</div>
        </div>
      </header>

      <main className="main-content">
        <div className="trace-overview">
          <div className="trace-header">
            <div>
              <h1 className="trace-title">{trace.name.replace('_', ' ').toUpperCase()}</h1>
              <span className="trace-id">{trace.trace_id}</span>
            </div>
            <div className="trace-meta">
              <div className="trace-meta-item">
                <span>Started:</span>
                <strong>{formatDateTime(trace.started_at)}</strong>
              </div>
              <div className="trace-meta-item">
                <span>Steps:</span>
                <strong>{trace.steps.length}</strong>
              </div>
            </div>
          </div>

          <div className="step-timeline">
            {trace.steps.map((step, index) => (
              <div
                key={index}
                className={`step-card ${selectedStep === index ? 'active' : ''}`}
                onClick={() => setSelectedStep(index)}
              >
                <span className="step-number">{index + 1}</span>
                <div className="step-type">{step.step_type}</div>
                <div className="step-name">{formatStepName(step.name)}</div>
                <span className={`step-status ${step.status === 'failed' ? 'failed' : ''}`}>
                  {step.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        {trace.steps[selectedStep] && (
          <StepDetail step={trace.steps[selectedStep]} />
        )}
      </main>
    </div>
  );
}

export default App;
