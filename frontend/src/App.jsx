import { useState } from "react";
import "./index.css";

const API_URL = "http://localhost:8000";

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  // ==========================================================
  // TENDER ANALYSIS
  // ==========================================================

  const [tenderText, setTenderText] = useState("");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [pdfLoading, setPdfLoading] = useState(false);

  // ==========================================================
  // STANDARDS EXPLORER
  // ==========================================================

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState("");

  const [selectedStandard, setSelectedStandard] =
    useState(null);

  const [intelligenceLoading, setIntelligenceLoading] =
    useState(false);

  // ==========================================================
  // TENDER ANALYSIS
  // ==========================================================

  const analyzeTender = async () => {
    if (!tenderText.trim()) {
      setError(
        "Please enter a procurement specification or tender."
      );
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
        const data = await response
          .json()
          .catch(() => null);

        throw new Error(
          data?.detail ||
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

  // ==========================================================
  // PDF PROCUREMENT REPORT
  // ==========================================================

  const downloadProcurementPDF = async () => {
    if (!tenderText.trim()) {
      setError("Tender text is not available for PDF generation.");
      return;
    }

    try {
      setPdfLoading(true);
      setError("");

      const response = await fetch(
        `${API_URL}/standards/procurement-report/pdf`,
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
        const data = await response
          .json()
          .catch(() => null);

        throw new Error(
          data?.detail ||
            `PDF generation failed with status ${response.status}`
        );
      }

      const blob = await response.blob();

      const downloadUrl =
        window.URL.createObjectURL(blob);

      const link =
        document.createElement("a");

      link.href = downloadUrl;
      link.download =
        "StandardsInsight_Procurement_Intelligence_Report.pdf";

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(downloadUrl);

    } catch (err) {
      console.error("PDF generation error:", err);

      setError(
        err.message ||
          "Unable to generate the procurement PDF report."
      );
    } finally {
      setPdfLoading(false);
    }
  };

  const clearAnalysis = () => {
    setTenderText("");
    setReport(null);
    setError("");
  };

  // ==========================================================
  // STANDARD SEARCH
  // ==========================================================

  const searchStandards = async () => {
    if (!searchQuery.trim()) {
      setSearchError(
        "Enter a product, material, application, or standard number."
      );
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
        const data = await response
          .json()
          .catch(() => null);

        throw new Error(
          data?.detail ||
            `Search failed with status ${response.status}`
        );
      }

      const data = await response.json();

      const results = Array.isArray(data)
        ? data
        : data.results ||
          data.standards ||
          [];

      setSearchResults(results);

      // Automatically open exact standard result
      if (
        results.length === 1 &&
        results[0].match_type ===
          "EXACT_STANDARD_NUMBER"
      ) {
        loadStandardIntelligence(results[0]);
      }
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

  // ==========================================================
  // LOAD STANDARD INTELLIGENCE
  // ==========================================================

  const loadStandardIntelligence = async (
    standard
  ) => {
    const id =
      standard?.id ||
      standard?.standard_id;

    if (!id) {
      return;
    }

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
        fetch(
          `${API_URL}/standards/${id}/version`
        ),
        fetch(
          `${API_URL}/standards/${id}/amendments`
        ),
        fetch(
          `${API_URL}/standards/${id}/certification`
        ),
        fetch(
          `${API_URL}/standards/${id}/relationships`
        ),
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
      console.error(
        "Standard intelligence error:",
        err
      );

      setSelectedStandard({
        ...standard,

        intelligence: {
          version: null,
          amendments: null,
          certification: null,
          relationships: null,

          error:
            "Unable to load standard intelligence.",
        },
      });
    } finally {
      setIntelligenceLoading(false);
    }
  };

  // ==========================================================
  // NAVIGATION
  // ==========================================================

  const openTenderPage = () => {
    setActivePage("tender");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const openStandardsPage = () => {
    setActivePage("standards");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // ==========================================================
  // RENDER
  // ==========================================================

  return (
    <div className="app">

      {/* ======================================================
          NAVBAR
      ====================================================== */}

      <header className="navbar">

        <div className="brand">

          <div className="brand-icon">
            SI
          </div>

          <div>
            <h1>
              StandardsInsight
            </h1>

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
            onClick={() =>
              setActivePage("dashboard")
            }
          >
            Dashboard
          </button>

          <button
            className={
              activePage === "tender"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={openTenderPage}
          >
            Tender Analysis
          </button>

          <button
            className={
              activePage === "standards"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={openStandardsPage}
          >
            Standards
          </button>

        </nav>

        <div className="status">
          <span className="status-dot"></span>
          System Online
        </div>

      </header>


      {/* ======================================================
          DASHBOARD
      ====================================================== */}

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
                Analyze procurement specifications,
                discover applicable BIS standards,
                detect compliance gaps, and receive
                evidence-backed recommendations.
              </p>

              <div className="hero-tags">

                <span>
                  Semantic Search
                </span>

                <span>
                  Compliance Intelligence
                </span>

                <span>
                  Knowledge Graph
                </span>

                <span>
                  Human-in-the-Loop
                </span>

              </div>

              <button
                className="analyze-button hero-button"
                onClick={openTenderPage}
              >
                Start Tender Analysis →
              </button>

            </div>


            <div className="hero-visual">

              <div className="visual-card">

                <div className="visual-header">
                  <span>
                    AI ANALYSIS ENGINE
                  </span>

                  <span className="pulse"></span>
                </div>

                <div className="visual-flow">

                  <div className="flow-node">
                    <strong>
                      Tender
                    </strong>

                    <small>
                      Specification
                    </small>
                  </div>

                  <div className="flow-line"></div>

                  <div className="flow-node highlighted">
                    <strong>
                      AI
                    </strong>

                    <small>
                      Semantic Match
                    </small>
                  </div>

                  <div className="flow-line"></div>

                  <div className="flow-node">
                    <strong>
                      BIS
                    </strong>

                    <small>
                      Standards
                    </small>
                  </div>

                </div>

                <div className="visual-footer">
                  <span>
                    314 Standards
                  </span>

                  <span>
                    39 Relationships
                  </span>
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

              <div className="action-icon">
                ⌕
              </div>

              <div>
                <span>
                  STANDARD DISCOVERY
                </span>

                <h3>
                  Explore Indian Standards
                </h3>

                <p>
                  Search standards using products,
                  materials, applications, or technical
                  requirements.
                </p>
              </div>

              <button
                onClick={openStandardsPage}
              >
                Explore Standards →
              </button>

            </div>


            <div className="action-card">

              <div className="action-icon">
                ▣
              </div>

              <div>
                <span>
                  PROCUREMENT INTELLIGENCE
                </span>

                <h3>
                  Analyze a Tender
                </h3>

                <p>
                  Identify applicable standards and
                  detect procurement compliance gaps.
                </p>
              </div>

              <button
                onClick={openTenderPage}
              >
                Analyze Tender →
              </button>

            </div>

          </section>

        </main>
      )}


      {/* ======================================================
          TENDER PAGE
      ====================================================== */}

      {activePage === "tender" && (

        <main className="container">

          <section className="page-header">

            <span className="section-label">
              PROCUREMENT INTELLIGENCE
            </span>

            <h2>
              Analyze a Tender
            </h2>

            <p>
              Paste your procurement requirement to
              identify applicable Indian Standards
              and evaluate compliance.
            </p>

          </section>


          <div className="tender-card">

            <div className="input-header">

              <div>

                <label>
                  Tender / Procurement Specification
                </label>

                <p>
                  Include product, material, grade,
                  application, certification requirements,
                  or explicit IS references.
                </p>

              </div>

              <span className="character-count">
                {tenderText.length} characters
              </span>

            </div>


            <textarea
              value={tenderText}
              onChange={(e) =>
                setTenderText(e.target.value)
              }
              placeholder="Example: Procurement of Ordinary Portland Cement 43 Grade for building construction. BIS certification is mandatory."
              disabled={loading}
            />


            <div className="input-footer">

              <div className="input-hint">

                <span>
                  ●
                </span>

                AI recommendation will be subject
                to confidence-based human verification.

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

              <strong>
                Analysis failed
              </strong>

              <span>
                {error}
              </span>

            </div>

          )}


          {report && (

            <ReportView
              report={report}
              tenderText={tenderText}
              onNewAnalysis={clearAnalysis}
              onDownloadPDF={downloadProcurementPDF}
              pdfLoading={pdfLoading}
            />

          )}

        </main>
      )}


      {/* ======================================================
          STANDARDS EXPLORER
      ====================================================== */}

      {activePage === "standards" && (

        <main className="container">

          <section className="page-header">

            <span className="section-label">
              STANDARD DISCOVERY
            </span>

            <h2>
              Standards Explorer
            </h2>

            <p>
              Search the StandardsInsight knowledge
              base using products, materials, applications,
              or technical terms.
            </p>

          </section>


          <section className="standards-search-card">

            <div className="search-box">

              <span className="search-symbol">
                ⌕
              </span>

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
                placeholder="Search e.g. IS 269:2015, ordinary Portland cement, coarse aggregate..."
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

              <span>
                Try:
              </span>

              <button
                onClick={() => {
                  setSearchQuery(
                    "IS 269:2015"
                  );
                }}
              >
                IS 269:2015
              </button>

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

            </div>

          </section>


          {searchError && (

            <div className="error-box">

              <strong>
                Search failed
              </strong>

              <span>
                {searchError}
              </span>

            </div>

          )}


          <div className="explorer-layout">

            {/* =================================================
                SEARCH RESULTS
            ================================================= */}

            <section className="search-results">

              <div className="results-heading">

                <span className="section-label">
                  SEARCH RESULTS
                </span>

                <h3>
                  {searchResults.length
                    ? `${searchResults.length} Standards Found`
                    : "Standards"}
                </h3>

              </div>


              {searchResults.length === 0 && (

                <div className="explorer-empty">

                  <div className="empty-icon">
                    ⌕
                  </div>

                  <h3>
                    Search the standards database
                  </h3>

                  <p>
                    Enter a technical requirement
                    to find semantically relevant
                    Indian Standards.
                  </p>

                </div>

              )}


              {searchResults.map(
                (standard, index) => {

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

                  const isExact =
                    standard.match_type ===
                    "EXACT_STANDARD_NUMBER";

                  const isSelected =
                    selectedStandard?.id ===
                    standard.id;


                  return (

                    <button
                      className={
                        isSelected
                          ? "standard-search-result selected"
                          : "standard-search-result"
                      }
                      key={
                        standard.id ||
                        `${standardNumber}-${index}`
                      }
                      onClick={() =>
                        loadStandardIntelligence(
                          standard
                        )
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


                          {isExact ? (

                            <span className="exact-match-pill">
                              ✓ EXACT MATCH
                            </span>

                          ) : confidence !==
                            undefined ? (

                            <span className="confidence-pill">
                              {formatPercentage(
                                confidence
                              )}
                            </span>

                          ) : null}

                        </div>


                        <h4>
                          {title}
                        </h4>


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

                }
              )}

            </section>


            {/* =================================================
                INTELLIGENCE
            ================================================= */}

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
                    Select a standard from the search
                    results to view its version, amendments,
                    certification, and related standards.
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


      {/* ======================================================
          FOOTER
      ====================================================== */}

      <footer>

        <div>

          <strong>
            StandardsInsight
          </strong>

          <span>
            AI-Powered Recommendation Engine
            for Indian Standards
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
   STANDARD INTELLIGENCE
============================================================ */

function StandardIntelligence({
  standard,
  loading,
}) {
  const intelligence =
    standard?.intelligence;

  const version =
    intelligence?.version || {};

  const amendments =
    intelligence?.amendments || {};

  const certification =
    intelligence?.certification || {};

  const relationships =
    intelligence?.relationships || {};


  // ----------------------------------------------------------
  // Handle different backend response shapes
  // ----------------------------------------------------------

  const amendmentList =
    Array.isArray(amendments)
      ? amendments
      : amendments?.amendments ||
        amendments?.records ||
        [];


  const certificationList =
    certification?.certifications ||
    [];


  const graphStandards =
    relationships?.standards ||
    [];


  return (

    <div className="intelligence-panel">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <div className="intelligence-header">

        <div>

          <span className="card-label">
            STANDARD INTELLIGENCE
          </span>

          <h3 className="details-heading">
            Detailed Standard Profile
          </h3>

        </div>

        <span className="verified-label">
          BIS DATA
        </span>

      </div>


      {/* ======================================================
          STANDARD OVERVIEW
      ====================================================== */}

      <div className="standard-overview">

        <div className="overview-number">

          {standard.is_number ||
            standard.reference ||
            "Unknown Standard"}

        </div>


        <h2>

          {standard.title ||
            "Standard title unavailable"}

        </h2>


        <div className="intelligence-meta">

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


        {standard.match_type ===
          "EXACT_STANDARD_NUMBER" && (

          <div className="exact-match-banner">

            ✓ Exact Standard Number Match

          </div>

        )}

      </div>


      {/* ======================================================
          LOADING
      ====================================================== */}

      {loading ? (

        <div className="intelligence-loading">

          <span className="spinner dark-spinner"></span>

          Loading standard intelligence...

        </div>

      ) : intelligence?.error ? (

        <div className="error-box">
          {intelligence.error}
        </div>

      ) : (

        <>

          {/* ==================================================
              VERSION
          ================================================== */}

          <div className="detail-section">

            <DetailSectionHeader
              icon="V"
              label="VERSION INTELLIGENCE"
              title="Version & Supersession"
            />


            <div className="detail-grid">

              <DetailItem
                label="Version Status"
                value={
                  version.version_status ||
                  "Current"
                }
              />

              <DetailItem
                label="Current Standard"
                value={
                  version.current_standard
                    ?.is_number ||
                  standard.is_number ||
                  "Not available"
                }
              />

              <DetailItem
                label="Relationship"
                value={
                  version.relationship ||
                  "No supersession relationship"
                }
              />

              <DetailItem
                label="Supersedes"
                value={
                  version.supersedes ||
                  "None recorded"
                }
              />

            </div>


            {version.resolution_note && (

              <div className="detail-note">

                <strong>
                  Resolution
                </strong>

                <p>
                  {version.resolution_note}
                </p>

              </div>

            )}

          </div>


          {/* ==================================================
              CERTIFICATION
          ================================================== */}

          <div className="detail-section">

            <DetailSectionHeader
              icon="C"
              label="CERTIFICATION INTELLIGENCE"
              title="BIS Certification & QCO"
            />


            <div className="certification-status-box">

              <div className="certification-check">
                ✓
              </div>

              <div>

                <strong>
                  {certification.overall_status ||
                    "No Certification Evidence"}
                </strong>

                <small>
                  Overall Certification Status
                </small>

              </div>

            </div>


            <div className="detail-grid">

              <DetailItem
                label="Compulsory"
                value={
                  certification.compulsory
                    ? "YES"
                    : "NO"
                }
                highlight={
                  certification.compulsory
                }
              />

              <DetailItem
                label="Certification Records"
                value={
                  certification.certification_count ??
                  certificationList.length
                }
              />

            </div>


            {certificationList.length > 0 && (

              <div className="certification-records">

                {certificationList.map(
                  (record, index) => (

                    <div
                      className="certification-record"
                      key={index}
                    >

                      <div className="record-header">

                        <strong>
                          {record.scheme ||
                            "BIS Certification"}
                        </strong>

                        {record.compulsory && (
                          <span>
                            COMPULSORY
                          </span>
                        )}

                      </div>


                      <DetailItem
                        label="Status"
                        value={
                          record.certification_status ||
                          "Not specified"
                        }
                      />

                      <DetailItem
                        label="Product Category"
                        value={
                          record.product_category ||
                          "Not specified"
                        }
                      />

                      <DetailItem
                        label="QCO"
                        value={
                          record.qco_name ||
                          "Not specified"
                        }
                      />

                      {record.notification_reference && (

                        <DetailItem
                          label="Notification"
                          value={
                            record.notification_reference
                          }
                        />

                      )}

                    </div>

                  )
                )}

              </div>

            )}

          </div>


          {/* ==================================================
              AMENDMENTS
          ================================================== */}

          <div className="detail-section">

            <DetailSectionHeader
              icon="A"
              label="AMENDMENT INTELLIGENCE"
              title="Amendment History"
            />


            <div className="amendment-summary">

              <div>

                <strong>
                  {amendmentList.length}
                </strong>

                <span>
                  Recorded Amendments
                </span>

              </div>


              <div>

                <strong>
                  {getLatestAmendmentYear(
                    amendmentList
                  )}
                </strong>

                <span>
                  Latest Amendment
                </span>

              </div>

            </div>


            {amendmentList.length > 0 ? (

              <div className="amendment-list">

                {amendmentList.map(
                  (amendment, index) => (

                    <div
                      className="amendment-row"
                      key={index}
                    >

                      <div className="amendment-number">

                        {amendment.amendment_number ||
                          index + 1}

                      </div>

                      <div>

                        <strong>
                          Amendment{" "}
                          {amendment.amendment_number ||
                            index + 1}
                        </strong>

                        <span>
                          Year:{" "}
                          {amendment.amendment_year ||
                            "Not specified"}
                        </span>

                      </div>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="no-data-box">

                No amendment records are currently
                available for this standard in the
                verified dataset.

              </div>

            )}

          </div>


          {/* ==================================================
              KNOWLEDGE GRAPH
          ================================================== */}

          <div className="detail-section">

            <DetailSectionHeader
              icon="G"
              label="KNOWLEDGE GRAPH"
              title="Related Standards"
            />


            <div className="graph-counts detailed">

              <div>

                <strong>
                  {relationships.relationship_count ||
                    0}
                </strong>

                <span>
                  Relationships
                </span>

              </div>


              <div>

                <strong>
                  {relationships.category_counts
                    ?.test_references || 0}
                </strong>

                <span>
                  Test References
                </span>

              </div>


              <div>

                <strong>
                  {relationships.category_counts
                    ?.material_references || 0}
                </strong>

                <span>
                  Material
                </span>

              </div>


              <div>

                <strong>
                  {relationships.category_counts
                    ?.conformity_inputs || 0}
                </strong>

                <span>
                  Conformity
                </span>

              </div>

            </div>


            {graphStandards.length > 0 && (

              <div className="graph-mini-list">

                {graphStandards
                  .slice(0, 8)
                  .map((item, index) => (

                    <div
                      className="graph-mini-item"
                      key={index}
                    >

                      <span className="graph-type">

                        {getRelationshipInitial(
                          item.relationship_type
                        )}

                      </span>


                      <div>

                        <strong>
                          {item.is_number ||
                            item.standard_number ||
                            item.reference ||
                            "Standard"}
                        </strong>

                        <small>
                          {item.relationship_type ||
                            "Related Standard"}
                        </small>

                      </div>

                    </div>

                  ))}

              </div>

            )}

          </div>


          {/* ==================================================
              EVIDENCE
          ================================================== */}

          <div className="detail-section">

            <DetailSectionHeader
              icon="E"
              label="EVIDENCE"
              title="BIS Source & Verification"
            />


            <div className="evidence-detail">

              <DetailItem
                label="Source Authority"
                value={
                  standard.source_authority ||
                  "BIS"
                }
              />

              <DetailItem
                label="Source Type"
                value={
                  standard.source_type ||
                  "BIS Source"
                }
              />

              <DetailItem
                label="Verification Status"
                value={
                  standard.verification_status ||
                  "Not specified"
                }
              />

              <DetailItem
                label="Source Document"
                value={
                  standard.source_document ||
                  "Not available"
                }
              />

            </div>


            {standard.source_url && (

              <a
                className="bis-source-button"
                href={standard.source_url}
                target="_blank"
                rel="noreferrer"
              >
                Open BIS Source →
              </a>

            )}

          </div>

        </>

      )}

    </div>
  );
}


/* ============================================================
   DETAIL SECTION HEADER
============================================================ */

function DetailSectionHeader({
  icon,
  label,
  title,
}) {
  return (
    <div className="detail-section-header">

      <div className="detail-icon">
        {icon}
      </div>

      <div>

        <span>
          {label}
        </span>

        <h4>
          {title}
        </h4>

      </div>

    </div>
  );
}


/* ============================================================
   DETAIL ITEM
============================================================ */

function DetailItem({
  label,
  value,
  highlight = false,
}) {
  return (
    <div className="detail-item">

      <span>
        {label}
      </span>

      <strong
        className={
          highlight
            ? "detail-highlight"
            : ""
        }
      >
        {value || "Not available"}
      </strong>

    </div>
  );
}


/* ============================================================
   REPORT VIEW
============================================================ */

function ReportView({
  report,
  tenderText,
  onNewAnalysis,
  onDownloadPDF,
  pdfLoading,
}) {
  return (
    <section className="results-section">

      <div className="results-header">

        <div>

          <span className="section-label">
            PROCUREMENT INTELLIGENCE REPORT
          </span>

          <h3>
            Analysis Results
          </h3>

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

        {/* RECOMMENDED STANDARD */}

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
            {report.recommended_standard
              ?.is_number}
          </div>


          <h4>
            {report.recommended_standard
              ?.title}
          </h4>


          <div className="confidence-section">

            <div className="confidence-header">

              <span>
                Recommendation Confidence
              </span>

              <strong>
                {formatPercentage(
                  report.recommended_standard
                    ?.confidence
                )}
              </strong>

            </div>


            <div className="confidence-bar">

              <div
                style={{
                  width: `${Math.min(
                    (
                      report
                        .recommended_standard
                        ?.confidence || 0
                    ) * 100,
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

            <span className="check-circle">
              ✓
            </span>

            <div>

              <strong>
                {report.compliance
                  ?.status ||
                  "Not available"}
              </strong>

              <small>
                Overall Compliance Status
              </small>

            </div>

          </div>


          <div className="compliance-list">

            <ComplianceRow
              label="QCO Applicable"
              value={
                report.compliance
                  ?.qco_applicable
              }
            />

            <ComplianceRow
              label="ISI Mark Required"
              value={
                report.compliance
                  ?.isi_mark_required
              }
            />

            <ComplianceRow
              label="Latest Version"
              value={
                report.compliance
                  ?.is_latest_version
              }
            />

          </div>

        </div>

      </div>


      {/* REQUIREMENTS */}

      <div className="result-card full-width">

        <div className="card-title-row">

          <div>

            <span className="card-label">
              REQUIREMENT EXTRACTION
            </span>

            <h4>
              Tender Requirements
            </h4>

          </div>

          <span className="verified-count">
            {report.tender_requirements
              ?.verified_requirements ||
              report.gap_analysis
                ?.summary
                ?.verified_requirements ||
              0}{" "}
            Verified
          </span>

        </div>


        <div className="requirements-grid">

          <Requirement
            label="Product"
            value={
              report.tender_requirements
                ?.product
            }
          />

          <Requirement
            label="Material"
            value={
              report.tender_requirements
                ?.material
            }
          />

          <Requirement
            label="Cement Type"
            value={prettyValue(
              report.tender_requirements
                ?.cement_type
            )}
          />

          <Requirement
            label="Grade"
            value={
              report.tender_requirements
                ?.grade
            }
          />

          <Requirement
            label="Application"
            value={
              report.tender_requirements
                ?.application
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


      {/* GAP ANALYSIS */}

      <div className="result-card full-width">

        <div className="card-title-row">

          <div>

            <span className="card-label">
              COMPLIANCE CHECK
            </span>

            <h4>
              Procurement Gap Analysis
            </h4>

          </div>


          <div className="gap-summary">

            <div>

              <strong>
                {report.gap_analysis
                  ?.summary?.total_gaps || 0}
              </strong>

              <span>
                Total Gaps
              </span>

            </div>


            <div className="high">

              <strong>
                {report.gap_analysis
                  ?.summary?.high || 0}
              </strong>

              <span>
                High
              </span>

            </div>


            <div className="medium">

              <strong>
                {report.gap_analysis
                  ?.summary?.medium || 0}
              </strong>

              <span>
                Medium
              </span>

            </div>

          </div>

        </div>


        {report.gap_analysis
          ?.items?.length > 0 ? (

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
                All currently evaluated tender
                requirements are satisfied by
                the available intelligence.
              </p>

            </div>

          </div>

        )}

      </div>


      {/* KNOWLEDGE GRAPH */}

      <div className="result-card full-width">

        <div className="card-title-row">

          <div>

            <span className="card-label">
              KNOWLEDGE GRAPH
            </span>

            <h4>
              Related Standards
            </h4>

          </div>

          <span className="relationship-count">
            {report.related_standards
              ?.relationship_count || 0}{" "}
            Relationships
          </span>

        </div>


        <div className="relationship-stats">

          <RelationStat
            label="Test References"
            value={
              report.related_standards
                ?.category_counts
                ?.test_references || 0
            }
          />

          <RelationStat
            label="Material References"
            value={
              report.related_standards
                ?.category_counts
                ?.material_references || 0
            }
          />

          <RelationStat
            label="Conformity Inputs"
            value={
              report.related_standards
                ?.category_counts
                ?.conformity_inputs || 0
            }
          />

        </div>


        {report.related_standards
          ?.standards?.length > 0 && (

          <div className="report-related-list">

            {report.related_standards.standards
              .slice(0, 18)
              .map((item, index) => (

                <div
                  className="report-related-item"
                  key={index}
                >

                  <strong>
                    {item.is_number ||
                      item.standard_number ||
                      item.reference}
                  </strong>

                  <span>
                    {item.relationship_type ||
                      "Related Standard"}
                  </span>

                </div>

              ))}

          </div>

        )}

      </div>


      {/* EVIDENCE + REVIEW */}

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
              report.evidence
                ?.source_authority
            }
          />

          <Evidence
            label="Source Type"
            value={
              report.evidence
                ?.source_type
            }
          />

          <Evidence
            label="Source Document"
            value={
              report.evidence
                ?.source_document
            }
          />


          {report.evidence
            ?.source_url && (

            <div className="evidence-row">

              <span>
                Source
              </span>

              <a
                href={
                  report.evidence.source_url
                }
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
                {report.human_review
                  ?.required
                  ? "Human Review Required"
                  : "Human Review Not Required"}
              </h4>


              {report.human_review
                ?.reasons?.map(
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


      {/* AUDIT TRAIL */}

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


      <div className="report-actions">

        <button
          className="pdf-button"
          onClick={onDownloadPDF}
          disabled={pdfLoading || !tenderText?.trim()}
        >
          {pdfLoading ? (
            <>
              <span className="pdf-spinner"></span>
              Generating PDF...
            </>
          ) : (
            <>
              <span className="pdf-icon">↓</span>
              Generate PDF Report
            </>
          )}
        </button>

        <button
          className="secondary-button new-analysis-button"
          onClick={onNewAnalysis}
          disabled={pdfLoading}
        >
          ← New Analysis
        </button>

      </div>

    </section>
  );
}


/* ============================================================
   SMALL COMPONENTS
============================================================ */

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

        <strong>
          {value}
        </strong>

        <span>
          {label}
        </span>

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

      <span>
        {label}
      </span>

      <strong
        className={
          value === true
            ? "yes"
            : value === false
            ? "no"
            : ""
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

      <span>
        {label}
      </span>

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
        gap.severity?.toLowerCase() ||
        "medium"
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

      <strong>
        {value}
      </strong>

      <span>
        {label}
      </span>

    </div>
  );
}


function Evidence({
  label,
  value,
}) {
  if (!value) {
    return null;
  }

  return (
    <div className="evidence-row">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

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
    value === undefined ||
    Number.isNaN(Number(value))
  ) {
    return "0%";
  }

  return `${(
    Number(value) * 100
  ).toFixed(2)}%`;
}


function prettyValue(value) {
  if (!value) {
    return "Not specified";
  }

  return String(value)
    .replaceAll("_", " ")
    .replace(
      /\b\w/g,
      (char) => char.toUpperCase()
    );
}


function getLatestAmendmentYear(
  amendments
) {
  if (!amendments?.length) {
    return "—";
  }

  const years = amendments
    .map(
      (item) =>
        Number(item.amendment_year)
    )
    .filter(
      (year) =>
        Number.isFinite(year) &&
        year > 0
    );

  if (!years.length) {
    return "—";
  }

  return Math.max(...years);
}


function getRelationshipInitial(
  relationshipType
) {
  const value = String(
    relationshipType || ""
  ).toUpperCase();

  if (value.includes("TEST")) {
    return "T";
  }

  if (value.includes("MATERIAL")) {
    return "M";
  }

  if (value.includes("CONFORMITY")) {
    return "C";
  }

  return "R";
}


export default App;