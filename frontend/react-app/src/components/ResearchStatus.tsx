import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { CheckCircleIcon, ClockIcon, DocumentTextIcon } from '@heroicons/react/24/outline';
import { researchApi } from '../api/client';
import type { ResearchStatusResponse } from '../types';
import clsx from 'clsx';

interface ResearchStatusProps {
    jobId: string;
    onComplete: (data: ResearchStatusResponse) => void;
}

export const ResearchStatus: React.FC<ResearchStatusProps> = ({ jobId, onComplete }) => {
    const [status, setStatus] = useState<string>('queued');
    // const [error, setError] = useState<string | null>(null);

    // Polling Logic
    useEffect(() => {
        let isMounted = true;
        const poll = async () => {
            try {
                const data = await researchApi.getStatus(jobId);
                if (isMounted) {
                    setStatus(data.status);
                    if (data.status === 'completed' || data.status === 'failed') {
                        onComplete(data);
                        return; // Stop polling
                    }
                }
            } catch (err) {
                console.error("Polling error", err);
                // if (isMounted) setError("Failed to fetch status");
            }

            if (isMounted && status !== 'completed' && status !== 'failed') {
                setTimeout(poll, 2000); // Poll every 2s
            }
        };

        poll();
        return () => { isMounted = false; };
    }, [jobId, status]);

    const steps = [
        { id: 'clinical_trials', label: 'Clinical Trials Mining', activeStates: ['running', 'generating_report', 'completed'], completedStates: ['generating_report', 'completed'] },
        { id: 'synthesis', label: 'Evidence Synthesis (LLM)', activeStates: ['running', 'generating_report', 'completed'], completedStates: ['generating_report', 'completed'] },
        { id: 'report', label: 'Report Generation', activeStates: ['generating_report', 'completed'], completedStates: ['completed'] },
    ];

    const getStepState = (step: typeof steps[0]) => {
        if (steps.some(s => s.completedStates.includes(status) && s === step)) return 'completed';
        // Rough heuristic for prototype since backend status is simple
        // In real app, backend would give granular progress. 
        // Here we map 3 simple states to 3 generic steps.

        // If status is 'running', we assume we are doing trials or synthesis.
        // If status is 'generating_report', we are doing report.
        if (step.activeStates.includes(status)) return 'active';
        return 'pending';
    };

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-pharma-card rounded-xl p-8 border border-slate-700 shadow-xl relative overflow-hidden"
        >
            {/* Background Pulse */}
            {status !== 'completed' && status !== 'failed' && (
                <div className="absolute top-0 right-0 w-32 h-32 bg-pharma-accent/20 rounded-full blur-3xl -mr-10 -mt-10 animate-pulse"></div>
            )}

            <h3 className="text-xl font-semibold mb-6 flex items-center space-x-3">
                <div className={clsx("w-3 h-3 rounded-full", {
                    'bg-pharma-accent animate-ping': status === 'running' || status === 'generating_report',
                    'bg-pharma-success': status === 'completed',
                    'bg-pharma-error': status === 'failed',
                    'bg-slate-500': status === 'queued'
                })}></div>
                <span>Research Status: <span className="text-pharma-accent capitalize">{status.replace('_', ' ')}</span></span>
            </h3>

            <div className="space-y-6 relative">
                {/* Connecting Line */}
                <div className="absolute left-6 top-4 bottom-4 w-0.5 bg-slate-800 -z-10"></div>

                {steps.map((step, idx) => {
                    const stepState = getStepState(step);
                    return (
                        <div key={idx} className="flex items-center space-x-4">
                            <div className={clsx("w-12 h-12 rounded-full flex items-center justify-center border-4 transition-all duration-500", {
                                'border-pharma-success bg-pharma-success/20 text-pharma-success': stepState === 'completed',
                                'border-pharma-accent bg-pharma-accent/20 text-pharma-accent animate-pulse': stepState === 'active',
                                'border-slate-700 bg-slate-800 text-slate-500': stepState === 'pending'
                            })}>
                                {stepState === 'completed' ? <CheckCircleIcon className="w-6 h-6" /> :
                                    stepState === 'active' ? <ClockIcon className="w-6 h-6 animate-spin-slow" /> :
                                        <DocumentTextIcon className="w-6 h-6" />}
                            </div>
                            <div>
                                <p className={clsx("font-medium text-lg", {
                                    'text-white': stepState !== 'pending',
                                    'text-slate-500': stepState === 'pending'
                                })}>{step.label}</p>
                                <p className="text-sm text-slate-500">
                                    {stepState === 'completed' ? 'Completed successfully' :
                                        stepState === 'active' ? 'Processing...' : 'Waiting...'}
                                </p>
                            </div>
                        </div>
                    )
                })}
            </div>
        </motion.div>
    );
};
