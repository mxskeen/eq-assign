export interface FilterResult {
    filter_name: string;
    passed: boolean;
    detail: string;
    expected: string | null;
    actual: string | null;
}

export interface Evaluation {
    candidate_id: string;
    candidate_data: {
        asin: string;
        title: string;
        price: number;
        rating: number;
        reviews: number;
        category?: string;
    };
    filter_results: FilterResult[];
    qualified: boolean;
    metadata: {
        score?: number;
        score_breakdown?: {
            review_score: number;
            rating_score: number;
            price_proximity: number;
        };
    };
}

export interface Step {
    name: string;
    step_type: string;
    input_data: Record<string, unknown> | null;
    output_data: Record<string, unknown> | null;
    reasoning: string | null;
    evaluations: Evaluation[];
    status: string;
    started_at: string | null;
    completed_at: string | null;
    error: string | null;
    metadata: Record<string, unknown>;
}

export interface Trace {
    trace_id: string;
    name: string;
    started_at: string;
    completed_at: string | null;
    metadata: Record<string, unknown>;
    steps: Step[];
}
