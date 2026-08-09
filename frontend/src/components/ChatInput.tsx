import React, { useState, useRef, useEffect } from 'react';
import { ArrowUp, MapPin, Mic, Sparkles } from 'lucide-react';

interface ChatInputProps {
  onSubmit: (message: string, context?: Record<string, any>) => void;
  isLoading: boolean;
  placeholder?: string;
  country?: string;
  state?: string;
  onJurisdictionChange?: (country: string, state: string) => void;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSubmit,
  isLoading,
  placeholder = "Message Sahay... (e.g. 'I lost my job and need help supporting my children')",
  country: initialCountry = 'IN',
  state: initialState = 'Bihar',
  onJurisdictionChange,
}) => {
  const [message, setMessage] = useState('');
  const [country, setCountry] = useState(initialCountry);
  const [state, setState] = useState(initialState);
  const [isVoiceSim, setIsVoiceSim] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`;
    }
  }, [message]);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!message.trim() || isLoading) return;
    const ctx: Record<string, any> = { country };
    if (country === 'IN' && state) ctx.state = state;
    onSubmit(message.trim(), ctx);
    setMessage('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleCountrySelect = (c: string) => {
    setCountry(c);
    if (onJurisdictionChange) onJurisdictionChange(c, state);
  };

  const handleStateSelect = (s: string) => {
    setState(s);
    if (onJurisdictionChange) onJurisdictionChange(country, s);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto">
      <div className="bg-[#0D1422] p-3.5 sm:p-4 rounded-3xl border border-slate-800 focus-within:border-sky-500/60 input-glow transition-all space-y-3">
        
        {/* Top Control Bar (Jurisdiction Context & Voice Simulation) */}
        <div className="flex flex-wrap items-center justify-between gap-2 pb-2.5 border-b border-slate-800/80 px-1 text-xs">
          <div className="flex items-center gap-2 text-slate-300 font-bold">
            <MapPin className="w-3.5 h-3.5 text-sky-400" />
            <span className="text-[11px] uppercase tracking-wider text-slate-400">Jurisdiction Context:</span>
            
            <select
              value={country}
              onChange={(e) => handleCountrySelect(e.target.value)}
              className="bg-[#121B2B] text-white text-xs font-bold px-2.5 py-1 rounded-xl border border-slate-700 focus:outline-none focus:border-sky-500 cursor-pointer"
            >
              <option value="IN">🇮🇳 India</option>
              <option value="US">🇺🇸 United States</option>
            </select>

            {country === 'IN' && (
              <select
                value={state}
                onChange={(e) => handleStateSelect(e.target.value)}
                className="bg-[#121B2B] text-white text-xs font-bold px-2.5 py-1 rounded-xl border border-slate-700 focus:outline-none focus:border-sky-500 cursor-pointer"
              >
                <option value="Bihar">Bihar</option>
                <option value="Delhi">Delhi</option>
                <option value="National">National (All States)</option>
              </select>
            )}
          </div>

          <button
            type="button"
            onClick={() => {
              setIsVoiceSim(!isVoiceSim);
              if (!isVoiceSim) {
                setMessage('My house was damaged by flooding in Bihar and we have nowhere to stay tonight.');
              }
            }}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-[11px] font-bold border transition-all cursor-pointer ${
              isVoiceSim
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 animate-pulse'
                : 'bg-[#121B2B] text-slate-400 border-slate-700 hover:text-slate-200'
            }`}
          >
            <Mic className="w-3 h-3 text-amber-400" />
            <span>{isVoiceSim ? 'Voice Simulated' : 'Voice Input'}</span>
          </button>
        </div>

        {/* Textarea */}
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          rows={2}
          className="w-full bg-transparent text-white placeholder-slate-400 text-sm sm:text-base px-1 focus:outline-none resize-none leading-relaxed"
        />

        {/* Footer & Send Button */}
        <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 px-1 text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <span className="hidden sm:inline text-[11px]">Press <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px]">Enter ↵</kbd> to send</span>
          </div>

          <button
            type="submit"
            disabled={!message.trim() || isLoading}
            className="p-2.5 sm:px-4 sm:py-2 bg-gradient-to-r from-sky-500 via-indigo-600 to-emerald-500 hover:from-sky-400 hover:to-emerald-400 disabled:opacity-30 text-white rounded-2xl text-xs font-black flex items-center gap-2 shadow-lg shadow-sky-500/20 transition-all cursor-pointer hover:scale-[1.03]"
          >
            {isLoading ? (
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>
                <span className="hidden sm:inline">Send</span>
                <ArrowUp className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>
    </form>
  );
};
