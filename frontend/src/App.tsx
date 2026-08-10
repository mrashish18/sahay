import { useState } from 'react';
import { Header } from './components/Header';
import { JudgeScenariosBar } from './components/JudgeScenariosBar';
import { Hero } from './components/Hero';
import { ChatInterface, ChatMessage } from './components/ChatInterface';
import { TrustStrip } from './components/TrustStrip';
import { HowItWorks } from './components/HowItWorks';
import { TechnicalTrust } from './components/TechnicalTrust';
import { Footer } from './components/Footer';
import { LoadingState } from './components/LoadingState';
import { ErrorState } from './components/ErrorState';
import { ToolRegistryModal } from './components/ToolRegistryModal';
import { sendChatQuery } from './services/api';

export function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [confirmedFacts, setConfirmedFacts] = useState<Record<string, any>>({});
  const [conversationId, setConversationId] = useState<string>(() => `session-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isToolsModalOpen, setIsToolsModalOpen] = useState(false);
  const [isJudgeDrawerOpen, setIsJudgeDrawerOpen] = useState(false);

  const handleSendMessage = async (userText: string, contextOverride: Record<string, any> = {}) => {
    const userMsgId = `user-${Date.now()}`;
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    const newUserMsg: ChatMessage = {
      id: userMsgId,
      sender: 'USER',
      text: userText,
      timestamp: timeStr,
    };

    setMessages((prev) => [...prev, newUserMsg]);
    setIsLoading(true);
    setError(null);

    try {
      // Merge accumulated confirmed facts with new context override
      const mergedContext = { ...confirmedFacts, ...contextOverride };
      const response = await sendChatQuery(userText, mergedContext, conversationId);

      // Cleanly sync jurisdiction and extracted facts into confirmed facts memory
      if (response.situation?.extracted_facts) {
        setConfirmedFacts((prev) => {
          const nextFacts = { ...prev, ...response.situation.extracted_facts };
          if (response.situation.extracted_facts.country === 'US') {
            delete nextFacts.state;
          }
          return nextFacts;
        });
      }

      // Generate natural conversational response text
      let naturalText = response.situation.summary;

      if (response.flow === 'PUBLIC_SERVICE' && response.missing_information && response.missing_information.length > 0) {
        const questionsList = response.missing_information.map((m, i) => `${i + 1}. ${m.question}`).join('\n');
        naturalText = `I can help you find relevant public assistance programs.\n\nTo narrow this down precisely, I just need a few details:\n${questionsList}`;
      } else if (response.recommendations && response.recommendations.length > 0 && response.flow === 'PUBLIC_SERVICE') {
        const top = response.recommendations[0];
        naturalText = `Based on what you've shared, I found verified programs that match your situation, led by **${top.title}**.\n\nBelow are the step-by-step guidance, required documents, and direct links to official government portals.`;
      }

      const sahayMsgId = `sahay-${Date.now()}`;
      const sahayMsg: ChatMessage = {
        id: sahayMsgId,
        sender: 'SAHAY',
        text: naturalText,
        responseObject: response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, sahayMsg]);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred while connecting to Sahay.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setMessages([]);
    setConfirmedFacts({});
    setConversationId(`session-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`);
    setError(null);
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#070B14] text-slate-100 flex flex-col font-sans selection:bg-sky-500 selection:text-white bg-ambient-lights">
      <Header
        onOpenTools={() => setIsToolsModalOpen(true)}
        onNavigateHome={handleReset}
        onSelectEmergency={() => handleSendMessage('My house was damaged by flooding in Bihar and we have nowhere to stay tonight.', { country: 'IN', state: 'Bihar' })}
        onToggleJudgeDrawer={() => setIsJudgeDrawerOpen(!isJudgeDrawerOpen)}
        isJudgeDrawerOpen={isJudgeDrawerOpen}
      />

      <JudgeScenariosBar
        isOpen={isJudgeDrawerOpen}
        onClose={() => setIsJudgeDrawerOpen(false)}
        onSelectScenario={(prompt, ctx) => {
          handleReset();
          handleSendMessage(prompt, ctx);
        }}
      />

      <main className="flex-1">
        {error ? (
          <ErrorState error={error} onRetry={() => setError(null)} />
        ) : messages.length > 0 ? (
          <>
            <ChatInterface
              messages={messages}
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
              onResetConversation={handleReset}
              onOpenTools={() => setIsToolsModalOpen(true)}
            />
            {isLoading && <LoadingState />}
          </>
        ) : (
          <>
            {isLoading ? (
              <LoadingState />
            ) : (
              <>
                <Hero onSubmitQuery={handleSendMessage} isLoading={isLoading} />
                <TrustStrip />
                <HowItWorks />
                <TechnicalTrust onOpenTools={() => setIsToolsModalOpen(true)} />
              </>
            )}
          </>
        )}
      </main>

      <ToolRegistryModal
        isOpen={isToolsModalOpen}
        onClose={() => setIsToolsModalOpen(false)}
      />

      <Footer />
    </div>
  );
}

export default App;
