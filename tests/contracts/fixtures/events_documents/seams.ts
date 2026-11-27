// Version 1 worker interface. Wire bodies are separate from normalized receipt expectations.
export type Slot = "calendar" | "filings" | "transcript" | "news";
type Dates = { start_date: string; end_date: string };
type Page = { page: number; limit: number };
type Period = { year: number; quarter: number };
export type ChartDisplay = "bar" | "point";
export type ChartMeasure = "eps" | "revenue";

export type Choices = {
  version: 1;
  symbol: string;
  calendar: Dates;
  filings: Dates & Page;
  transcript: Period;
  news: Page & (Dates | { start_date?: never; end_date?: never });
  charts: Record<ChartMeasure, ChartDisplay>;
};

type RequestParameters = {
  calendar: Choices["calendar"] & { symbol?: never };
  filings: Choices["filings"] & { symbol: string };
  transcript: Choices["transcript"] & { symbol: string };
  news: Choices["news"] & { symbol: string };
};

export type Query<K extends Slot = Slot> = {
  [P in K]: { slot: P; parameters: RequestParameters[P] & { provider: "fmp" } };
}[K];

export type Scope<K extends Slot = Slot> = {
  query: Query<K>;
  generation: number;
  provider: "fmp";
  dataset: string;
  route: string;
};

export type SelectionIssue = {
  field: string;
  bounds: string;
};

export type SelectionResult<K extends Slot = Slot> =
  | { valid: true; query: Query<K> }
  | { valid: false; issue: SelectionIssue };

export type CalendarField = "eps_actual" | "eps_consensus" | "revenue_actual" | "revenue_consensus";
export type CalendarTokens = Readonly<Record<number, Partial<Record<CalendarField, string>>>>;
export type InstalledFailureCode =
  | "authentication" | "entitlement" | "throttling" | "timeout" | "invalid_parameters"
  | "invalid_response" | "upstream" | "internal_error";

export type FailureCode = InstalledFailureCode
  | "transport" | "unavailable" | "invalid_evidence" | "permission_denied" | "unknown";

export type Failure<K extends Slot = Slot> = {
  status: "failure";
  scope: Scope<K>;
  httpStatus: number | null;
  code: FailureCode;
  retryable: boolean;
};

export type BodylessEmpty<K extends Slot = Slot> = {
  status: "empty";
  httpStatus: 204;
  scope: Scope<K>;
  providerRetrievedAt: null;
  respondedAt: string;
};

// E is the Workspace FinancialEvidence with known metadata, including its original rows.
export type BodyReceipt<E, K extends Slot = Slot> = {
  status: "success" | "empty";
  httpStatus: 200;
  scope: Scope<K>;
  providerRetrievedAt: string;
  evidence: E;
} & (K extends "calendar" ? { tokens: CalendarTokens } : { tokens?: never });

export type Receipt<E, K extends Slot = Slot> = {
  [P in K]: BodyReceipt<E, P> | BodylessEmpty<P> | Failure<P>;
}[K];

export type Read<E> = <K extends Slot>(scope: Scope<K>, signal: AbortSignal) => Promise<Receipt<E, K>>;

export type SlotState<E, K extends Slot> =
  | { status: "idle" }
  | { status: "invalid"; issue: SelectionIssue }
  | { status: "pending"; scope: Scope<K> }
  | Receipt<E, K>;

export type ControlsProps = {
  choices: Choices;
  issues: Partial<Record<Slot | "symbol", SelectionIssue>>;
  onApplySymbol: (symbol: string) => void;
  onApplyBounds: <K extends Slot>(slot: K, bounds: Choices[K]) => void;
  onChartDisplayChange: (measure: ChartMeasure, display: ChartDisplay) => void;
};

export type Controller<E> = {
  controls: ControlsProps;
  slots: { [K in Slot]: SlotState<E, K> };
  onRetry: (slot: Slot) => void;
};

export type CalendarMark = {
  generation: number;
  ordinal: number;
  field: CalendarField;
  plotValue: number;
  exactText: string;
};

export type EarningsProps<E> = {
  symbol: string;
  slot: SlotState<E, "calendar">;
  display: Choices["charts"];
  onRetry: () => void;
  onInspect: (mark: CalendarMark) => void;
};

export type DocumentsProps<E> = {
  slots: Pick<Controller<E>["slots"], "filings" | "transcript" | "news">;
  onRetry: (slot: Exclude<Slot, "calendar">) => void;
};

export type StoryLayout = {
  i: "events_documents_story";
  x: number;
  y: number;
  w: number;
  h: number;
  view_order: ["question", "calendar", "filings", "transcript", "news", "conclusion"];
  state: { storage: { eventsDocuments: Choices } };
};

export type ReceiptExpectation<K extends Slot> =
  | Omit<BodyReceipt<unknown, K>, "evidence"> | BodylessEmpty<K> | Failure<K>;
