"use client";

import React, { useEffect, useState } from 'react';
import { formatDistanceToNow } from 'date-fns';
import { Case, CaseStep } from '@/types/caseModels';
import { serverUrl } from '@/utils/config';
import "@/styles/case.css";

const fetchCaseData = async (caseId: string) => {
    try {
        const response = await fetch(`${serverUrl}/cases/${caseId}`);
        if (!response.ok) {
            throw new Error('Case not found');
        }
        return await response.json();
    } catch (error) {
        throw error;
    }
};

const CaseResult = ({ params }: { params: { case_id: string } }) => {
    const case_id = params.case_id;
    const [caseData, setCaseData] = useState<Case | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (case_id) {
            fetchCaseData(case_id)
                .then(data => {
                    setCaseData(data);
                    setLoading(false);
                })
                .catch(error => {
                    setError(error.message);
                    setLoading(false);
                });
        }
    }, [case_id]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!caseData) return <div>No case data found.</div>;

    return (
        <div className="caseDetails">
            <h1 className="title">{caseData.procedure_name}</h1>
            <p className="summary">CPT Codes: {caseData.cpt_codes.join(', ')}</p>
            
            {caseData.summary ? (
                <p className="summary">Summary: {caseData.summary}</p>
            ) : (
                <p className="summary">Summary: Loading summary or not available...</p>
            )}
    
            <p className="createdInfo">Case Created: {formatDistanceToNow(new Date(caseData.created_at))} ago</p>
    
            {caseData.steps.length > 0 ? (
                <div className="steps">
                    <h2>Steps:</h2>
                    <ul>
                        {caseData.steps.map((step: CaseStep, index: number) => (
                            <li key={index} className="stepItem">
                                <p><strong>Question:</strong> {step.question}</p>
                                <p><strong>Determination:</strong> {step.is_met ? 'Met' : 'Not Met'}</p>
                                {step.reasoning && <p><strong>Reasoning:</strong> {step.reasoning}</p>}
                                {step.decision && <p><strong>Decision:</strong> {step.decision}</p>}
                                {step.evidence && step.evidence.map((evidence, evidenceIndex) => (
                                    <div key={evidenceIndex} className="evidence">
                                        <p><strong>Evidence Content:</strong> {evidence.content}</p>
                                        {evidence.event_datetime && <p><strong>Date:</strong> {new Date(evidence.event_datetime).toLocaleDateString()}</p>}
                                    </div>
                                ))}
                            </li>
                        ))}
                    </ul>
                </div>
            ) : (
                <p className="summary">No steps available for this case.</p>
            )}
    
            <p className="finalDetermination">Final Determination: {caseData.is_met ? 'Met' : 'Not Met'}</p>
        </div>
    );
    
};

export default CaseResult;
