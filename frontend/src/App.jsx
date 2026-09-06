import { useState } from "react";
import "./index.css";

const API_URL = "http://localhost:8000";

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  const [tenderText, setTenderText] = useState("");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState("");
  const [selectedStandard, setSelectedStandard] = useState(null);
  const [intelligenceLoading, setIntelligenceLoading] = useState(false);

  /* ============================================================
     TENDER ANALYSIS
  ============================================================ */

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
        const data = await response.json().catch(() => null);

        throw new Error(
          data?.detail ||
            `Request failed with status ${response.status}`
        );
      }

      const data = await response.json();
      setReport(data);
    } catch (err) {
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

  /* ============================================================
     STANDARDS SEARCH
  ============================================================ */

  const searchStandards = async () => {
    if (!searchQuery.trim()) {
      setSearchError("Enter a product, material, application, or standard.");
      return;
    }

    setSearchLoading(true);
    setSearchError("");
    setSearchResults([]);
    setSelectedStandard(null);

    try {
      const response = await fetch(
        `${API_URL}/standards/search`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: searchQuery,
            top_k: 10,
          }),
        }
      );

      if (!response.ok) {
        const data = await response.json().catch(() => null);

        throw new Error(
          data?.detail ||
            `Search failed with status ${response.status}`
        );
      }

      const data = await response.json();

      const results =
        Array.isArray(data)
          ? data
          : data.results || data.standards || [];

      setSearchResults(results);
    } catch (err) {
      console.error(err);
      setSearchError(
        err.message ||
          "Unable to search the standards database."
      );
    } finally {
      setSearchLoading(false);
    }
  };

  /* ============================================================
     STANDARD INTELLIGENCE
  ============================================================ */

  const loadStandardIntelligence = async (standard) => {
    const id =
      standard.id ||
      standard.standard_id;

    if (!id) return;

    setSelectedStandard({
      ...standard,
      intelligence: null,
    });

    setIntelligenceLoading(true);

    try {
      const [
        versionResponse,
        amendmentResponse,
        certificationResponse,
        relationshipResponse,
      ] = await Promise.all([
        fetch(`${API_URL}/standards/${id}/version`),
        fetch(`${API_URL}/standards/${id}/amendments`),
        fetch(`${API_URL}/standards/${id}/certification`),
        fetch(`${API_URL}/standards/${id}/relationships`),
      ]);

      const [
        version,
        amendments,
        certification,
        relationships,
      ] = await Promise.all([
        safeJson(versionResponse),
        safeJson(amendmentResponse),
        safeJson(certificationResponse),
        safeJson(relationshipResponse),
      ]);

      setSelectedStandard({
        ...standard,
        intelligence: {
          version,
          amendments,
          certification,
          relationships,
        },
      });
    } catch (err) {
      console.error(err);

      setSelectedStandard({
        ...standard,
        intelligence: {
          error:
            "Some intelligence data could not be loaded.",
        },
      });
    } finally {
      setIntelligenceLoading(false);
    }
  };

  const goToTenderAnalysis = () => {
    setActivePage("tender");
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  return (
    <div className="app">

      {/* ========================================================
          NAVBAR
      ======================================================== */}

      <header className="navbar">

        <div className="brand">
          <div className="brand-icon">SI</div>

          <div>
            <h1>StandardsInsight</h1>
            <span>
              Indian Standards Intelligence Platform
            </span>
          </div>
        </div>

        <nav>
          <button
            className={
              activePage === "dashboard"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() => setActivePage("dashboard")}
          >
            Dashboard
          </button>

          <button
            className={
              activePage === "tender"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() => setActivePage("tender")}
          >
            Tender Analysis
          </button>

          <button
            className={
              activePage === "standards"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() => setActivePage("standards")}
          >
            Standards
          </button>

          <button className="nav-button">
            Reports
          </button>
        </nav>

        <div className="status">
          <span className="status-dot"></span>
          System Online
        </div>

      </header>

      {/* ========================================================
          DASHBOARD
      ======================================================== */}

      {activePage === "dashboard" && (
        <main className="container">

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
                Analyze procurement specifications, discover
                applicable BIS standards, detect compliance gaps,
                and receive evidence-backed recommendations.
              </p>

              <div className="hero-tags">
                <span>Semantic Search</span>
                <span>Compliance Intelligence</span>
                <span>Knowledge Graph</span>
                <span>Human-in-the-Loop</span>
              </div>

              <button
                className="analyze-button hero-button"
                onClick={goToTenderAnalysis}
              >
                Start Tender Analysis →
              </button>

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

          <section className="dashboard-actions">

            <div className="action-card">
              <div className="action-icon">⌕</div>

              <div>
                <span>STANDARD DISCOVERY</span>
                <h3>Explore Indian Standards</h3>
                <p>
                  Search standards using products, materials,
                  applications, or technical requirements.
                </p>
              </div>

              <button
                onClick={() => setActivePage("standards")}
              >
                Explore Standards →
              </button>
            </div>

            <div className="action-card">
              <div className="action-icon">▣</div>

              <div>
                <span>PROCUREMENT INTELLIGENCE</span>
                <h3>Analyze a Tender</h3>
                <p>
                  Identify applicable standards and detect
                  procurement compliance gaps.
                </p>
              </div>

              <button
                onClick={() => setActivePage("tender")}
              >
                Analyze Tender →
              </button>
            </div>

          </section>

        </main>
      )}

      {/* ========================================================
          TENDER ANALYSIS
      ======================================================== */}

      {activePage === "tender" && (
        <main className="container">

          <section className="page-header">

            <span className="section-label">
              PROCUREMENT INTELLIGENCE
            </span>

            <h2>Analyze a Tender</h2>

            <p>
              Paste your procurement requirement to identify
              applicable Indian Standards and evaluate compliance.
            </p>

          </section>

          <div className="tender-card">

            <div className="input-header">

              <div>
                <label>
                  Tender / Procurement Specification
                </label>

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
                AI recommendation will be subject to
                confidence-based human verification.
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

          {error && (
            <div className="error-box">
              <strong>Analysis failed</strong>
              <span>{error}</span>
            </div>
          )}

          {report && (
            <ReportView
              report={report}
              onNewAnalysis={clearAnalysis}
            />
          )}

        </main>
      )}

      {/* ========================================================
          STANDARDS EXPLORER
      ======================================================== */}

      {activePage === "standards" && (
        <main className="container">

          <section className="page-header">

            <span className="section-label">
              STANDARD DISCOVERY
            </span>

            <h2>Standards Explorer</h2>

            <p>
              Search the StandardsInsight knowledge base using
              products, materials, applications, or technical terms.
            </p>

          </section>

          <section className="standards-search-card">

            <div className="search-box">

              <span className="search-symbol">⌕</span>

              <input
                value={searchQuery}
                onChange={(e) =>
                  setSearchQuery(e.target.value)
                }
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    searchStandards();
                  }
                }}
                placeholder="Search e.g. ordinary Portland cement, coarse aggregate for concrete..."
              />

              <button
                onClick={searchStandards}
                disabled={searchLoading}
              >
                {searchLoading
                  ? "Searching..."
                  : "Search Standards"}
              </button>

            </div>

            <div className="search-examples">
              <span>Try:</span>

              <button
                onClick={() => {
                  setSearchQuery(
                    "ordinary Portland cement"
                  );
                }}
              >
                Ordinary Portland Cement
              </button>

              <button
                onClick={() => {
                  setSearchQuery(
                    "coarse aggregate for concrete"
                  );
                }}
              >
                Coarse Aggregate
              </button>

              <button
                onClick={() => {
                  setSearchQuery(
                    "requirements for plain and reinforced concrete"
                  );
                }}
              >
                Reinforced Concrete
              </button>
            </div>

          </section>

          {searchError && (
            <div className="error-box">
              <strong>Search failed</strong>
              <span>{searchError}</span>
            </div>
          )}

          <div className="explorer-layout">

            {/* SEARCH RESULTS */}

            <section className="search-results">

              <div className="results-heading">

                <div>
                  <span className="section-label">
                    SEARCH RESULTS
                  </span>

                  <h3>
                    {searchResults.length
                      ? `${searchResults.length} Standards Found`
                      : "Standards"}
                  </h3>
                </div>

              </div>

              {searchResults.length === 0 && (
                <div className="explorer-empty">
                  <div className="empty-icon">⌕</div>

                  <h3>
                    Search the standards database
                  </h3>

                  <p>
                    Enter a technical requirement to find
                    semantically relevant Indian Standards.
                  </p>
                </div>
              )}

              {searchResults.map((standard, index) => {

                const standardNumber =
                  standard.is_number ||
                  standard.reference ||
                  "Unknown Standard";

                const title =
                  standard.title ||
                  "Standard title unavailable";

                const confidence =
                  standard.rerank_score ??
                  standard.score ??
                  standard.confidence;

                return (
                  <button
                    className={
                      selectedStandard?.id === standard.id
                        ? "standard-search-result selected"
                        : "standard-search-result"
                    }
                    key={
                      standard.id ||
                      `${standardNumber}-${index}`
                    }
                    onClick={() =>
                      loadStandardIntelligence(standard)
                    }
                  >

                    <div className="standard-result-icon">
                      IS
                    </div>

                    <div className="standard-result-content">

                      <div className="standard-result-top">

                        <strong>
                          {standardNumber}
                        </strong>

                        {confidence !== undefined && (
                          <span className="confidence-pill">
                            {formatPercentage(confidence)}
                          </span>
                        )}

                      </div>

                      <h4>{title}</h4>

                      <div className="result-tags">

                        {standard.domain && (
                          <span>
                            {standard.domain}
                          </span>
                        )}

                        {standard.standard_type && (
                          <span>
                            {standard.standard_type}
                          </span>
                        )}

                        {standard.status && (
                          <span>
                            {standard.status}
                          </span>
                        )}

                      </div>

                    </div>

                    <span className="result-arrow">
                      →
                    </span>

                  </button>
                );
              })}

            </section>

            {/* STANDARD INTELLIGENCE */}

            <section className="standard-intelligence">

              {!selectedStandard && (
                <div className="intelligence-empty">

                  <div className="intelligence-icon">
                    ◇
                  </div>

                  <h3>
                    Standard Intelligence
                  </h3>

                  <p>
                    Select a standard from the search results
                    to view its version, amendments, certification,
                    and related standards.
                  </p>

                </div>
              )}

              {selectedStandard && (
                <StandardIntelligence
                  standard={selectedStandard}
                  loading={intelligenceLoading}
                />
              )}

            </section>

          </div>

        </main>
      )}

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
   REPORT VIEW
============================================================ */

function ReportView({ report, onNewAnalysis }) {
  return (
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

      <div className="result-grid">

        <div className="result-card">

          <div className="card-top">
            <span className="card-label">
              RECOMMENDED STANDARD
            </span>

            <span className="ai-badge">
              AI RECOMMENDED
            </span>
          </div>

          <div className="standard-number">
            {report.recommended_standard?.is_number}
          </div>

          <h4>
            {report.recommended_standard?.title}
          </h4>

          <div className="confidence-section">

            <div className="confidence-header">
              <span>
                Recommendation Confidence
              </span>

              <strong>
                {formatPercentage(
                  report.recommended_standard?.confidence
                )}
              </strong>
            </div>

            <div className="confidence-bar">
              <div
                style={{
                  width: `${Math.min(
                    (report.recommended_standard
                      ?.confidence || 0) * 100,
                    100
                  )}%`,
                }}
              ></div>
            </div>

          </div>

        </div>

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

            <span className="check-circle">
              ✓
            </span>

            <div>
              <strong>
                {report.compliance?.status}
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

        </div>

      </div>

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

            <div className="large-check">
              ✓
            </div>

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

      </div>

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

      </div>

      <div className="two-column">

        <div className="result-card">

          <div className="card-top">
            <span className="card-label">
              EVIDENCE
            </span>

            <span className="verified-label">
              BIS SOURCE
            </span>
          </div>

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

        <div className="result-card review-card">

          <span className="card-label">
            DECISION CONTROL
          </span>

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

          {report.audit_trail?.map(
            (step, index) => (
              <div
                className="audit-step"
                key={index}
              >

                <div className="audit-number">
                  {index + 1}
                </div>

                <strong>
                  {prettyValue(step)}
                </strong>

              </div>
            )
          )}

        </div>

      </div>

      <button
        className="secondary-button new-analysis-button"
        onClick={onNewAnalysis}
      >
        ← New Analysis
      </button>

    </section>
  );
}


/* ============================================================
   STANDARD INTELLIGENCE
============================================================ */

function StandardIntelligence({
  standard,
  loading,
}) {
  const intelligence = standard.intelligence;

  return (
    <div className="intelligence-panel">

      <div className="intelligence-header">

        <span className="card-label">
          STANDARD INTELLIGENCE
        </span>

        <span className="verified-label">
          BIS DATA
        </span>

      </div>

      <div className="intelligence-standard-number">
        {standard.is_number ||
          standard.reference ||
          "Unknown"}
      </div>

      <h3>
        {standard.title ||
          "Standard title unavailable"}
      </h3>

      <div className="intelligence-meta">

        {standard.domain && (
          <span>{standard.domain}</span>
        )}

        {standard.standard_type && (
          <span>{standard.standard_type}</span>
        )}

        {standard.status && (
          <span>{standard.status}</span>
        )}

      </div>

      {loading ? (
        <div className="intelligence-loading">
          <span className="spinner dark-spinner"></span>
          Loading standard intelligence...
        </div>
      ) : intelligence?.error ? (
        <div className="error-box">
          {intelligence.error}
        </div>
      ) : intelligence ? (
        <>

          <IntelligenceSection
            title="Version"
            icon="V"
          >
            <InfoRow
              label="Version Status"
              value={
                intelligence.version?.version_status
              }
            />

            <InfoRow
              label="Current Standard"
              value={
                intelligence.version?.current_standard
                  ?.is_number ||
                standard.is_number
              }
            />

            <InfoRow
              label="Resolution"
              value={
                intelligence.version?.resolution_note ||
                "No version conflict detected."
              }
            />
          </IntelligenceSection>

          <IntelligenceSection
            title="Amendments"
            icon="A"
          >
            <InfoRow
              label="Amendment Count"
              value={
                intelligence.amendments?.amendment_count ??
                intelligence.amendments?.amendments?.length ??
                0
              }
            />

            <InfoRow
              label="Latest Amendment"
              value={
                intelligence.amendments?.latest_amendment
                  ?.amendment_year ||
                "No amendment record"
              }
            />
          </IntelligenceSection>

          <IntelligenceSection
            title="Certification"
            icon="C"
          >
            <InfoRow
              label="Status"
              value={
                intelligence.certification
                  ?.overall_status ||
                "No Certification Evidence"
              }
            />

            <InfoRow
              label="Compulsory"
              value={
                intelligence.certification?.compulsory
                  ? "Yes"
                  : "No"
              }
            />

            <InfoRow
              label="Scheme"
              value={
                intelligence.certification
                  ?.certifications?.[0]?.scheme ||
                "Not specified"
              }
            />

            <InfoRow
              label="QCO"
              value={
                intelligence.certification
                  ?.certifications?.[0]?.qco_name ||
                "Not specified"
              }
            />
          </IntelligenceSection>

          <IntelligenceSection
            title="Knowledge Graph"
            icon="G"
          >

            <div className="graph-counts">

              <div>
                <strong>
                  {intelligence.relationships
                    ?.relationship_count || 0}
                </strong>
                <span>Relationships</span>
              </div>

              <div>
                <strong>
                  {intelligence.relationships
                    ?.category_counts
                    ?.test_references || 0}
                </strong>
                <span>Test References</span>
              </div>

              <div>
                <strong>
                  {intelligence.relationships
                    ?.category_counts
                    ?.material_references || 0}
                </strong>
                <span>Material</span>
              </div>

              <div>
                <strong>
                  {intelligence.relationships
                    ?.category_counts
                    ?.conformity_inputs || 0}
                </strong>
                <span>Conformity</span>
              </div>

            </div>

          </IntelligenceSection>

        </>
      ) : null}

    </div>
  );
}


/* ============================================================
   SMALL COMPONENTS
============================================================ */

function IntelligenceSection({
  title,
  icon,
  children,
}) {
  return (
    <div className="intelligence-section">

      <div className="intelligence-section-title">

        <span>
          {icon}
        </span>

        <h4>{title}</h4>

      </div>

      <div>
        {children}
      </div>

    </div>
  );
}


function InfoRow({ label, value }) {
  return (
    <div className="info-row">

      <span>{label}</span>

      <strong>
        {value || "Not available"}
      </strong>

    </div>
  );
}


function StatCard({
  value,
  label,
  icon,
}) {
  return (
    <div className="stat-card">

      <div className="stat-icon">
        {icon}
      </div>

      <div>
        <strong>{value}</strong>
        <span>{label}</span>
      </div>

    </div>
  );
}


function ComplianceRow({
  label,
  value,
}) {
  return (
    <div className="compliance-row">

      <span>{label}</span>

      <strong
        className={
          value === true
            ? "yes"
            : "no"
        }
      >
        {value === true
          ? "✓ YES"
          : value === false
          ? "NO"
          : "N/A"}
      </strong>

    </div>
  );
}


function Requirement({
  label,
  value,
}) {
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
  return (
    <div
      className={`gap-item ${
        gap.severity?.toLowerCase() || "medium"
      }`}
    >

      <div className="gap-severity">
        {gap.severity || "MEDIUM"}
      </div>

      <div>
        <strong>
          {gap.requirement ||
            "Procurement Requirement"}
        </strong>

        <p>
          {gap.message ||
            "Verification required."}
        </p>

        {gap.recommended_action && (
          <small>
            Recommended action:{" "}
            {gap.recommended_action}
          </small>
        )}

      </div>

    </div>
  );
}


function RelationStat({
  label,
  value,
}) {
  return (
    <div className="relation-stat">
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}


function Evidence({
  label,
  value,
}) {
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

async function safeJson(response) {
  if (!response.ok) {
    return null;
  }

  return response.json();
}


function formatPercentage(value) {
  if (
    value === null ||
    value === undefined
  ) {
    return "0%";
  }

  return `${(
    Number(value) * 100
  ).toFixed(2)}%`;
}


function prettyValue(value) {
  if (!value) return "Not specified";

  return String(value)
    .replaceAll("_", " ")
    .replace(
      /\b\w/g,
      (char) => char.toUpperCase()
    );
}


export default App;