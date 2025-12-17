import React from 'react';
import { motion } from 'framer-motion';
import { DocumentTextIcon, PresentationChartBarIcon, BeakerIcon } from '@heroicons/react/24/outline';
import type { CanonicalResult } from '../types';

interface ReportViewProps {
    result?: CanonicalResult;
    jobId: string;
    onReset: () => void;
}

export const ReportView: React.FC<ReportViewProps> = ({ result, jobId, onReset }) => {
    if (!result) return null;

    const handleDownload = (type: 'pdf' | 'ppt') => {
        // Direct link to our new proxy endpoint. 
        // We use window.open to trigger download in separate tab (or same tab download).
        const url = `http://127.0.0.1:8000/api/research/${jobId}/download/${type}`;
        window.open(url, '_blank');
    };

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
        >
            {/* Top Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-pharma-card p-6 rounded-xl border border-slate-700 shadow-lg">
                    <p className="text-slate-400 text-sm font-medium">Confidence Score</p>
                    <div className="flex items-end mt-2">
                        <span className="text-4xl font-bold text-white">{Math.round((result.confidence_overall || 0) * 100)}%</span>
                    </div>
                    <div className="w-full bg-slate-700 h-2 rounded-full mt-3 overflow-hidden">
                        <div className="h-full bg-pharma-accent" style={{ width: `${(result.confidence_overall || 0) * 100}%` }}></div>
                    </div>
                </div>

                <div className="bg-pharma-card p-6 rounded-xl border border-slate-700 shadow-lg">
                    <p className="text-slate-400 text-sm font-medium">Data Completeness</p>
                    <div className="flex items-end mt-2">
                        <span className="text-4xl font-bold text-white">{Math.round((result.data_completeness_score || 0) * 100)}%</span>
                    </div>
                    <div className="w-full bg-slate-700 h-2 rounded-full mt-3 overflow-hidden">
                        <div className="h-full bg-pharma-success" style={{ width: `${(result.data_completeness_score || 0) * 100}%` }}></div>
                    </div>
                </div>

                <div className="bg-pharma-card p-6 rounded-xl border border-slate-700 shadow-lg">
                    <p className="text-slate-400 text-sm font-medium">Trials Analyzed</p>
                    <div className="flex items-center space-x-3 mt-2">
                        <BeakerIcon className="w-8 h-8 text-pharma-warning" />
                        <span className="text-4xl font-bold text-white">{result.trials.length}</span>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left: Summary */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="bg-pharma-card p-8 rounded-xl border border-slate-700 shadow-lg">
                        <h3 className="text-xl font-semibold text-white mb-4">Executive Summary</h3>
                        <div className="prose prose-invert max-w-none text-slate-300">
                            {result.trial_summary?.split('\n').map((line, i) => (
                                <p key={i}>{line}</p>
                            ))}
                        </div>
                    </div>

                    <div className="bg-pharma-card p-8 rounded-xl border border-slate-700 shadow-lg">
                        <h3 className="text-xl font-semibold text-white mb-4">Key Findings</h3>
                        <ul className="space-y-3">
                            {result.key_findings.map((item, i) => (
                                <li key={i} className="flex items-start space-x-3 text-slate-300">
                                    <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-pharma-accent flex-shrink-0"></span>
                                    <span>{item}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>

                {/* Right: Actions & Follow-up */}
                <div className="space-y-6">
                    <div className="bg-pharma-card p-6 rounded-xl border border-slate-700 shadow-lg">
                        <h3 className="text-lg font-semibold text-white mb-4">Downloads</h3>
                        <div className="space-y-3">
                            <button
                                onClick={() => handleDownload('pdf')}
                                className="w-full flex items-center justify-between p-4 bg-slate-800 hover:bg-slate-700 rounded-lg border border-slate-600 transition-colors group"
                            >
                                <div className="flex items-center space-x-3">
                                    <div className="p-2 bg-red-500/10 rounded-lg group-hover:bg-red-500/20">
                                        <DocumentTextIcon className="w-6 h-6 text-red-500" />
                                    </div>
                                    <div className="text-left">
                                        <p className="font-medium text-white">Full Report</p>
                                        <p className="text-xs text-slate-500">PDF Format</p>
                                    </div>
                                </div>
                                {/* Placeholder action */}
                            </button>

                            <button
                                onClick={() => handleDownload('ppt')}
                                className="w-full flex items-center justify-between p-4 bg-slate-800 hover:bg-slate-700 rounded-lg border border-slate-600 transition-colors group"
                            >
                                <div className="flex items-center space-x-3">
                                    <div className="p-2 bg-orange-500/10 rounded-lg group-hover:bg-orange-500/20">
                                        <PresentationChartBarIcon className="w-6 h-6 text-orange-500" />
                                    </div>
                                    <div className="text-left">
                                        <p className="font-medium text-white">Presentation</p>
                                        <p className="text-xs text-slate-500">PowerPoint</p>
                                    </div>
                                </div>
                            </button>
                        </div>
                    </div>

                    <div className="bg-pharma-card p-6 rounded-xl border border-slate-700 shadow-lg">
                        <h3 className="text-lg font-semibold text-white mb-4">Suggested Follow-Up</h3>
                        <ul className="space-y-3">
                            {result.suggested_follow_up.map((item, i) => (
                                <li key={i} className="text-sm text-slate-400 border-l-2 border-slate-600 pl-3">
                                    {item}
                                </li>
                            ))}
                        </ul>
                    </div>

                    <button
                        onClick={onReset}
                        className="w-full py-3 text-slate-400 hover:text-white border border-slate-700 hover:border-slate-500 rounded-lg transition-all"
                    >
                        Start New Research
                    </button>
                </div>
            </div>
        </motion.div>
    );
};
