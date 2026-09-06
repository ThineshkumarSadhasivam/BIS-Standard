import { useState } from "react";
import "./index.css";

const API_URL = "http://localhost:8000";

function App() {
  const [tenderText, setTenderText] = useState("");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeTender = async () => {
    if (!tenderText.trim()) {
      setError("Please enter a procurement specification or tender.");
      return;
    }

    setLoading(true);
    setError("");
    setReport(null);

    try {
      const response = await fetch(
        `${API_URL}/standards/procurement-report`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            tender_text: tenderText,
            top_k: 5,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);

        throw new Error(
          errorData?.detail ||
            `Request failed with status ${response.status}`
        );
      }

      const data = await response.json();

      setReport(data);
    } catch (err) {
      console.error(err);
      setError(
        err.message ||
          "Unable to connect to the StandardsInsight backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const clearAnalysis = () => {
    setTenderText("");
    setReport(null);
    setError("");
  };

  return (
    <div className="app">

      {/* ================= NAVBAR ================= */}

      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">SI</div>

          <div>
            <h1>StandardsInsight</h1>
            <span>Indian Standards Intelligence Platform</span>
          </div>
        </div>

        <nav>
          <a className="active">Dashboard</a>
          <a>Tender Analysis</a>
          <a>Standards</a>
          <a>Reports</a>
        </nav>

        <div className="status">
          <span className="status-dot"></span>
          System Online
        </div>
      </header>

      {/* ================= MAIN ================= */}

      <main className="container">

        {/* HERO */}

        <section className="hero">
          <div className="hero-content">
            <div className="eyebrow">
              AI-POWERED PROCUREMENT INTELLIGENCE
            </div>

            <h2>
              Identify the right
              <span> Indian Standards</span>
            </h2>

            <p>
              Analyze procurement specifications, discover applicable
              BIS standards, detect compliance gaps, and receive
              evidence-backed recommendations.
            </p>

            <div className="hero-tags">
              <span>Semantic Search</span>
              <span>Compliance Intelligence</span>
              <span>Knowledge Graph</span>
              <span>Human-in-the-Loop</span>
            </div>
          </div>

          <div className="hero-visual">
            <div className="visual-card">
              <div className="visual-header">
                <span>AI ANALYSIS ENGINE</span>
                <span className="pulse"></span>
              </div>

              <div className="visual-flow">
                <div className="flow-node">
                  <strong>Tender</strong>
                  <small>Specification</small>
                </div>

                <div className="flow-line"></div>

                <div className="flow-node highlighted">
                  <strong>AI</strong>
                  <small>Semantic Match</small>
                </div>

                <div className="flow-line"></div>

                <div className="flow-node">
                  <strong>BIS</strong>
                  <small>Standards</small>
                </div>
              </div>

              <div className="visual-footer">
                <span>314 Standards</span>
                <span>39 Relationships</span>
              </div>
            </div>
          </div>
        </section>

        {/* ================= KPI ================= */}

        <section className="stats-grid">

          <StatCard
            value="314"
            label="Standards Indexed"
            icon="◎"
          />

          <StatCard
            value="39"
            label="Knowledge Relationships"
            icon="◇"
          />

          <StatCard
            value="4"
            label="Certification Records"
            icon="✓"
          />

          <StatCard
            value="AI"
            label="Human Verified"
            icon="◈"
          />

        </section>

        {/* ================= ANALYSIS ================= */}

        <section className="analysis-section">

          <div className="section-heading">
            <div>
              <span className="section-label">
                PROCUREMENT ANALYSIS
              </span>

              <h3>Analyze a Tender</h3>

              <p>
                Paste your procurement requirement below. StandardsInsight
                will identify applicable standards and analyze compliance.
              </p>
            </div>

            {report && (
              <button
                className="secondary-button"
                onClick={clearAnalysis}
              >
                New Analysis
              </button>
            )}
          </div>

          <div className="tender-card">

            <div className="input-header">
              <div>
                <label>Tender / Procurement Specification</label>
                <p>
                  Include product, material, grade, application,
                  certification requirements, or explicit IS references.
                </p>
              </div>

              <span className="character-count">
                {tenderText.length} characters
              </span>
            </div>

            <textarea
              value={tenderText}
              onChange={(e) => setTenderText(e.target.value)}
              placeholder="Example: Procurement of Ordinary Portland Cement 43 Grade for building construction. BIS certification is mandatory."
              disabled={loading}
            />

            <div className="input-footer">

              <div className="input-hint">
                <span>●</span>
                AI recommendation will be subject to confidence-based
                human verification.
              </div>

              <button
                className="analyze-button"
                onClick={analyzeTender}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Analyzing...
                  </>
                ) : (
                  <>
                    Analyze Tender
                    <span>→</span>
                  </>
                )}
              </button>

            </div>
          </div>

          {/* ERROR */}

          {error && (
            <div className="error-box">
              <strong>Analysis failed</strong>
              <span>{error}</span>
            </div>
          )}

        </section>

        {/* ================= RESULTS ================= */}

        {report && (
          <section className="results-section">

            <div className="results-header">
              <div>
                <span className="section-label">
                  PROCUREMENT INTELLIGENCE REPORT
                </span>

                <h3>Analysis Results</h3>
              </div>

              <div
                className={
                  report.executive_status ===
                  "HUMAN REVIEW REQUIRED"
                    ? "review-badge"
                    : "success-badge"
                }
              >
                {report.executive_status ===
                "HUMAN REVIEW REQUIRED"
                  ? "⚠ Human Review Required"
                  : "✓ Analysis Complete"}
              </div>
            </div>

            {/* TOP RESULT GRID */}

            <div className="result-grid">

              {/* RECOMMENDED STANDARD */}

              <div className="result-card standard-result">

                <div className="card-top">
                  <span className="card-label">
                    RECOMMENDED STANDARD
                  </span>

                  <span className="ai-badge">
                    AI RECOMMENDED
                  </span>
                </div>

                <div className="standard-number">
                  {report.recommended_standard?.is_number ||
                    report.executive_summary?.recommended_standard
                      ?.is_number ||
                    "N/A"}
                </div>

                <h4>
                  {report.recommended_standard?.title ||
                    report.executive_summary?.recommended_standard
                      ?.title ||
                    "Standard title unavailable"}
                </h4>

                <div className="standard-meta">
                  <span>
                    {report.recommended_standard?.domain ||
                      report.executive_summary?.recommended_standard
                        ?.domain ||
                      "Indian Standard"}
                  </span>

                  <span>
                    {report.recommended_standard?.standard_type ||
                      "Standard"}
                  </span>
                </div>

                <div className="confidence-section">
                  <div className="confidence-header">
                    <span>Recommendation Confidence</span>

                    <strong>
                      {formatPercentage(
                        report.recommended_standard?.confidence ||
                          report.executive_summary
                            ?.recommended_standard?.confidence
                      )}
                    </strong>
                  </div>

                  <div className="confidence-bar">
                    <div
                      style={{
                        width: `${Math.min(
                          ((report.recommended_standard?.confidence ||
                            report.executive_summary
                              ?.recommended_standard?.confidence ||
                            0) * 100),
                          100
                        )}%`,
                      }}
                    ></div>
                  </div>
                </div>

              </div>

              {/* COMPLIANCE */}

              <div className="result-card">

                <div className="card-top">
                  <span className="card-label">
                    COMPLIANCE INTELLIGENCE
                  </span>

                  <span className="verified-label">
                    VERIFIED
                  </span>
                </div>

                <div className="compliance-status">
                  <span className="check-circle">✓</span>

                  <div>
                    <strong>
                      {report.compliance?.status ||
                        "Not Available"}
                    </strong>

                    <small>
                      Overall Compliance Status
                    </small>
                  </div>
                </div>

                <div className="compliance-list">

                  <ComplianceRow
                    label="QCO Applicable"
                    value={report.compliance?.qco_applicable}
                  />

                  <ComplianceRow
                    label="ISI Mark Required"
                    value={report.compliance?.isi_mark_required}
                  />

                  <ComplianceRow
                    label="Latest Version"
                    value={report.compliance?.is_latest_version}
                  />

                </div>

                {report.compliance?.recommendation && (
                  <div className="recommendation-box">
                    <span>Recommendation</span>
                    <p>
                      {report.compliance.recommendation}
                    </p>
                  </div>
                )}

              </div>

            </div>

            {/* ================= REQUIREMENTS ================= */}

            <div className="result-card full-width">

              <div className="card-title-row">
                <div>
                  <span className="card-label">
                    REQUIREMENT EXTRACTION
                  </span>
                  <h4>Tender Requirements</h4>
                </div>

                <span className="verified-count">
                  {report.gap_analysis?.summary
                    ?.verified_requirements || 0} Verified
                </span>
              </div>

              <div className="requirements-grid">

                <Requirement
                  label="Product"
                  value={report.tender_requirements?.product}
                />

                <Requirement
                  label="Material"
                  value={report.tender_requirements?.material}
                />

                <Requirement
                  label="Cement Type"
                  value={prettyValue(
                    report.tender_requirements?.cement_type
                  )}
                />

                <Requirement
                  label="Grade"
                  value={report.tender_requirements?.grade}
                />

                <Requirement
                  label="Application"
                  value={
                    report.tender_requirements?.application
                  }
                />

                <Requirement
                  label="BIS Certification"
                  value={
                    report.tender_requirements
                      ?.certification_required
                      ? "Required"
                      : "Not specified"
                  }
                />

              </div>
            </div>

            {/* ================= GAP ANALYSIS ================= */}

            <div className="result-card full-width">

              <div className="card-title-row">

                <div>
                  <span className="card-label">
                    COMPLIANCE CHECK
                  </span>
                  <h4>Procurement Gap Analysis</h4>
                </div>

                <div className="gap-summary">

                  <div>
                    <strong>
                      {report.gap_analysis?.summary
                        ?.total_gaps || 0}
                    </strong>
                    <span>Total Gaps</span>
                  </div>

                  <div className="high">
                    <strong>
                      {report.gap_analysis?.summary?.high || 0}
                    </strong>
                    <span>High</span>
                  </div>

                  <div className="medium">
                    <strong>
                      {report.gap_analysis?.summary?.medium || 0}
                    </strong>
                    <span>Medium</span>
                  </div>

                </div>

              </div>

              {report.gap_analysis?.items?.length > 0 ? (
                <div className="gap-list">
                  {report.gap_analysis.items.map(
                    (gap, index) => (
                      <GapItem
                        key={index}
                        gap={gap}
                      />
                    )
                  )}
                </div>
              ) : (
                <div className="no-gaps">
                  <div className="large-check">✓</div>

                  <div>
                    <strong>
                      No procurement gaps detected
                    </strong>

                    <p>
                      All currently evaluated tender requirements
                      are satisfied by the available intelligence.
                    </p>
                  </div>
                </div>
              )}

              {report.gap_analysis?.warnings?.length > 0 && (
                <div className="warnings-section">

                  <h5>
                    ⚠ Warnings requiring attention
                  </h5>

                  {report.gap_analysis.warnings.map(
                    (warning, index) => (
                      <div
                        className="warning-item"
                        key={index}
                      >
                        <strong>
                          {warning.type?.replaceAll("_", " ")}
                        </strong>

                        <span>
                          {warning.message}
                        </span>
                      </div>
                    )
                  )}

                </div>
              )}

            </div>

            {/* ================= RELATED STANDARDS ================= */}

            <div className="result-card full-width">

              <div className="card-title-row">

                <div>
                  <span className="card-label">
                    KNOWLEDGE GRAPH
                  </span>

                  <h4>Related Standards</h4>
                </div>

                <span className="relationship-count">
                  {report.related_standards
                    ?.relationship_count || 0} Relationships
                </span>

              </div>

              <div className="relationship-stats">

                <RelationStat
                  label="Test References"
                  value={
                    report.related_standards
                      ?.category_counts?.test_references || 0
                  }
                />

                <RelationStat
                  label="Material References"
                  value={
                    report.related_standards
                      ?.category_counts?.material_references || 0
                  }
                />

                <RelationStat
                  label="Conformity Inputs"
                  value={
                    report.related_standards
                      ?.category_counts?.conformity_inputs || 0
                  }
                />

              </div>

              <div className="related-list">

                {(
                  report.related_standards?.standards || []
                ).slice(0, 12).map((item, index) => (

                  <div
                    className="related-item"
                    key={index}
                  >

                    <div className="relation-icon">
                      {getRelationIcon(
                        item.relationship_type
                      )}
                    </div>

                    <div className="related-content">

                      <div className="related-top">

                        <strong>
                          {item.related_standard?.is_number ||
                            "Unknown Standard"}
                        </strong>

                        <span>
                          {formatRelationType(
                            item.relationship_type
                          )}
                        </span>

                      </div>

                      <p>
                        {item.related_standard?.title ||
                          "Related standard"}
                      </p>

                    </div>

                  </div>

                ))}

              </div>

            </div>

            {/* ================= EVIDENCE + REVIEW ================= */}

            <div className="two-column">

              {/* EVIDENCE */}

              <div className="result-card">

                <div className="card-top">
                  <span className="card-label">
                    EVIDENCE
                  </span>

                  <span className="verified-label">
                    BIS SOURCE
                  </span>
                </div>

                <div className="evidence-list">

                  <Evidence
                    label="Source Authority"
                    value={
                      report.evidence?.source_authority
                    }
                  />

                  <Evidence
                    label="Source Type"
                    value={
                      report.evidence?.source_type
                    }
                  />

                  <Evidence
                    label="Source Document"
                    value={
                      report.evidence?.source_document
                    }
                  />

                  {report.evidence?.source_url && (
                    <div className="evidence-row">
                      <span>Source</span>

                      <a
                        href={report.evidence.source_url}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Open BIS Source →
                      </a>
                    </div>
                  )}

                </div>

              </div>

              {/* HUMAN REVIEW */}

              <div className="result-card review-card">

                <div className="card-top">
                  <span className="card-label">
                    DECISION CONTROL
                  </span>
                </div>

                <div className="review-content">

                  <div className="review-icon">
                    ⚠
                  </div>

                  <div>
                    <h4>
                      {report.human_review?.required
                        ? "Human Review Required"
                        : "Human Review Not Required"}
                    </h4>

                    {report.human_review?.reasons?.map(
                      (reason, index) => (
                        <p key={index}>
                          {reason}
                        </p>
                      )
                    )}

                  </div>

                </div>

              </div>

            </div>

            {/* ================= AUDIT TRAIL ================= */}

            <div className="result-card full-width">

              <div className="card-top">
                <span className="card-label">
                  TRACEABILITY
                </span>

                <span className="verified-label">
                  AUDIT TRAIL
                </span>
              </div>

              <div className="audit-trail">

                {(
                  report.audit_trail || []
                ).map((step, index) => (

                  <div
                    className="audit-step"
                    key={index}
                  >

                    <div className="audit-number">
                      {index + 1}
                    </div>

                    <div>
                      <strong>
                        {prettyValue(step)}
                      </strong>
                    </div>

                    {index <
                      report.audit_trail.length - 1 && (
                      <div className="audit-line"></div>
                    )}

                  </div>

                ))}

              </div>

            </div>

          </section>
        )}

        {/* ================= EMPTY STATE ================= */}

        {!report && !loading && (
          <section className="empty-state">

            <div className="empty-icon">⌕</div>

            <h3>Ready to analyze</h3>

            <p>
              Enter a procurement specification above to generate
              an AI-powered Procurement Intelligence Report.
            </p>

            <div className="example-box">

              <span>TRY AN EXAMPLE</span>

              <button
                onClick={() =>
                  setTenderText(
                    "Procurement of Ordinary Portland Cement 43 Grade for building construction. BIS certification is mandatory."
                  )
                }
              >
                Ordinary Portland Cement — 43 Grade →
              </button>

            </div>

          </section>
        )}

      </main>

      {/* ================= FOOTER ================= */}

      <footer>
        <div>
          <strong>StandardsInsight</strong>
          <span>
            AI-Powered Recommendation Engine for Indian Standards
          </span>
        </div>

        <span>
          Metadata-level analysis • Human verification enabled
        </span>
      </footer>

    </div>
  );
}


/* ============================================================
   COMPONENTS
============================================================ */

function StatCard({ value, label, icon }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>

      <div>
        <strong>{value}</strong>
        <span>{label}</span>
      </div>
    </div>
  );
}


function ComplianceRow({ label, value }) {
  const isTrue = value === true;

  return (
    <div className="compliance-row">

      <span>{label}</span>

      <strong className={isTrue ? "yes" : "no"}>
        {value === null || value === undefined
          ? "N/A"
          : isTrue
          ? "✓ YES"
          : "NO"}
      </strong>

    </div>
  );
}


function Requirement({ label, value }) {
  return (
    <div className="requirement-item">

      <span>{label}</span>

      <strong>
        {value || "Not specified"}
      </strong>

    </div>
  );
}


function GapItem({ gap }) {
  const severity =
    gap.severity?.toLowerCase() || "medium";

  return (
    <div className={`gap-item ${severity}`}>

      <div className="gap-severity">
        {gap.severity || "MEDIUM"}
      </div>

      <div>
        <strong>
          {gap.requirement || "Procurement Requirement"}
        </strong>

        <p>
          {gap.message || "Verification required."}
        </p>

        {gap.recommended_action && (
          <small>
            Recommended action: {gap.recommended_action}
          </small>
        )}
      </div>

    </div>
  );
}


function RelationStat({ label, value }) {
  return (
    <div className="relation-stat">
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}


function Evidence({ label, value }) {
  if (!value) return null;

  return (
    <div className="evidence-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}


/* ============================================================
   HELPERS
============================================================ */

function formatPercentage(value) {
  if (value === null || value === undefined) {
    return "0%";
  }

  return `${(Number(value) * 100).toFixed(2)}%`;
}


function prettyValue(value) {
  if (!value) return "Not specified";

  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}


function formatRelationType(value) {
  if (!value) return "RELATED";

  return value
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}


function getRelationIcon(type) {
  switch (type) {
    case "TEST_REFERENCE":
      return "T";

    case "MATERIAL_REFERENCE":
      return "M";

    case "CONFORMITY_INPUT":
      return "C";

    case "REFERENCED_STANDARD":
      return "R";

    default:
      return "•";
  }
}


export default App;