export type FlowType = 'CRISIS' | 'PUBLIC_SERVICE' | 'ELIGIBILITY_CHECK' | 'DOCUMENT_GUIDANCE' | 'GENERAL_INFORMATION' | 'WEB_SEARCH_REQUIRED' | 'AMBIGUOUS';
export type UrgencyLevel = 'CRISIS' | 'HIGH' | 'NORMAL' | 'INFORMATIONAL';
export type EligibilityStatus = 'LIKELY_ELIGIBLE' | 'POTENTIALLY_ELIGIBLE' | 'INELIGIBLE' | 'UNCERTAIN';
export type TTEProposalStatus = 'PROPOSED' | 'VALIDATED' | 'APPROVED' | 'REJECTED';

export interface Situation {
  summary: string;
  extracted_facts: Record<string, any>;
  primary_intent?: string;
  weather_data?: Record<string, any>;
}

export interface Urgency {
  level: UrgencyLevel;
  score: number;
  reasoning: string;
}

export interface MissingInfoItem {
  field: string;
  question: string;
  importance: string;
}

export interface RecommendationItem {
  scheme_id: string;
  title: string;
  issuing_authority: string;
  country?: string;
  jurisdiction_level?: string;
  region?: string;
  category: string;
  summary: string;
  match_confidence: string;
}

export interface EligibilityItem {
  scheme_id: string;
  status: EligibilityStatus;
  matching_criteria: string[];
  unmet_criteria: string[];
  reasoning: string;
}

export interface DocumentItem {
  document_name: string;
  purpose: string;
  how_to_obtain: string;
  is_mandatory: boolean;
}

export interface ActionStep {
  step_number: number;
  title: string;
  description: string;
  estimated_time?: string;
}

export interface SourceItem {
  title: string;
  url: string;
  issuing_authority: string;
  last_verified?: string;
}

export interface EvidenceItem {
  chunk_id: string;
  scheme_id: string;
  title: string;
  content: string;
  country?: string;
  jurisdiction_level?: string;
  region?: string;
  similarity_score: number;
  source_url: string;
  issuing_authority: string;
  last_verified?: string;
  section_type: string;
}

export interface SahayResponse {
  request_id: string;
  timestamp: string;
  flow: FlowType;
  situation: Situation;
  urgency: Urgency;
  missing_information: MissingInfoItem[];
  recommendations: RecommendationItem[];
  eligibility: EligibilityItem[];
  documents: DocumentItem[];
  action_plan: ActionStep[];
  sources: SourceItem[];
  evidence?: EvidenceItem[];
  disclaimer: string;
}

export type SahayAIResponse = SahayResponse;

export interface ToolDefinition {
  name: string;
  version: string;
  category: string;
  description: string;
  input_schema: Record<string, any>;
  output_schema: Record<string, any>;
  permissions: string[];
  reliability_score: number;
  status: string;
  created_at: string;
  approved_by?: string;
}

export interface TTEProposal {
  proposal_id: string;
  tool_name: string;
  problem_context: string;
  generated_code: string;
  test_results: Record<string, any>;
  static_analysis_passed: boolean;
  security_audit_passed: boolean;
  status: TTEProposalStatus;
  created_at: string;
}
