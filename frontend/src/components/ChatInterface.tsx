import React, { useState } from 'react';
import { SahayResponse, EligibilityStatus } from '../types';
import { ShieldAlert, Building, CheckCircle2, FileText, ExternalLink, HelpCircle, ArrowLeft, Clock, MapPin, Sliders, Search, XCircle, Check, ChevronDown, ChevronUp, LifeBuoy, User, Globe, Home, Flame, DollarSign, CloudRain } from 'lucide-react';
import { ChatInput } from './ChatInput';

export interface ChatMessage {
  id: string;
  sender: 'USER' | 'SAHAY';
  text: string;
  responseObject?: SahayResponse;
  timestamp: string;
}

interface ChatInterfaceProps {
  messages: ChatMessage[];
  onSendMessage: (message: string, context?: Record<string, any>) => void;
  isLoading: boolean;
  onResetConversation: () => void;
  onOpenTools: () => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  onSendMessage,
  isLoading,
  onResetConversation,
  onOpenTools,
}) => {
  const [expandedSources, setExpandedSources] = useState<Record<string, boolean>>({});
  const [expandedEligibility, setExpandedEligibility] = useState<Record<string, boolean>>({});
  const [checkedDocs, setCheckedDocs] = useState<Record<string, boolean>>({});

  const toggleSourceExpand = (id: string) => {
    setExpandedSources((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const toggleEligibilityExpand = (id: string) => {
    setExpandedEligibility((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const toggleDocCheck = (name: string) => {
    setCheckedDocs((prev) => ({ ...prev, [name]: !prev[name] }));
  };

  const getEligibilityBadge = (status: EligibilityStatus) => {
    switch (status) {
      case 'LIKELY_ELIGIBLE':
        return <span className="px-3 py-1 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-black">LIKELY ELIGIBLE</span>;
      case 'POTENTIALLY_ELIGIBLE':
        return <span className="px-3 py-1 rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/40 text-xs font-black">POTENTIALLY ELIGIBLE</span>;
      case 'INELIGIBLE':
        return <span className="px-3 py-1 rounded-lg bg-rose-500/20 text-rose-300 border border-rose-500/40 text-xs font-black">INELIGIBLE</span>;
      default:
        return <span className="px-3 py-1 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/40 text-xs font-black">INFO REQUIRED</span>;
    }
  };

  const ambiguousChips = [
    { label: '🏠 Housing Assistance (PMAY)', text: 'I am looking for PMAY government housing assistance.' },
    { label: '🌧️ Disaster Flood Damage', text: 'My house was damaged by flooding and I need shelter relief.' },
    { label: '💰 Financial & Housing Costs', text: 'I need financial assistance to pay housing and living costs.' },
    { label: '📄 Documents & Application', text: 'What documents are required to apply for housing support?' },
  ];

  const biharCities = ['Patna', 'Gaya', 'Supaul', 'Muzaffarpur', 'Bhagalpur'];

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6 pb-32 px-4 sm:px-6 pt-4">
      {/* Top Thread Bar */}
      <div className="flex items-center justify-between py-3 border-b border-slate-800 text-xs">
        <button
          onClick={onResetConversation}
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-[#0D1422] hover:bg-slate-800 text-slate-300 border border-slate-700 font-bold transition-all cursor-pointer shadow-sm"
        >
          <ArrowLeft className="w-4 h-4 text-sky-400" />
          <span>New Conversation</span>
        </button>

        <div className="flex items-center gap-2 text-slate-400 font-semibold">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span>Conversational Workspace Active</span>
        </div>
      </div>

      {/* Messages Thread */}
      <div className="space-y-6">
        {messages.map((msg) => {
          const isSahay = msg.sender === 'SAHAY';
          const resp = msg.responseObject;
          const isCrisis = resp?.urgency?.level === 'CRISIS';
          const isAmbiguous = resp?.flow === 'AMBIGUOUS';
          const isWebSearch = resp?.flow === 'WEB_SEARCH_REQUIRED';
          const isGeneral = resp?.flow === 'GENERAL_INFORMATION';
          const weatherData = resp?.situation?.weather_data;

          return (
            <div key={msg.id} className="space-y-4">
              {/* Message Bubble Container */}
              <div className={`flex items-start gap-3 sm:gap-4 ${isSahay ? '' : 'flex-row-reverse'}`}>
                
                {/* Avatar */}
                <div
                  className={`w-9 h-9 rounded-2xl flex items-center justify-center flex-shrink-0 border shadow-md ${
                    isSahay
                      ? 'bg-gradient-to-tr from-sky-500 to-indigo-600 border-sky-400/40 text-white'
                      : 'bg-slate-800 border-slate-700 text-slate-200'
                  }`}
                >
                  {isSahay ? <LifeBuoy className="w-5 h-5" /> : <User className="w-5 h-5" />}
                </div>

                {/* Message Content Body */}
                <div className={`flex-1 space-y-3 ${isSahay ? '' : 'text-right'}`}>
                  
                  {/* Sender Name & Time */}
                  <div className={`flex items-center gap-2 text-xs text-slate-400 ${isSahay ? '' : 'justify-end'}`}>
                    <span className="font-bold text-white">{isSahay ? 'Sahay Assistant' : 'You'}</span>
                    {isWebSearch && (
                      <span className="px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30 text-[10px] font-bold flex items-center gap-1">
                        <Globe className="w-3 h-3 text-sky-400" /> Web Search
                      </span>
                    )}
                    <span>•</span>
                    <span>{msg.timestamp}</span>
                  </div>

                  {/* Text Content */}
                  <div
                    className={`p-4 sm:p-5 rounded-2xl text-sm leading-relaxed ${
                      isSahay
                        ? 'bg-[#0D1422] border border-slate-800 text-slate-200 shadow-sm'
                        : 'bg-gradient-to-r from-sky-600 to-indigo-600 text-white font-medium shadow-md ml-auto max-w-xl text-left'
                    }`}
                  >
                    <p className="whitespace-pre-line">{msg.text}</p>
                  </div>

                  {/* 🌧️ COMPACT WEATHER CARD (Open-Meteo API) */}
                  {isSahay && weatherData && (
                    <div className="p-5 rounded-2xl bg-[#121B2B] border border-sky-500/30 input-glow space-y-3 text-left">
                      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                        <span className="text-xs font-black text-sky-300 uppercase tracking-wider flex items-center gap-1.5">
                          <CloudRain className="w-4 h-4 text-sky-400" />
                          {weatherData.time_period
                            ? `${weatherData.time_period.charAt(0).toUpperCase() + weatherData.time_period.slice(1)} Forecast`
                            : 'Daily Forecast'}{' '}
                          · {weatherData.city}, {weatherData.admin_region}
                        </span>
                        <span className="text-[10px] font-mono text-slate-400">
                          {weatherData.updated_at}
                        </span>
                      </div>

                      <div className="flex items-baseline justify-between">
                        <div>
                          <div className="text-3xl font-black text-white">
                            {weatherData.temp_min}° — {weatherData.temp_max}°C
                          </div>
                          <p className="text-xs text-sky-200 font-bold mt-1">
                            {weatherData.condition}
                          </p>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-3 pt-2 text-xs border-t border-slate-800/80">
                        <div className="flex items-center gap-2 text-slate-300">
                          <span className="text-sky-400 font-bold">💧 Rain Probability:</span>
                          <span className="font-mono text-white font-bold">{weatherData.rain_probability}%</span>
                        </div>
                        <div className="flex items-center gap-2 text-slate-300">
                          <span className="text-sky-400 font-bold">💨 Wind:</span>
                          <span className="font-mono text-white font-bold">{weatherData.wind_speed} km/h</span>
                        </div>
                      </div>

                      <div className="pt-2 flex items-center justify-between text-[11px] text-slate-400 border-t border-slate-800/50">
                        <span>Timezone: {weatherData.timezone}</span>
                        <span className="font-bold text-sky-400">Source: Open-Meteo Weather Forecast</span>
                      </div>
                    </div>
                  )}

                  {/* 📍 City Choice Chips for Weather (When city is missing) */}
                  {isSahay && resp?.missing_information?.some((m) => m.field === 'city') && (
                    <div className="pt-2 text-left space-y-2">
                      <span className="text-xs font-bold text-slate-400 block">Select a city in Bihar:</span>
                      <div className="flex flex-wrap gap-2">
                        {biharCities.map((cityName) => (
                          <button
                            key={cityName}
                            onClick={() => onSendMessage(`Will it rain tomorrow in ${cityName}?`)}
                            className="px-3.5 py-1.5 rounded-xl bg-[#121B2B] hover:bg-slate-800 border border-slate-700 hover:border-sky-500/50 text-xs text-white font-bold transition-all cursor-pointer flex items-center gap-1.5"
                          >
                            <span>📍</span>
                            <span>{cityName}</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 🚨 CRISIS SUPPORT BANNER (If Crisis Flow) */}
                  {isSahay && isCrisis && (
                    <div className="p-5 rounded-2xl bg-red-950/40 border border-red-500/50 crisis-glow space-y-2 text-left">
                      <div className="flex items-center gap-3">
                        <ShieldAlert className="w-6 h-6 text-red-400 animate-pulse flex-shrink-0" />
                        <div>
                          <h4 className="text-sm font-black text-white">🚨 CRISIS SUPPORT — Immediate Safety First</h4>
                          <p className="text-xs text-red-200 mt-0.5">
                            Seek immediate high ground or safe shelter. Contact local emergency authorities if structure is compromised.
                          </p>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Ambiguous Choice Chips (Only for Housing/Public Service Ambiguity) */}
                  {isSahay && isAmbiguous && (resp?.situation?.primary_intent === 'HOUSING' || resp?.situation?.primary_intent === 'PUBLIC_SERVICE_AMBIGUOUS') && (
                    <div className="pt-2 text-left space-y-2">
                      <span className="text-xs font-bold text-slate-400 block">Select your specific requirement:</span>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {ambiguousChips.map((chip, idx) => (
                          <button
                            key={idx}
                            onClick={() => onSendMessage(chip.text)}
                            className="p-3 rounded-xl bg-[#121B2B] hover:bg-slate-800 border border-slate-700 text-xs text-white font-bold transition-all text-left flex items-center justify-between cursor-pointer group"
                          >
                            <span>{chip.label}</span>
                            <span className="text-sky-400 group-hover:translate-x-0.5 transition-transform">→</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Clarification Questions Callout */}
                  {isSahay && resp && !isAmbiguous && !weatherData && resp.missing_information.length > 0 && (
                    <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs space-y-2 text-left">
                      <div className="flex items-center gap-2 font-bold text-amber-400">
                        <HelpCircle className="w-4 h-4" />
                        <span>A few details will help narrow this down precisely:</span>
                      </div>
                      <ul className="list-disc list-inside space-y-1 pl-1 text-slate-300">
                        {resp.missing_information.map((item, idx) => (
                          <li key={idx}>
                            <span className="font-bold text-amber-300">{item.field}:</span> {item.question}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Web Sources for WebSearch / General Info (Except when Weather Card is active) */}
                  {isSahay && resp && (isWebSearch || isGeneral) && !weatherData && resp.sources.length > 0 && (
                    <div className="pt-2 text-left space-y-2">
                      <span className="text-xs font-bold text-slate-400 block">Verified Web Citations:</span>
                      {resp.sources.map((src, idx) => (
                        <a
                          key={idx}
                          href={src.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="p-3 rounded-xl bg-[#121B2B] border border-slate-800 hover:border-sky-500/40 flex items-center justify-between text-xs group"
                        >
                          <div className="flex items-center gap-2">
                            <Globe className="w-4 h-4 text-sky-400" />
                            <span className="font-bold text-white group-hover:text-sky-300 transition-colors">
                              {src.title}
                            </span>
                          </div>
                          <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-sky-400 transition-colors" />
                        </a>
                      ))}
                    </div>
                  )}

                  {/* Rich Inline Cards for Public Service / Crisis / Eligibility Responses */}
                  {isSahay && resp && !isWebSearch && !isGeneral && !isAmbiguous && (
                    <div className="space-y-4 text-left pt-2">
                      
                      {/* 1. Next Best Actions (Prioritized Steps) */}
                      {resp.action_plan.length > 0 && (
                        <div className="p-4 rounded-2xl bg-[#121B2B] border border-slate-800 space-y-3">
                          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                            <span className="text-xs font-black text-sky-400 uppercase tracking-wider flex items-center gap-1.5">
                              <Clock className="w-4 h-4" /> Next Best Action Plan
                            </span>
                          </div>
                          <div className="space-y-2.5">
                            {resp.action_plan.map((step) => (
                              <div key={step.step_number} className="flex items-start gap-3 p-3 rounded-xl bg-[#0D1422] border border-slate-800 text-xs">
                                <div className="w-6 h-6 rounded-full bg-sky-500/20 text-sky-300 border border-sky-500/40 font-black text-xs flex items-center justify-center flex-shrink-0">
                                  {step.step_number}
                                </div>
                                <div className="flex-1">
                                  <div className="flex items-center justify-between font-bold text-white mb-0.5">
                                    <span>{step.title}</span>
                                    {step.estimated_time && (
                                      <span className="text-[10px] text-sky-400 font-mono">⏱ {step.estimated_time}</span>
                                    )}
                                  </div>
                                  <p className="text-slate-300 text-[11px] leading-relaxed">{step.description}</p>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* 2. Recommended Programs & Official Sources */}
                      {resp.recommendations.length > 0 && (
                        <div className="p-4 rounded-2xl bg-[#121B2B] border border-slate-800 space-y-3">
                          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                            <span className="text-xs font-black text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                              <Building className="w-4 h-4" /> Verified Programs ({resp.recommendations.length})
                            </span>
                            
                            <button
                              onClick={() => toggleSourceExpand(msg.id)}
                              className="text-xs text-slate-400 hover:text-white flex items-center gap-1 cursor-pointer"
                            >
                              <span>{expandedSources[msg.id] ? 'Hide Sources' : 'View Sources'}</span>
                              {expandedSources[msg.id] ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                            </button>
                          </div>

                          <div className="space-y-2.5">
                            {resp.recommendations.map((rec) => (
                              <div key={rec.scheme_id} className="p-3.5 rounded-xl bg-[#0D1422] border border-slate-800 space-y-1.5 text-xs">
                                <div className="flex flex-wrap items-center justify-between gap-2">
                                  <h5 className="font-bold text-white">{rec.title}</h5>
                                  <span className="text-[10px] font-extrabold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                                    {rec.match_confidence} Confidence
                                  </span>
                                </div>
                                <p className="text-slate-300 text-[11px] leading-relaxed">{rec.summary}</p>
                              </div>
                            ))}
                          </div>

                          {/* Expandable Official Sources List */}
                          {expandedSources[msg.id] && resp.sources.length > 0 && (
                            <div className="pt-2 border-t border-slate-800 space-y-2">
                              <span className="text-[11px] font-bold text-slate-400">Direct Official Citations:</span>
                              {resp.sources.map((src, idx) => (
                                <a
                                  key={idx}
                                  href={src.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="p-2.5 rounded-xl bg-[#0D1422] border border-slate-800 hover:border-teal-500/40 flex items-center justify-between text-xs group"
                                >
                                  <span className="font-bold text-white group-hover:text-teal-300 transition-colors flex items-center gap-2">
                                    <span className="w-2 h-2 rounded-full bg-emerald-400" />
                                    {src.title}
                                  </span>
                                  <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-teal-400 transition-colors" />
                                </a>
                              ))}
                            </div>
                          )}
                        </div>
                      )}

                      {/* 3. Deterministic Eligibility Breakdown */}
                      {resp.eligibility.length > 0 && (
                        <div className="p-4 rounded-2xl bg-[#121B2B] border border-slate-800 space-y-3">
                          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                            <span className="text-xs font-black text-indigo-400 uppercase tracking-wider flex items-center gap-1.5">
                              <CheckCircle2 className="w-4 h-4" /> Eligibility Criteria Assessment
                            </span>

                            <button
                              onClick={() => toggleEligibilityExpand(msg.id)}
                              className="text-xs text-slate-400 hover:text-white flex items-center gap-1 cursor-pointer"
                            >
                              <span>{expandedEligibility[msg.id] ? 'Hide Rules' : 'View Rules'}</span>
                              {expandedEligibility[msg.id] ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                            </button>
                          </div>

                          <div className="space-y-2">
                            {resp.eligibility.map((el, idx) => (
                              <div key={idx} className="p-3.5 rounded-xl bg-[#0D1422] border border-slate-800 space-y-2 text-xs">
                                <div className="flex items-center justify-between">
                                  <span className="font-mono text-slate-400 font-bold text-[11px]">Scheme ID: {el.scheme_id}</span>
                                  {getEligibilityBadge(el.status)}
                                </div>
                                <p className="text-slate-200 text-xs">{el.reasoning}</p>

                                {expandedEligibility[msg.id] && (
                                  <div className="pt-2 border-t border-slate-800 space-y-1.5 text-[11px]">
                                    {el.matching_criteria.length > 0 && (
                                      <div className="text-emerald-400">
                                        <span className="font-bold">✓ Satisfied Rules:</span> {el.matching_criteria.join(', ')}
                                      </div>
                                    )}
                                    {el.unmet_criteria.length > 0 && (
                                      <div className="text-rose-300">
                                        <span className="font-bold">✕ Unmet / Missing:</span> {el.unmet_criteria.join(', ')}
                                      </div>
                                    )}
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* 4. Document Readiness Tracker */}
                      {resp.documents.length > 0 && (
                        <div className="p-4 rounded-2xl bg-[#121B2B] border border-slate-800 space-y-3">
                          <span className="text-xs font-black text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                            <FileText className="w-4 h-4 text-indigo-400" /> Required Documents
                          </span>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {resp.documents.map((doc, idx) => {
                              const isChecked = !!checkedDocs[doc.document_name];
                              return (
                                <div
                                  key={idx}
                                  onClick={() => toggleDocCheck(doc.document_name)}
                                  className={`p-3 rounded-xl border transition-all cursor-pointer flex items-center justify-between text-xs ${
                                    isChecked
                                      ? 'bg-emerald-950/30 border-emerald-500/40'
                                      : 'bg-[#0D1422] border-slate-800 hover:border-indigo-500/30'
                                  }`}
                                >
                                  <div className="flex items-center gap-2">
                                    <input
                                      type="checkbox"
                                      checked={isChecked}
                                      onChange={() => {}}
                                      className="w-3.5 h-3.5 rounded text-emerald-500 focus:ring-0 cursor-pointer"
                                    />
                                    <span className={`font-bold ${isChecked ? 'text-emerald-300 line-through' : 'text-white'}`}>
                                      {doc.document_name}
                                    </span>
                                  </div>
                                  {doc.is_mandatory && (
                                    <span className="text-[9px] uppercase font-black px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
                                      Mandatory
                                    </span>
                                  )}
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Persistent Bottom Chat Input */}
      <div className="fixed bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-[#070B14] via-[#070B14]/90 to-transparent backdrop-blur-md z-30">
        <ChatInput onSubmit={onSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};
