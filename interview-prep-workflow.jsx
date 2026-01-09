import React from 'react';

const WorkflowDiagram = () => {
  const inputBoxStyle = "bg-slate-700 border-2 border-slate-500 rounded-lg p-3 text-white text-sm";
  const phaseBoxStyle = "rounded-xl p-4 min-h-[140px]";
  const outputBoxStyle = "bg-white/90 rounded-lg p-3 text-slate-800 text-sm leading-relaxed";
  const arrowStyle = "text-slate-400 text-2xl font-bold";
  
  return (
    <div className="bg-slate-900 min-h-screen p-6 font-sans">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Interview Prep Tool: Workflow</h1>
          <p className="text-slate-400">B2B Company Analyst - Interview Prep Mode</p>
        </div>

        {/* Inputs Section */}
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-slate-300 mb-3 uppercase tracking-wide">Inputs</h2>
          <div className="flex gap-4 flex-wrap">
            <div className={inputBoxStyle}>
              <div className="font-semibold text-amber-400 mb-1">Company URL</div>
              <div className="text-slate-300 text-xs">Target company website</div>
            </div>
            <div className={inputBoxStyle}>
              <div className="font-semibold text-amber-400 mb-1">Job Description</div>
              <div className="text-slate-300 text-xs">Full JD text or URL</div>
            </div>
            <div className={inputBoxStyle}>
              <div className="font-semibold text-amber-400 mb-1">Your CV</div>
              <div className="text-slate-300 text-xs">PDF or text upload</div>
            </div>
          </div>
        </div>

        {/* Main Flow */}
        <div className="flex items-start gap-3">
          
          {/* Phase 1 */}
          <div className={`${phaseBoxStyle} bg-gradient-to-b from-blue-600 to-blue-700 flex-1`}>
            <div className="text-blue-200 text-xs font-semibold uppercase tracking-wider mb-2">Phase 1</div>
            <h3 className="text-white font-bold text-lg mb-3">Understand the Company</h3>
            <div className={outputBoxStyle}>
              <div className="font-semibold text-blue-700 mb-2">Quick Brief (5-6 sentences)</div>
              <ul className="space-y-1 text-xs">
                <li>• What problem do they solve?</li>
                <li>• Who are their customers?</li>
                <li>• What makes them different?</li>
                <li>• Business model basics</li>
              </ul>
            </div>
            <div className="text-blue-200 text-xs mt-3 italic">
              Sources: Company website, About page, Product pages
            </div>
          </div>

          <div className={`${arrowStyle} self-center`}>→</div>

          {/* Phase 2 */}
          <div className={`${phaseBoxStyle} bg-gradient-to-b from-purple-600 to-purple-700 flex-1`}>
            <div className="text-purple-200 text-xs font-semibold uppercase tracking-wider mb-2">Phase 2</div>
            <h3 className="text-white font-bold text-lg mb-3">Context & Momentum</h3>
            <div className={outputBoxStyle}>
              <div className="font-semibold text-purple-700 mb-2">Why They're Hiring</div>
              <ul className="space-y-1 text-xs">
                <li>• Recent news & announcements</li>
                <li>• Leadership changes</li>
                <li>• Market pressures / opportunities</li>
                <li>• Role hypothesis: why now?</li>
              </ul>
            </div>
            <div className="text-purple-200 text-xs mt-3 italic">
              Sources: News search, LinkedIn, Press releases
            </div>
          </div>

          <div className={`${arrowStyle} self-center`}>→</div>

          {/* Phase 3 */}
          <div className={`${phaseBoxStyle} bg-gradient-to-b from-emerald-600 to-emerald-700 flex-1`}>
            <div className="text-emerald-200 text-xs font-semibold uppercase tracking-wider mb-2">Phase 3</div>
            <h3 className="text-white font-bold text-lg mb-3">Your Fit</h3>
            <div className={outputBoxStyle}>
              <div className="font-semibold text-emerald-700 mb-2">Strongest Case + Gaps</div>
              <ul className="space-y-1 text-xs">
                <li>• Top 3 proof points (prioritised)</li>
                <li>• Why each matters to them</li>
                <li>• Potential gaps/concerns</li>
                <li>• How to address gaps</li>
              </ul>
            </div>
            <div className="text-emerald-200 text-xs mt-3 italic">
              Sources: CV + JD comparison, Role hypothesis
            </div>
          </div>

          <div className={`${arrowStyle} self-center`}>→</div>

          {/* Phase 4 */}
          <div className={`${phaseBoxStyle} bg-gradient-to-b from-amber-600 to-amber-700 flex-1`}>
            <div className="text-amber-200 text-xs font-semibold uppercase tracking-wider mb-2">Phase 4</div>
            <h3 className="text-white font-bold text-lg mb-3">Interview Ammunition</h3>
            <div className={outputBoxStyle}>
              <div className="font-semibold text-amber-700 mb-2">Questions & Talking Points</div>
              <ul className="space-y-1 text-xs">
                <li>• 3-5 smart questions to ask</li>
                <li>• Topics to weave in naturally</li>
                <li>• Stories/examples to prepare</li>
                <li>• Red flags to watch for</li>
              </ul>
            </div>
            <div className="text-amber-200 text-xs mt-3 italic">
              Sources: All phases synthesised
            </div>
          </div>

        </div>

        {/* Processing Note */}
        <div className="mt-8 bg-slate-800 rounded-lg p-4 border border-slate-600">
          <h3 className="text-white font-semibold mb-2">Processing Logic</h3>
          <div className="grid grid-cols-4 gap-4 text-sm">
            <div className="text-slate-300">
              <span className="text-blue-400 font-semibold">Phase 1:</span> Web scrape company site → Extract & summarise core value prop
            </div>
            <div className="text-slate-300">
              <span className="text-purple-400 font-semibold">Phase 2:</span> News API search → Infer strategic context & hiring rationale
            </div>
            <div className="text-slate-300">
              <span className="text-emerald-400 font-semibold">Phase 3:</span> CV↔JD matching → Prioritise by role hypothesis relevance
            </div>
            <div className="text-slate-300">
              <span className="text-amber-400 font-semibold">Phase 4:</span> Synthesise all phases → Generate actionable prep materials
            </div>
          </div>
        </div>

        {/* Model Recommendation */}
        <div className="mt-4 bg-slate-800/50 rounded-lg p-4 border border-slate-700">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <h3 className="text-white font-semibold">Recommended Model: Claude Sonnet 4.5</h3>
          </div>
          <p className="text-slate-400 text-sm">
            Use <span className="text-white">Claude Sonnet 4.5 (Thinking)</span> for Phase 2-3 inference tasks (role hypothesis, gap analysis). 
            Standard Sonnet 4.5 sufficient for extraction and summarisation tasks.
          </p>
        </div>

        {/* Footer */}
        <div className="mt-6 text-center text-slate-500 text-sm">
          Workflow v1.0 | Steve Porter | Sonar Intelligence
        </div>
      </div>
    </div>
  );
};

export default WorkflowDiagram;
