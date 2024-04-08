export interface Evidence {
    content: string;
    page_number: number;
    pdf_name: string;
    event_datetime?: Date;
  }
  
  export interface StepOption {
    key: string;
    text: string;
    selected: boolean;
  }
  
  export interface StepLogic {
    text: string;
    selected: boolean;
  }
  
  export interface CaseStep {
    key: string;
    question: string;
    options: StepOption[];
    reasoning?: string;
    decision?: string;
    next_step?: string;
    is_met?: boolean;
    is_final?: boolean;
    evidence?: Evidence[];
    logic?: StepLogic[];
  }
  
  export interface Case {
    case_id: string;
    status: string;
    procedure_name: string;
    cpt_codes: string[];
    summary?: string;
    is_met: boolean;
    is_complete: boolean;
    steps: CaseStep[];
    created_at: Date;
  }
  