import React, { useState } from 'react';
import { SahayResponse, EligibilityStatus } from '../types';
import { ShieldAlert, Building, CheckCircle2, FileText, ExternalLink, HelpCircle, ArrowLeft, Clock, MapPin, Sliders, Search, XCircle, Check } from 'lucide-react';
import { sendChatQuery } from '../services/api';

interface StructuredResponseViewProps {
  data: SahayResponse;
  onNewRequest: () => void;
}

export const StructuredResponseView: React.FC<StructuredResponseViewProps> = ({ data: initialData, onNewRequest }) => {
  const [data, setData] = useState<SahayResponse>(initialData);
  const [viewMode, setViewMode] = useState<'CITIZEN' | 'INSPECTOR'>('CITIZEN');
  const [checkedDocs, setCheckedDocs] = useState<Record<string, boolean>>({});
  const [isReevaluating, setIsReevaluating] = useState(false);

  // Editable Facts state for live re-evaluation
  const [facts, setFacts] = useState<Record<string, any>>(data.situation.extracted_facts);

  const isCrisis = data.urgency.level === 'CRISIS';

  // Extract Jurisdiction string
  const extractedCountry = facts.country || data.situation.extracted_facts.country || 'IN';
  const extractedState = facts.state || data.situation.extracted_facts.state;
  const jurisdictionLabel = extractedCountry === 'IN'
    ? (extractedState ? `India · ${extractedState}` : 'India · National')
    : (extractedCountry === 'US' ? 'United States · Federal' : 'Location needed');

  const toggleDocCheck = (name: string) => {
    setCheckedDocs((prev) => ({ ...prev, [name]: !prev[name] }));
  };

  const handleReevaluate = async (updatedFacts: Record<string, any>) => {
    try {
      setIsReevaluating(true);
      const queryMessage = `Re-evaluating eligibility based on updated user facts: ${JSON.stringify(updatedFacts)}`;
      const res = await sendChatQuery(queryMessage, updatedFacts);
      setData(res);
      setFacts(updatedFacts);
    } catch (e) {
      // Keep existing data on error
    } finally {
      setIsReevaluating(false);
    }
  };

  const totalMandatoryDocs = data.documents.filter((d) => d.is_mandatory).length;
  const readyMandatoryDocs = data.documents.filter((d) => d.is_mandatory && checkedDocs[d.document_name]).length;

  const getEligibilityBadge = (status: EligibilityStatus) => {
    switch (status) {
      case 'LIKELY_ELIGIBLE':
        return <span className="px-3.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-black tracking-wide">LIKELY ELIGIBLE</span>;
      case 'POTENTIALLY_ELIGIBLE':
        return <span className="px-3.5 py-1 rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/40 text-xs font-black tracking-wide">POTENTIALLY ELIGIBLE</span>;
      case 'INELIGIBLE':
        return <span className="px-3.5 py-1 rounded-lg bg-rose-500/20 text-rose-300 border border-rose-500/40 text-xs font-black tracking-wide">INELIGIBLE</span>;
      default:
        return <span className="px-3.5 py-1 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/40 text-xs font-black tracking-wide">UNCERTAIN / INFO REQUIRED</span>;
    }
  };

  return (
    <div className="w-full max-w-5xl mx-auto space-y-6 pb-24 px-4 sm:px-6 pt-4">
      {/* Top Controls Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 py-3 border-b border-slate-800">
        <button
          onClick={onNewRequest}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 text-xs font-bold transition-all cursor-pointer shadow-sm hover:scale-[1.02]"
        >
          <ArrowLeft className="w-4 h-4 text-sky-400" />
          <span>New Query</span>
        </button>

        {/* View Mode Toggle Switch */}
        <div className="flex items-center bg-slate-900 p-1.5 rounded-xl border border-slate-700 text-xs font-bold shadow-inner">
          <button
            onClick={() => setViewMode('CITIZEN')}
            className={`px-4 py-1.5 rounded-lg transition-all cursor-pointer ${
              viewMode === 'CITIZEN' ? 'bg-sky-500 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            👤 Citizen Guidance
          </button>
          <button
            onClick={() => setViewMode('INSPECTOR')}
            className={`px-4 py-1.5 rounded-lg transition-all cursor-pointer ${
              viewMode === 'INSPECTOR' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            🔍 RAG & Technical Inspector
          </button>
        </div>

        <div className="flex items-center gap-3 text-xs">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-200 font-bold">
            <MapPin className="w-3.5 h-3.5 text-sky-400" />
            <span>{jurisdictionLabel}</span>
          </div>

          <div
            className={`px-3 py-1.5 rounded-xl border font-black ${
              isCrisis
                ? 'bg-red-500/20 text-red-300 border-red-500/50 animate-pulse'
                : 'bg-sky-500/20 text-sky-300 border-sky-500/30'
            }`}
          >
            {isCrisis ? 'CRISIS MODE' : `${data.flow.replace('_', ' ')}`}
          </div>
        </div>
      </div>

      {/* 🚨 CRISIS SUPPORT BANNER */}
      {isCrisis && (
        <div className="p-6 rounded-2xl bg-red-950/40 border border-red-500/50 crisis-glow space-y-3">
          <div className="flex items-center gap-4">
            <div className="p-3.5 rounded-2xl bg-red-500/20 border border-red-500/40 text-red-400">
              <ShieldAlert className="w-8 h-8 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-black text-white">🚨 CRISIS SUPPORT — Immediate Action Required</h2>
                <span className="text-xs px-2.5 py-0.5 rounded bg-red-500/30 text-red-200 font-extrabold border border-red-500/40">
                  Priority 1 Active
                </span>
              </div>
              <p className="text-xs sm:text-sm text-red-200 mt-1 leading-relaxed">
                Your physical safety is the top priority. Seek high ground or immediate safe shelter and call local emergency services.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* 01. SITUATION ASSESSMENT */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <span className="text-xs uppercase tracking-widest text-sky-400 font-black">SITUATION ASSESSMENT</span>
            <h2 className="text-xl sm:text-2xl font-black text-white mt-1">{data.situation.summary}</h2>
          </div>
          <div className="text-right">
            <span className="text-xs text-slate-400 font-medium">Assessed Urgency Severity:</span>
            <div className="text-sm font-black text-amber-400">{data.urgency.level} ({ (data.urgency.score * 100).toFixed(0) }% severity)</div>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-3">
          <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">
            <span className="text-sky-400 font-bold">Urgency Reasoning: </span>
            {data.urgency.reasoning}
          </p>

          {/* Interactive Fact Refiner for Judges/Users */}
          <div className="pt-3 border-t border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-300 flex items-center gap-1.5">
                <Sliders className="w-4 h-4 text-sky-400" />
                Live Extracted Facts (Modify to Re-evaluate Engine):
              </span>
              {isReevaluating && <span className="text-xs text-sky-400 font-bold animate-pulse">Re-evaluating engine...</span>}
            </div>

            <div className="flex flex-wrap gap-2 pt-1">
              {Object.entries(facts).map(([key, val]) => (
                <div key={key} className="px-3 py-1 rounded-lg bg-slate-800 text-slate-200 text-xs border border-slate-700 flex items-center gap-1.5 font-medium">
                  <span className="text-slate-400 font-semibold">{key}:</span>
                  <span className="text-white font-bold">{String(val)}</span>
                </div>
              ))}

              {/* Quick Fact Presets */}
              <button
                onClick={() => handleReevaluate({ ...facts, state: 'Bihar', annual_income: 120000 })}
                className="px-3 py-1 rounded-lg bg-sky-500/20 hover:bg-sky-500/30 text-sky-300 border border-sky-500/40 text-xs font-bold transition-all cursor-pointer shadow-sm"
              >
                + Add Low Income Bihar Fact
              </button>
            </div>
          </div>
        </div>

        {/* Missing Information Prompt Callout */}
        {data.missing_information.length > 0 && (
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs sm:text-sm space-y-2">
            <div className="flex items-center gap-2 font-bold text-amber-400">
              <HelpCircle className="w-4 h-4" />
              <span>Additional Information Needed for Higher Eligibility Precision:</span>
            </div>
            <ul className="list-disc list-inside space-y-1 pl-1 text-slate-300">
              {data.missing_information.map((item, idx) => (
                <li key={idx}>
                  <span className="font-bold text-amber-300">{item.field}:</span> {item.question}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* VIEW MODE 1: CITIZEN GUIDANCE VIEW */}
      {viewMode === 'CITIZEN' ? (
        <>
          {/* 02. NEXT BEST ACTION (Action Plan) */}
          <div className="glass-panel p-6 rounded-2xl space-y-5">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-purple-500/20 text-purple-400 border border-purple-500/30">
                <Clock className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-black text-white">Next Best Action</h3>
                <p className="text-xs text-slate-400">Prioritized step-by-step guidance</p>
              </div>
            </div>

            <div className="space-y-4 relative before:absolute before:inset-0 before:left-3.5 before:w-0.5 before:bg-slate-800">
              {data.action_plan.map((step) => (
                <div key={step.step_number} className="relative flex items-start gap-4 pl-9">
                  <div className="absolute left-0 w-7 h-7 rounded-full bg-gradient-to-tr from-indigo-500 to-sky-400 text-white font-black text-xs flex items-center justify-center border-2 border-[#0B0F19] shadow-md">
                    {step.step_number}
                  </div>
                  <div className="p-4 sm:p-5 rounded-2xl bg-slate-900/90 border border-slate-800 flex-1 space-y-1.5 hover:border-sky-500/40 transition-colors">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <h4 className="text-sm sm:text-base font-bold text-white">{step.title}</h4>
                      {step.estimated_time && (
                        <span className="text-xs text-sky-300 bg-sky-950/60 px-3 py-1 rounded-lg font-mono font-bold border border-sky-500/30">
                          ⏱ {step.estimated_time}
                        </span>
                      )}
                    </div>
                    <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">{step.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 03. APPLICABLE PUBLIC SERVICES & EMERGENCY RESOURCES */}
          <div className="glass-panel p-6 rounded-2xl space-y-5">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-sky-500/20 text-sky-400 border border-sky-500/30">
                <Building className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-black text-white">
                  {isCrisis ? 'Emergency Resources & Disaster Relief Programs' : 'Potentially Applicable Public Services'}
                </h3>
                <p className="text-xs text-slate-400">Verified government programs matching your query</p>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-4">
              {data.recommendations.map((rec) => (
                <div key={rec.scheme_id} className="glass-card p-5 rounded-2xl space-y-2 border-slate-800">
                  <div className="flex flex-wrap items-start justify-between gap-2">
                    <div>
                      <h4 className="text-base sm:text-lg font-extrabold text-white">{rec.title}</h4>
                      <p className="text-xs text-sky-400 font-bold mt-0.5">
                        {rec.issuing_authority} • {rec.category}
                      </p>
                    </div>
                    <span className="text-xs font-black px-3 py-1 rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/30">
                      {rec.match_confidence} Confidence
                    </span>
                  </div>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">{rec.summary}</p>
                </div>
              ))}
            </div>
          </div>

          {/* 04. DETERMINISTIC ELIGIBILITY ENGINE ASSESSMENT */}
          <div className="glass-panel p-6 rounded-2xl space-y-5">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                <CheckCircle2 className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-black text-white">Deterministic Eligibility Assessment</h3>
                <p className="text-xs text-slate-400">Evaluated against structured legal rules without hallucinated claims</p>
              </div>
            </div>

            <div className="space-y-4">
              {data.eligibility.map((el, idx) => (
                <div key={idx} className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="text-xs font-mono font-bold text-slate-400">Scheme ID: {el.scheme_id}</span>
                    {getEligibilityBadge(el.status)}
                  </div>
                  <p className="text-xs sm:text-sm text-slate-200 leading-relaxed font-medium">{el.reasoning}</p>

                  {/* Satisfied Criteria */}
                  {el.matching_criteria.length > 0 && (
                    <div className="text-xs sm:text-sm space-y-1.5 pt-1">
                      <span className="font-extrabold text-emerald-400 flex items-center gap-1.5">
                        <Check className="w-4 h-4 text-emerald-400" />
                        Satisfied Criteria:
                      </span>
                      <ul className="space-y-1 pl-4 text-slate-200">
                        {el.matching_criteria.map((c, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <span className="text-emerald-400 font-bold">✓</span>
                            <span>{c}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Unmet Criteria */}
                  {el.unmet_criteria.length > 0 && (
                    <div className="text-xs sm:text-sm space-y-1.5 pt-1">
                      <span className="font-extrabold text-rose-300 flex items-center gap-1.5">
                        <XCircle className="w-4 h-4 text-rose-400" />
                        Unmet / Missing Criteria:
                      </span>
                      <ul className="space-y-1 pl-4 text-slate-200">
                        {el.unmet_criteria.map((uc, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <span className="text-rose-400 font-bold">✕</span>
                            <span className="text-slate-300">{uc}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
            <p className="text-[11px] text-slate-400 italic text-center pt-1">
              Informational assessment based on user facts. Does not make false claims of official legal entitlement.
            </p>
          </div>

          {/* 05. INTERACTIVE DOCUMENT READINESS TRACKER */}
          <div className="glass-panel p-6 rounded-2xl space-y-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-xl bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-black text-white">Document Readiness Tracker</h3>
                  <p className="text-xs text-slate-400">Mark documents you already possess to track readiness</p>
                </div>
              </div>

              {totalMandatoryDocs > 0 && (
                <div className="px-4 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-xs font-black text-indigo-300">
                  Mandatory Readiness: {readyMandatoryDocs} / {totalMandatoryDocs} Complete
                </div>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {data.documents.map((doc, idx) => {
                const isChecked = !!checkedDocs[doc.document_name];
                return (
                  <div
                    key={idx}
                    onClick={() => toggleDocCheck(doc.document_name)}
                    className={`p-4 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between space-y-3 ${
                      isChecked
                        ? 'bg-emerald-950/30 border-emerald-500/50 shadow-md'
                        : 'bg-slate-900/90 border-slate-800 hover:border-indigo-500/40'
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-1.5">
                        <div className="flex items-center gap-2.5">
                          <input
                            type="checkbox"
                            checked={isChecked}
                            onChange={() => {}}
                            className="w-4 h-4 rounded text-emerald-500 focus:ring-0 cursor-pointer"
                          />
                          <h4 className={`text-xs sm:text-sm font-bold ${isChecked ? 'text-emerald-300 line-through' : 'text-white'}`}>
                            {doc.document_name}
                          </h4>
                        </div>
                        {doc.is_mandatory && (
                          <span className="text-[10px] uppercase font-black px-2.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/40">
                            Mandatory
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-slate-300"><span className="text-slate-400 font-semibold">Purpose:</span> {doc.purpose}</p>
                    </div>
                    <div className="pt-2 border-t border-slate-800 text-xs text-indigo-300 font-medium">
                      <span className="font-semibold text-slate-400">How to acquire:</span> {doc.how_to_obtain}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* 06. VERIFIED PUBLIC SOURCES */}
          <div className="glass-panel p-6 rounded-2xl space-y-5">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-teal-500/20 text-teal-400 border border-teal-500/30">
                <ExternalLink className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-black text-white">Verified Public Sources & Official Portals</h3>
                <p className="text-xs text-slate-400">Direct citations to official issuing authorities</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {data.sources.map((src, idx) => (
                <a
                  key={idx}
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-teal-500/40 text-left block transition-all group shadow-sm hover:scale-[1.01]"
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs sm:text-sm font-bold text-white group-hover:text-teal-300 transition-colors flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                      {src.title}
                    </span>
                    <ExternalLink className="w-4 h-4 text-slate-500 group-hover:text-teal-400 transition-colors" />
                  </div>
                  <p className="text-xs text-slate-400">
                    Issued by: <span className="text-slate-200 font-semibold">{src.issuing_authority}</span>
                  </p>
                </a>
              ))}
            </div>
          </div>
        </>
      ) : (
        /* VIEW MODE 2: RAG & TECHNICAL INSPECTOR VIEW FOR HACKATHON JUDGES */
        <div className="glass-panel p-6 rounded-2xl space-y-6">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
              <Search className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-black text-white">RAG Evidence & Vector Retrieval Inspector</h3>
              <p className="text-xs text-slate-400">Inspect semantic similarity scores, section chunking, and source traceability</p>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {data.evidence && data.evidence.length > 0 ? (
              data.evidence.map((ev, idx) => (
                <div key={idx} className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono font-bold text-sky-400">{ev.chunk_id}</span>
                      <span className="text-xs px-2.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-bold">
                        {ev.section_type}
                      </span>
                    </div>
                    <span className="text-xs font-mono font-black px-3 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                      Similarity Score: { (ev.similarity_score * 100).toFixed(1) }%
                    </span>
                  </div>

                  <p className="text-xs sm:text-sm text-slate-200 font-mono leading-relaxed bg-slate-950 p-4 rounded-xl border border-slate-800">
                    "{ev.content}"
                  </p>

                  <div className="flex flex-wrap items-center justify-between text-xs text-slate-400 pt-1">
                    <span>Scheme ID: <strong className="text-white">{ev.scheme_id}</strong> ({ev.title})</span>
                    <span>Source: <a href={ev.source_url} target="_blank" rel="noopener noreferrer" className="text-sky-400 hover:underline font-bold">{ev.source_url}</a></span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-400">No RAG evidence chunks returned for this query.</p>
            )}
          </div>
        </div>
      )}

      {/* Legal Disclaimer */}
      <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 text-center text-xs text-slate-400">
        <p>{data.disclaimer}</p>
      </div>
    </div>
  );
};
