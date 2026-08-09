import React, { useState, useEffect } from 'react';
import { X, Cpu, ShieldCheck, Plus, CheckCircle } from 'lucide-react';
import { ToolDefinition, TTEProposal } from '../types';
import { fetchTools, proposeTTETool, approveTTETool } from '../services/api';

interface ToolRegistryModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ToolRegistryModal: React.FC<ToolRegistryModalProps> = ({ isOpen, onClose }) => {
  const [tools, setTools] = useState<ToolDefinition[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Proposal form state
  const [toolName, setToolName] = useState('');
  const [context, setContext] = useState('');
  const [code, setCode] = useState('');
  const [activeProposal, setActiveProposal] = useState<TTEProposal | null>(null);
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);

  const loadTools = async () => {
    try {
      setLoading(true);
      const data = await fetchTools();
      setTools(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load tool registry');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadTools();
    }
  }, [isOpen]);

  const handlePropose = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!toolName || !context || !code) return;
    try {
      setError(null);
      const prop = await proposeTTETool(toolName, context, code);
      setActiveProposal(prop);
      setActionSuccess('TTE Proposal submitted and static analysis evaluated.');
    } catch (err: any) {
      setError(err.message || 'Proposal failed');
    }
  };

  const handleApprove = async (proposalId: string) => {
    try {
      setError(null);
      await approveTTETool(proposalId);
      setActionSuccess('Proposal approved and registered in Tool Registry!');
      setActiveProposal(null);
      await loadTools();
    } catch (err: any) {
      setError(err.message || 'Approval failed');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
      <div className="glass-panel w-full max-w-4xl max-h-[90vh] overflow-hidden rounded-2xl border border-slate-800 flex flex-col shadow-2xl">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <Cpu className="w-5 h-5 text-sky-400" />
            <h3 className="text-lg font-bold text-white">Tool Registry & Controlled TTE Inspector</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1">
          {error && (
            <div className="p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs">
              {error}
            </div>
          )}

          {actionSuccess && (
            <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
              <CheckCircle className="w-4 h-4 flex-shrink-0" />
              <span>{actionSuccess}</span>
            </div>
          )}

          {/* Active Tool Registry List */}
          <div>
            <h4 className="text-sm font-bold text-slate-200 mb-3 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Active Registered Tools ({tools.length})</span>
            </h4>

            {loading ? (
              <p className="text-xs text-slate-400">Loading tools...</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {tools.map((t) => (
                  <div key={`${t.name}-${t.version}`} className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-bold text-white">{t.name} <span className="text-xs font-normal text-slate-400">v{t.version}</span></span>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        {t.status}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300">{t.description}</p>
                    <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800">
                      <span>Reliability: {(t.reliability_score * 100).toFixed(0)}%</span>
                      <span>By: {t.approved_by || 'SYSTEM'}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* TTE Tool Gap Proposal Form */}
          <div className="pt-6 border-t border-slate-800">
            <h4 className="text-sm font-bold text-slate-200 mb-3 flex items-center gap-2">
              <Plus className="w-4 h-4 text-sky-400" />
              <span>Propose New Tool Capability (Controlled TTE Sandbox)</span>
            </h4>

            <form onSubmit={handlePropose} className="space-y-3 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Tool Name</label>
                  <input
                    type="text"
                    value={toolName}
                    onChange={(e) => setToolName(e.target.value)}
                    placeholder="e.g. disaster_grant_calculator"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-400 mb-1">Problem Context</label>
                  <input
                    type="text"
                    value={context}
                    onChange={(e) => setContext(e.target.value)}
                    placeholder="e.g. Calculate max disaster grant ratio"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">Python Code Specification</label>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="def calculate_grant(damage, cap):&#10;    return min(damage, cap)"
                  rows={3}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-emerald-400 font-mono placeholder-slate-600 focus:outline-none focus:border-sky-500 resize-none"
                />
              </div>

              <button
                type="submit"
                className="px-4 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold transition-colors cursor-pointer"
              >
                Submit TTE Proposal
              </button>
            </form>

            {activeProposal && (
              <div className="mt-4 p-4 rounded-xl bg-slate-900 border border-slate-700 space-y-3">
                <div className="flex items-center justify-between">
                  <h5 className="text-xs font-bold text-white">Proposal Evaluation: {activeProposal.proposal_id}</h5>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-sky-500/20 text-sky-300">
                    Status: {activeProposal.status}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className={`p-2 rounded border ${activeProposal.static_analysis_passed ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-red-500/10 border-red-500/30 text-red-400'}`}>
                    AST Check: {activeProposal.static_analysis_passed ? 'PASSED' : 'FAILED'}
                  </div>
                  <div className={`p-2 rounded border ${activeProposal.security_audit_passed ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' : 'bg-red-500/10 border-red-500/30 text-red-400'}`}>
                    Security Audit: {activeProposal.security_audit_passed ? 'PASSED' : 'FAILED'}
                  </div>
                </div>

                {activeProposal.static_analysis_passed && activeProposal.security_audit_passed && (
                  <button
                    onClick={() => handleApprove(activeProposal.proposal_id)}
                    className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition-colors cursor-pointer"
                  >
                    Approve & Register Tool to Registry
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
