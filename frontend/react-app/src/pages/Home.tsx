import React, { useState } from 'react';
import axios from 'axios';
import { Layout } from '../components/Layout';
import { NewResearch } from '../components/NewResearch';
import { ResearchStatus } from '../components/ResearchStatus';
import { ReportView } from '../components/ReportView';
import { researchApi } from '../api/client';
import type { CanonicalResult } from '../types';

export const Home: React.FC = () => {
    const [view, setView] = useState<'new' | 'status' | 'report'>('new');
    const [currentJobId, setCurrentJobId] = useState<string | null>(null);
    const [result, setResult] = useState<CanonicalResult | undefined>(undefined);
    const [isLoading, setIsLoading] = useState(false);

    const handleStartResearch = async (molecule: string, prompt: string) => {
        setIsLoading(true);
        try {
            const data = await researchApi.createJob(molecule, prompt);
            setCurrentJobId(data.job_id);
            setView('status');
        } catch (e: any) {
            console.error("Failed to start job", e);
            if (axios.isAxiosError(e)) {
                alert(`Error: ${e.message}\nStatus: ${e.response?.status}\nData: ${JSON.stringify(e.response?.data)}`);
            } else {
                alert(`Failed to start research job. Check backend connection.\n${e?.message || e}`);
            }
        } finally {
            setIsLoading(false);
        }
    };

    const handleResearchComplete = (data: any) => {
        if (data.status === 'completed') {
            setResult(data.canonical_result);
            setView('report');
        } else {
            // failed
            alert("Research job failed.");
            setView('new');
        }
    };

    return (
        <Layout>
            <div className="space-y-8">
                {/* Header Section */}
                <div className="flex flex-col space-y-2">
                    <h1 className="text-3xl font-bold text-white">
                        {view === 'new' ? 'Welcome, Researcher' :
                            view === 'status' ? 'Research in Progress' :
                                'Research Results'}
                    </h1>
                    <p className="text-slate-400">
                        {view === 'new' ? 'Enter a molecule to begin autonomous clinical trial analysis.' :
                            view === 'status' ? 'Our agents are mining, synthesizing, and generating reports.' :
                                `Analysis complete for ${result?.molecule || 'Molecule'}.`}
                    </p>
                </div>

                {/* View Switcher */}
                <div className="min-h-[600px]">
                    {view === 'new' && (
                        <NewResearch onSubmit={handleStartResearch} isLoading={isLoading} />
                    )}

                    {view === 'status' && currentJobId && (
                        <ResearchStatus jobId={currentJobId} onComplete={handleResearchComplete} />
                    )}

                    {view === 'report' && currentJobId && (
                        <ReportView result={result} jobId={currentJobId} onReset={() => setView('new')} />
                    )}
                </div>
            </div>
        </Layout>
    );
};
