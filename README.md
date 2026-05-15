License: CC BY 4.0
arXiv:2511.14136v1 [cs.AI] 18 Nov 2025
Beyond Accuracy: A Multi-Dimensional Framework for Evaluating Enterprise Agentic AI Systems
Sushant Mehta
sushant0523@gmail.com
Abstract
Current agentic AI benchmarks predominantly evaluate task completion accuracy, while overlooking critical enterprise requirements such as cost-efficiency, reliability, and operational stability. Through systematic analysis of 12 main benchmarks and empirical evaluation of state-of-the-art agents, we identify three fundamental limitations: (1) absence of cost-controlled evaluation leading to 50x cost variations for similar precision, (2) inadequate reliability assessment where agent performance drops from 60% (single run) to 25% (8-run consistency), and (3) missing multidimensional metrics for security, latency, and policy compliance. We propose CLEAR (Cost, Latency, Efficacy, Assurance, Reliability), a holistic evaluation framework specifically designed for enterprise deployment. Evaluation of six leading agents on 300 enterprise tasks demonstrates that optimizing for accuracy alone yields agents 4.4-10.8x more expensive than cost-aware alternatives with comparable performance. Expert evaluation (N=15) confirms that CLEAR better predicts production success (correlation 
ρ
=
0.83
) compared to accuracy-only evaluation (
ρ
=
0.41
).

1Introduction
Rapid advancement of autonomous agents based on large language models (LLM) has generated significant interest in their enterprise applications, from software engineering (Jimenez et al. 2024) to customer service automation (Yao et al. 2024). However, there is a critical gap between benchmark performance and production deployment success. While 85% of the companies experiment with generative AI, only a small fraction deploy agents in production, with most projects abandoned after proof-of-concept stages (Chiu 2025). This failure stems from a fundamental misalignment: existing benchmarks optimize for task completion accuracy, while enterprises require holistic evaluation across cost, reliability, security, and operational constraints.

Recent benchmarks have made substantial progress in evaluating agent capabilities. SWE-bench (Jimenez et al. 2024) assesses software engineering through real GitHub issues, WebArena (Zhou et al. 2023) tests web navigation across realistic environments, and AgentBench (Liu et al. 2023a) provides multi-environment evaluation. However, systematic analysis reveals three critical limitations that impede enterprise adoption and create a distorted view of agent capabilities.

First, cost is entirely ignored. Despite agents making hundreds of API calls per task, with complex architectures like Reflexion making up to 2,000 API calls for iterative refinement, no major benchmark reports cost metrics. Our analysis shows that leading agents exhibit 50x cost variations (from $0.10 to $5.00 per task) for similar accuracy levels, with complex agent architectures achieving marginal accuracy gains at exponential cost increases (Kapoor et al. 2024). This creates a distorted research landscape in which expensive and fragile solutions appear superior to efficient alternatives. A 2-point improvement in accuracy might cost $50,000 additional spend per 10,000 tasks, an unacceptable trade-off for most enterprises.

Second, reliability remains unmeasured. Production systems require consistent performance across thousands of similar requests with failure rates below 1-5%, yet benchmarks report single-run success rates that mask brittleness. Recent work in the 
τ
-bench (Yao et al. 2024) introduced pass@k metrics, revealing that GPT-4-based agents drop from success 60% (pass@1) to just 25% (pass@8), which is insufficient for enterprise deployment where reliability is paramount. A customer service agent that works 70% of the time in testing but only 30% consistently in production creates a poorer user experience than a 60% agent with reliable performance.

Third, enterprise-critical dimensions are absent. Real-world deployment demands security against prompt injection, compliance with organizational policies, latency within SLA constraints, and graceful error handling, none systematically evaluated by current benchmarks. Current benchmarks evaluate none of these, creating a performance gap 37% between lab tests and production deployment (Liu et al. 2024). An agent that passes all functional tests, but leaks customer data or violates regulatory requirements, represents a catastrophic failure, not a minor shortcoming.

This work makes four primary contributions:

(1) Systematic Gap Analysis: We analyze 12 major agentic benchmarks (SWE-bench, WebArena, AgentBench, GAIA, ToolLLM, 
τ
-bench, WorkArena, Mind2Web, OSWorld, InterCode, BFCL, and others) and identify specific limitations through the lens of enterprise requirements, documenting validity issues affecting 7/10 benchmarks and cost misestimation rates up to 100% (Kang et al. 2024).

(2) CLEAR Framework: We propose a five-dimensional holistic evaluation framework (cost, latency, efficiency, assurance, reliability) with novel metrics including cost-normalized accuracy (CNA), pass@k reliability, policy adherence score (PAS), and SLA compliance rate tailored for enterprise contexts. The framework supports both individual dimension analysis and composite scoring with customizable weights.

(3) Enterprise Task Suite: We introduce a benchmark of 300 tasks across six enterprise domains (customer support, data analysis, process automation, software development, compliance, multi-stakeholder workflows) with ground-truth cost, latency, and policy compliance annotations. Each task includes 5-15 steps with realistic complexity that reflect actual enterprise workflows.

(4) Empirical Validation: Evaluation of six state-of-the-art agents (ReAct-GPT4, ReAct-GPT-o3, Reflexion, Plan-Execute, ToolFormer, Domain-Tuned) reveals that accuracy-optimal configurations cost 4.4-10.8x more than Pareto-efficient alternatives. Expert validation (N = 15 Enterprise-AI leads) shows that CLEAR predictions are strongly correlated with production success (
ρ
=
0.83
, p<0.001) versus accuracy-alone (
ρ
=
0.41
, p=0.03), establishing statistical significance and practical relevance.

Our findings establish that multidimensional evaluation is not optional but essential for the deployment of enterprise agents, providing actionable frameworks for both researchers and practitioners. We aim to release our Enterprise Task Suite, evaluation code, and complete experimental results to facilitate adoption and enable reproducible research to advance practical agent systems.

2Related Work
2.1Agentic AI Benchmarks
The landscape of agent evaluation has evolved rapidly. Software engineering benchmarks include the SWE-bench (Jimenez et al. 2024), which evaluates agents on 2,294 real GitHub issues with execution-based testing, and InterCode (Yang et al. 2023) enabling interactive coding with execution feedback across Bash, SQL, Python, and CTF challenges. Web navigation benchmarks assess agents in browser environments: WebArena (Zhou et al. 2023) provides 812 tasks on self-hosted websites with functional correctness evaluation, while Mind2Web (Deng et al. 2023) covers 2,350 tasks on 137 real websites.

Multi-domain benchmarks test generalization. AgentBench (Liu et al. 2023a) evaluates 29 LLMs in eight environments (OS, database, knowledge graphs, gaming, embodied AI), revealing significant gaps between commercial and open source models. GAIA (Mialon et al. 2023) provides 466 real-world questions that require reasoning, multimodality, and tool use, exposing a 77% human-AI performance gap. Tool-use benchmarks include ToolLLM (Qin et al. 2024) that includes 16,464 real-world APIs from RapidAPI and Berkeley Function Calling Leaderboard (Patil et al. 2024) that assess function calling across multiple languages and scenarios.

Enterprise-focused benchmarks have emerged recently. WorkArena (Drouin et al. 2024) evaluates knowledge work on ServiceNow with 33 atomic tasks, while 
τ
-bench (Yao et al. 2024) introduces multi-turn user interactions with policy compliance in retail and airline domains, revealing reliability issues through pass@k metrics.

2.2Benchmark Limitations
Recent critical analyses expose systematic problems. Kapoor et al. (Kapoor et al. 2024) demonstrate that agent evaluations fail to control cost, creating misleading conclusions about architecture improvements. Their analysis shows that simple baseline strategies outperform complex agents at 50x lower cost. They identify inadequate holdout sets, with 7/8 benchmarks lacking appropriate validation sets for claimed generality levels.

Kang et al. (Kang et al. 2024) found severe validity issues in 8/10 popular benchmarks, including task validity failures (do-nothing agents passing 38% of 
τ
-bench airline tasks), outcome validity failures (LLM-as-judge making arithmetic errors, augmented tests changing 41% of SWE-bench rankings), and undisclosed issues. Yehudai et al. (Yehudai et al. 2025) surveyed 120 agent evaluation frameworks, identifying missing enterprise requirements including multistep granular evaluation, cost-efficiency measurement, focus on safety and compliance, and live adaptive benchmarks.

2.3Enterprise AI Evaluation
Enterprise evaluation differs fundamentally from academic benchmarking. Aisera’s CLASSic framework (Aisera Research Team 2024) proposes five dimensions (Cost, Latency, Accuracy, Stability, Security) with empirical evidence that domain-specific agents achieve 82.7% accuracy versus 59-63% for general LLMs at 4.4-10.8x lower cost. AWS research (Liu et al. 2024) on multi-agent systems demonstrates 90% goal success rates with proper coordination versus 53-60% for single agents, while documenting a 37% performance gap from lab to production. Industry reports highlight that only 10% of enterprises successfully implement generative AI in production (Chiu 2025), with inadequate evaluation frameworks cited as the main failure factor.

3The CLEAR Framework
We propose CLEAR (Cost, Latency, Efficacy, Assurance, Reliability), a comprehensive framework that addresses the identified gaps. CLEAR recognizes that enterprise deployment requires multi-objective optimization across five critical dimensions.

3.1Framework Dimensions
Cost (C) measures economic efficiency, including API token consumption, inference costs, and infrastructure overhead. We introduce cost-normalized accuracy (CNA):

CNA
=
Accuracy
Cost
×
100
(1)
where Cost is measured in USD per task. This metric enables a fair comparison between expensive high-accuracy agents and cost-effective alternatives. Furthermore, we track the cost per success (CPS) to account for varying success rates:

CPS
=
Total Cost
Number of Successful Tasks
(2)
CPS reveals that failed attempts still incur costs, making reliability economically critical.

Latency (L) evaluates response time throughout the planning, execution, and reflection phases. We measure end-to-end task completion time and introduce SLA compliance rate:

SCR
=
Tasks Completed Within SLA
Total Tasks
×
100
%
(3)
with domain-specific SLA thresholds (3 seconds for customer support, 30 seconds for code generation). Latency directly impacts user experience and system throughput, making it critical for production deployment.

Efficacy (E) captures task completion quality through traditional accuracy metrics augmented with domain-specific measurements. For software tasks, we evaluate functional correctness through test passage rates. For data analysis, we assess the accuracy and quality of the result. For customer support, we measure the accuracy of the intention classification and the appropriateness of the response. Unlike single-metric benchmarks, we recognize that efficacy requirements vary by domain and use case.

Assurance (A) evaluates safety, security, and policy compliance. We introduce policy adherence score (PAS):

PAS
=
1
−
Policy Violations
Total Policy-Critical Actions
(4)
Security assessment includes prompt injection resistance in 500 adversarial test cases from established attack taxonomies, data leak prevention, hallucination rates for domain knowledge, and graceful failure handling. Policy violations represent hard failures in enterprise contexts: a single unauthorized data disclosure can invalidate otherwise perfect performance.

Reliability (R) assesses consistency through the pass@k metric introduced by 
τ
-bench (Yao et al. 2024), where pass@k measures the probability of achieving k consecutive successes:

pass@k
=
Trials with 
​
k
​
 consecutive successes
Total trials
(5)
We evaluated pass@3, pass@5 and pass@8, with production deployment requiring pass@8 
≥
 80% for mission-critical applications. Single-run evaluation masks brittleness: an agent with 70% pass@1 might achieve only 30% pass@8, making it unsuitable for production despite acceptable single-run performance.

3.2Composite Score and Enterprise Task Suite
For single-number comparison: 
CLEAR
=
w
C
⋅
C
norm
+
w
L
⋅
L
norm
+
w
E
⋅
E
+
w
A
⋅
A
+
w
R
⋅
R
 where the weights sum to 1 and are application-specific. Cost and latency are normalized via min-max scaling. Default equal weighting (
w
i
=
0.2
) provides a balanced assessment, while enterprises can customize (e.g., financial services: 
w
R
=
0.4
, 
w
A
=
0.3
; customer-facing: 
w
L
=
0.35
).

We developed 300 tasks in six domains with ground-truth CLEAR annotations: Customer Support (60 tasks): Multiturn policy-compliant issue resolution with escalation handling; Data Analysis (50): SQL query construction, report generation, visualization; Process Automation (50): Multistep workflows with approval chains; Software Development (60): Fixing bugs, review of code, generation of test from production repositories; Compliance (40): GDPR processing, regulatory verification; Multi-Stakeholder (40): Cross-departmental coordination with conflicting priorities. Tasks feature 5-15 steps with realistic complexity. See Appendix A for detailed descriptions.

4Experimental Evaluation
Setup. We assessed six architectures: ReAct-GPT4, ReAct-GPT-o3, Reflexion (Shinn et al. 2023), Plan-Execute (hierarchical planner), ToolFormer (Schick et al. 2023), and Domain-Tuned (fine-tuned Llama). Each executed all 300 tasks. For reliability, we sampled 60 representative tasks and executed each 10 times. We recruited 15 AI enterprise deployment leads (mean experience 5.9 years) who evaluated the results on 40 randomly assigned tasks, rating readiness to deploy on a 5-point scale (inter-rater reliability 
α
=
0.78
).

Table 1:Performance across CLEAR dimensions. Pareto-optimal agents marked with *.
Agent	Eff.	Cost	CNA	Lat.	PAS	R@8
(%)	($)		(s)		(%)
ReAct-GPT4	72.3	2.87	25.2	8.4	0.89	58.3
ReAct-GPT-o3*	68.7	0.31	221.6	4.2	0.85	52.1
Reflexion	74.1	5.12	14.5	12.7	0.91	61.2
Plan-Execute*	71.9	1.24	58.0	6.8	0.88	64.5
ToolFormer	69.5	1.89	36.8	5.9	0.82	55.7
Domain-Tuned*	70.3	0.27	260.4	3.8	0.93	72.8
Results. Table 1 presents results across CLEAR dimensions. Although Reflexion achieved the highest efficacy (74. 1%), it cost 5.12 times more than the efficacy of ReAct-GPT-o3 (68. 7%, representing only 5.4 percentage points of improvement with the increase in cost 1, 551%. Domain-Tuned achieved the best cost-normalized accuracy (260.4) and reliability (pass@8 = 72.8%) through task-specific optimization.

Three agents form the Pareto frontier: ReAct-GPT-o3 (optimal cost), Plan-Execute (balanced), and Domain-Tuned (optimal reliability). Reflexion, despite the highest raw accuracy, is dominated by Plan-Execute, which achieves comparable efficacy (71.9% vs 74.1%) at 4.1x lower cost with superior reliability (64.5% vs 61.2% pass@8).

Single-run success (pass@1) ranges from 68-74%, but 8-run consistency (pass@8) drops dramatically to 52-73%. Domain-Tuned maintains 72.8% pass@8 (10.8% drop from pass@1), while ReAct-GPT4 drops 19.4% (from 72.3% to 58.3%), revealing brittleness in general-purpose agents that single-run evaluation masks.

Domain-Tuned excels in compliance (+7.5 points over ReAct-GPT4) and multi-stakeholder tasks (+7.5 points) where specialized knowledge matters most. ReAct-GPT4 performs best in software development (73.3%). All agents met customer support SLAs (3 sec), but Plan-Execute and Reflexion exceeded software development SLAs (30 sec) on 23% and 34% of tasks due to extensive reflection. Domain-Tuned achieved the highest adherence to policy (PAS = 0.93) with the best resistance to prompt injection (8% successful attacks vs. 18% for ToolFormer). See Appendix B for detailed domain breakdowns.

Table 2:Correlation with expert-rated deployment readiness (N=15 experts, 40 tasks each).
Evaluation Approach	Pearson 
ρ
Spearman 
ρ
s
Efficacy Only	0.41	0.39
Efficacy + Cost	0.58	0.56
CLEAR (All 5 Dimensions)	0.83	0.81
Expert Validation. Table 2 shows CLEAR correlates strongly with expert deployment readiness (
ρ
=
0.83
, p<0.001), substantially outperforming efficacy-only evaluation (
ρ
=
0.41
). The experts valued reliability the most, followed by policy compliance and cost-efficiency. An expert noted: ”A 70% agent that works reliably is far more deployable than an 80% agent that is unpredictable and expensive.”

5Discussion
Implications for Benchmark Design. Our findings demonstrate that academic benchmarks must evolve beyond the accuracy-centric evaluation. Cost transparency should be mandatory-reporting token consumption, API costs, and inference time enables fair comparison. Reliability assessment using pass @ k metrics (minimum k = 8) reveals production-critical brittleness invisible in single-run evaluation. Domain-specific evaluation better captures real-world performance than generic benchmarks, as evidenced by 15-25% performance variations across domains.

Architectural Insights. Domain-tuned models demonstrate surprising effectiveness, achieving best cost-normalized accuracy and reliability despite using smaller base models (70B vs GPT-4’s rumored 1.7T parameters). Task-specific optimization outweighs the scale of the raw model for enterprise-focused applications. Conversely, complex agent architectures (Reflexion with multi-turn self-refinement) show diminishing returns. Although self-reflection improves accuracy marginally, it dramatically increases cost and latency while harming reliability through additional failure modes. The Plan-Execute agent’s strong performance (Pareto-optimal, balanced) indicates that hierarchical decomposition with cost-aware component selection offers a practical middle ground.

Limitations. Task coverage, while spanning six domains with 300 tasks, remains limited compared to the real diversity of the company. Agent selection focused on established architectures; newer approaches warrant investigation. The cost dynamics will shift with the evolution of the model pricing, though the relative comparisons remain valid. Human evaluation with 15 experts provides initial validation, but larger-scale studies would strengthen generalizability. Future work should explore adaptive weight learning, online evaluation methodologies, multi-agent coordination evaluation, interpretability metrics, and long-horizon evaluation.

6Conclusion
This work establishes multidimensional evaluation as essential for enterprise agentic AI systems. Through systematic analysis of 12 main benchmarks, we identified critical gaps: cost is unmeasured despite 50x variations, reliability is untested despite drops in consistency 60 to 25%, and operational requirements are absent despite 37% lab to production gaps. Our CLEAR framework addresses these limitations with a comprehensive assessment of cost, latency, effectiveness, assurance, and reliability.

Empirical evaluation of six leading agents across 300 enterprise tasks demonstrates that accuracy optimization yields suboptimal deployments: agents with highest raw accuracy cost 4.4-10.8x more than Pareto-efficient alternatives. Domain-specialized approaches outperform general-purpose architectures, achieving superior cost-normalized performance (260.4 vs. 14.5-58.0 CNA) and reliability (72.8% vs 52.1-64.5% pass@8). Expert validation confirms that CLEAR predicts production success better (
ρ
=
0.83
) than traditional metrics (
ρ
=
0.41
).

As agentic AI moves from research to production, evaluation must evolve accordingly. CLEAR provides a foundation for enterprise-appropriate assessment, enabling cost-conscious architectural decisions and reliable deployment. We plan to release our Enterprise Task Suite, evaluation code, and complete experimental results to facilitate adoption and enable reproducible research to advance practical agent systems.

References
Beetz and Riedl (2019)
Beetz, R., and Riedl, Y.2019.Robotic Process Automation: Developing a Multi-Criteria Evaluation Model for the Selection of Automatable Business Processes.In AMCIS 2019 Proceedings, volume 4.
Chen et al. (2024)
Chen, J.; Lu, Y.; Wang, X.; Zeng, H.; et al.2024.Multi-Agent-as-Judge: Aligning LLM-Agent-Based Automated Evaluation with Multi-Dimensional Human Evaluation.arXiv preprint arXiv:2507.21028.
Chiu (2025)
Chiu, O.2025.The Key to Production AI Agents: Evaluations.Databricks Blog.
Deng et al. (2023)
Deng, X.; Gu, Y.; Zheng, B.; Chen, S.; Stevens, S.; Wang, B.; Sun, H.; and Su, Y.2023.Mind2Web: Towards a Generalist Agent for the Web.In NeurIPS Datasets and Benchmarks Track.
Drouin et al. (2024)
Drouin, A.; Gasse, M.; Caccia, M.; Laradji, I. H.; Del Verme, M.; Marty, T.; Boisvert, L.; Thakkar, M.; Cappart, Q.; Vazquez, D.; et al.2024.WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?arXiv preprint arXiv:2403.07718.
Jimenez et al. (2024)
Jimenez, C. E.; Yang, J.; Wettig, A.; Yao, S.; Pei, K.; Press, O.; and Narasimhan, K.2024.SWE-bench: Can Language Models Resolve Real-World GitHub Issues?In International Conference on Learning Representations (ICLR).
Kang et al. (2024)
Kang, D., et al.2024.AI Agent Benchmarks Are Broken: A Critical Analysis.Technical Report.
Kapoor et al. (2024)
Kapoor, S.; Stroebl, B.; Pandit, S.; Bommasani, R.; and Narayanan, A.2024.AI Agents That Matter.arXiv preprint arXiv:2407.01502.
Liu et al. (2023a)
Liu, X.; Yu, H.; Zhang, H.; Xu, Y.; Lei, X.; Lai, H.; Gu, Y.; Ding, H.; Men, K.; Yang, K.; et al.2023a.AgentBench: Evaluating LLMs as Agents.In International Conference on Learning Representations (ICLR).
Liu et al. (2023b)
Liu, Y.; Iter, D.; Xu, Y.; Wang, S.; Xu, R.; and Zhu, C.2023b.G-eval: NLG Evaluation using GPT-4 with Better Human Alignment.In Conference on Empirical Methods in Natural Language Processing (EMNLP).
Liu et al. (2024)
Liu, J.; Zhang, K.; Chen, W.; Alkhouli, T.; Negrinho, R.; Elluru, V. R.; Benajiba, Y.; et al.2024.Towards Effective GenAI Multi-Agent Collaboration: Design and Evaluation for Enterprise Applications.arXiv preprint arXiv:2412.05449.
Mialon et al. (2023)
Mialon, G.; Fourrier, C.; Swift, C.; Wolf, T.; LeCun, Y.; and Scialom, T.2023.GAIA: A Benchmark for General AI Assistants.arXiv preprint arXiv:2311.12983.
Patil et al. (2024)
Patil, S. G.; Yan, F.; Mao, H.; Ji, C. C.-W.; Zhang, T.; Stoica, I.; and Gonzalez, J. E.2024.Gorilla: Large Language Model Connected with Massive APIs.Berkeley Function Calling Leaderboard.
Qin et al. (2024)
Qin, Y.; Liang, S.; Ye, Y.; Zhu, K.; Yan, L.; Lu, Y.; Lin, Y.; Cong, X.; Tang, X.; Qian, B.; et al.2024.ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs.In International Conference on Learning Representations (ICLR).
Aisera Research Team (2024)
Aisera Research Team.2024.CLASSic: A Holistic Framework for Evaluating Enterprise AI Agents.Aisera Technical Report.
Salesforce AI Research (2024)
Salesforce AI Research.2024.First-Of-Its-Kind LLM Benchmark Ranks Generative AI Against Real-World Business Tasks.Salesforce Blog.
Samsung Research (2024)
Samsung Research.2024.TRUEBench: Trustworthy Real-world Usage Evaluation Benchmark for Enterprise LLMs.Samsung AI Research.
Schick et al. (2023)
Schick, T.; Dwivedi-Yu, J.; Dessì, R.; Raileanu, R.; Lomeli, M.; Zettlemoyer, L.; Cancedda, N.; and Scialom, T.2023.Toolformer: Language Models Can Teach Themselves to Use Tools.In NeurIPS.
Shinn et al. (2023)
Shinn, N.; Cassano, F.; Gopinath, A.; Narasimhan, K.; and Yao, S.2023.Reflexion: Language Agents with Verbal Reinforcement Learning.In NeurIPS.
Xie et al. (2024)
Xie, T.; Zhang, D.; Chen, J.; Li, X.; Zhao, S.; Cao, R.; Hua, T. J.; Shin, D.; Lei, F.; Liu, Y.; et al.2024.OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments.In NeurIPS Datasets and Benchmarks Track.
Yang et al. (2023)
Yang, J.; Prabhakar, A.; Narasimhan, K.; and Yao, S.2023.InterCode: Standardizing and Benchmarking Interactive Coding with Execution Feedback.In NeurIPS Datasets and Benchmarks Track.
Yao et al. (2023)
Yao, S.; Zhao, J.; Yu, D.; Du, N.; Shafran, I.; Narasimhan, K.; and Cao, Y.2023.ReAct: Synergizing Reasoning and Acting in Language Models.In International Conference on Learning Representations (ICLR).
Yao et al. (2024)
Yao, S.; Hu, J.; Shinn, N.; and Narasimhan, K.2024.
τ
-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.arXiv preprint arXiv:2406.12045.
Yehudai et al. (2025)
Yehudai, A.; Eden, L.; Li, A.; Uziel, G.; Zhao, Y.; Bar-Haim, R.; Cohan, A.; and Shmueli-Scheuer, M.2025.Survey on Evaluation of LLM-based Agents.arXiv preprint arXiv:2503.16416.
Zhang et al. (2024)
Zhang, Z., et al.2024.Agent-SafetyBench: Evaluating the Safety of LLM Agents.arXiv preprint arXiv:2412.14470.
Zhou et al. (2023)
Zhou, S.; Xu, F. F.; Zhu, H.; Zhou, X.; Lo, R.; Sridhar, A.; Cheng, X.; Bisk, Y.; Fried, D.; Alon, U.; et al.2023.WebArena: A Realistic Web Environment for Building Autonomous Agents.In Advances in Neural Information Processing Systems, volume 36.
Appendix AEnterprise Task Suite Details
Our benchmark comprises 300 tasks across six enterprise domains, each with ground-truth annotations for all CLEAR dimensions:

Customer Support (60 tasks): Multi-turn policy-compliant issue resolution requiring knowledge base retrieval with proper citation, escalation handling with role-based routing, and complaint management with sentiment analysis. Tasks span routine inquiries (30%), complex technical issues (40%), and edge cases requiring human escalation (30%). SLA: 3 seconds average response time.

Data Analysis (50 tasks): Report generation from structured databases, SQL query construction with optimization constraints, data visualization with accuracy verification, and trend analysis with statistical validation. Tasks require handling missing data, outlier detection, and ensuring compliance with data privacy regulations. SLA: 15 seconds for query execution, 45 seconds for reports.

Process Automation (50 tasks): Form completion with validation rules, approval workflow navigation across multi-step processes, cross-system integration requiring API orchestration, and exception handling for edge cases. Tasks test error recovery, rollback mechanisms, and audit trail generation. SLA: 10 seconds per process step.

Software Development (60 tasks): Bug fixing in production codebases with test-driven validation, code review with security vulnerability detection, test generation achieving ¿80% coverage, and refactoring with performance optimization. Tasks span Python (40%), JavaScript (30%), and Java (30%) from real enterprise repositories. SLA: 30 seconds for analysis, 60 seconds for code generation.

Compliance (40 tasks): GDPR request processing (data access, deletion, portability), audit trail validation ensuring complete traceability, regulatory requirement verification against SOC 2 and ISO 27001 standards, and policy enforcement across multi-stakeholder workflows. Tasks require precise interpretation of legal language and zero-tolerance for policy violations. SLA: 20 seconds per compliance check.

Multi-Stakeholder Workflows (40 tasks): Cross-departmental coordination requiring approval chains, conflict resolution with competing stakeholder priorities, role-based access control enforcement, and deadline management with escalation paths. These represent the most complex scenarios with 8-15 steps, multiple decision points, and requiring negotiation between conflicting requirements. SLA: 15 seconds per interaction.

All tasks include: (1) Natural language task description, (2) Required input data/context, (3) Expected output with ground-truth, (4) Policy documents defining constraints, (5) Cost baselines from reference implementations, (6) Latency SLA thresholds, (7) Security test cases, (8) Reliability baseline from 50 human expert executions.

Appendix BDetailed Domain Performance
Table 3 presents a comprehensive breakdown of the domain-specific performance in the six agents and the dimensions of efficacy and policy adherence.

Table 3:Detailed domain-specific performance showing efficacy (%) and policy adherence score (PAS) across six enterprise task categories.
ReAct-GPT4	Plan-Exec	Domain-T
Domain	Eff.	PAS	Eff.	PAS	Eff.	PAS
Customer Support	78.3	0.87	75.0	0.85	81.7	0.95
Data Analysis	69.0	0.94	72.0	0.93	71.0	0.96
Process Automation	71.0	0.88	73.0	0.89	72.0	0.92
Software Dev.	73.3	0.91	70.0	0.87	71.7	0.94
Compliance	65.0	0.82	67.5	0.84	72.5	0.93
Multi-Stakeholder	61.3	0.78	64.0	0.81	68.8	0.89
Overall	72.3	0.89	71.9	0.88	70.3	0.93
Key Domain Insights:

Customer Support: Domain-Tuned excels due to fine-tuning on enterprise support tickets with policy-compliant response templates. The 81.7% efficacy represents successful resolution without escalation. PAS of 0.95 indicates minimal policy violations (e.g., unauthorized discounts, data sharing). ReAct-GPT4 struggles with policy boundaries (PAS 0.87), often over-promising or providing unauthorized information.

Data Analysis: All agents perform moderately well (69-72% efficacy), with high policy adherence (0.93-0.96) since SQL constraints naturally enforce data access policies. Plan-Execute slightly outperforms (72%) through hierarchical query decomposition. Failures primarily stem from complex multi-table joins and aggregate functions.

Process Automation: Balanced performance across agents (71-73%). Plan-Execute’s hierarchical structure aligns naturally with multi-step workflows. Policy adherence challenges include skipping required approvals and violating temporal sequencing constraints. Domain-Tuned achieves highest PAS (0.92) through learned workflow patterns.

Software Development: ReAct-GPT4 achieves best efficacy (73.3%) leveraging GPT-4’s superior code understanding, particularly for complex refactoring. However, policy violations occur through unsafe code patterns (hardcoded credentials, SQL injection vulnerabilities). Domain-Tuned balances code quality with security compliance (PAS 0.94).

Compliance: Largest performance gap across agents (65-72.5%). Domain-Tuned significantly outperforms (+7.5 points) due to training on regulatory documents and legal language. General-purpose agents struggle with precise legal interpretation, often providing approximately correct but legally insufficient responses. PAS variation (0.82-0.93) reflects challenges in zero-tolerance compliance requirements.

Multi-Stakeholder: Lowest efficacy across all agents (61-69%), highlighting fundamental challenges in complex coordination. Tasks require balancing conflicting priorities, managing approval chains with 3-5 stakeholders, and negotiating constraint violations. Domain-Tuned’s advantage (+7.5 points over ReAct-GPT4) comes from learned conflict resolution patterns. Low PAS (0.78-0.89) indicates frequent policy violations in complex scenarios with competing requirements.

Appendix CCost and Latency Analysis
Table 4:Detailed cost breakdown and latency analysis across agents.
Agent	Input	Output	Total	Plan	Exec	Reflect
Tok.	Tok.	Cost	(s)	(s)	(s)
ReAct-GPT4	47.2K	8.3K	$2.87	2.1	4.8	1.5
ReAct-GPT-o3	52.1K	9.7K	$0.31	1.2	2.4	0.6
Reflexion	89.4K	15.2K	$5.12	3.4	6.1	3.2
Plan-Execute	38.6K	7.1K	$1.24	1.8	4.2	0.8
ToolFormer	44.3K	9.8K	$1.89	1.5	3.6	0.8
Domain-Tuned	31.2K	5.4K	$0.27	0.9	2.3	0.6
Table 4 reveals that Reflexion’s high cost stems from multiple self-reflection iterations (avg 2.8 iterations per task), increasing both token consumption and latency. Domain-Tuned achieves lowest cost through efficient inference on smaller model with task-specific optimization reducing unnecessary reasoning steps. Plan-Execute balances cost by using GPT-4 for planning (15% of tokens) and GPT-o3 for execution (85% of tokens).

Latency breakdown shows reflection phases dominate for Reflexion (3.2s, 25% of total), while Domain-Tuned minimizes reflection through learned patterns. Planning latency varies 0.9-3.4s, with Reflexion requiring complex multi-step planning. These findings inform architectural decisions: reflection loops provide marginal accuracy gains at disproportionate cost and latency penalties.

References
Beetz and Riedl (2019)
Beetz, R., and Riedl, Y.2019.Robotic Process Automation: Developing a Multi-Criteria Evaluation Model for the Selection of Automatable Business Processes.In AMCIS 2019 Proceedings, volume 4.
Chen et al. (2024)
Chen, J.; Lu, Y.; Wang, X.; Zeng, H.; et al.2024.Multi-Agent-as-Judge: Aligning LLM-Agent-Based Automated Evaluation with Multi-Dimensional Human Evaluation.arXiv preprint arXiv:2507.21028.
Chiu (2025)
Chiu, O.2025.The Key to Production AI Agents: Evaluations.Databricks Blog.
Deng et al. (2023)
Deng, X.; Gu, Y.; Zheng, B.; Chen, S.; Stevens, S.; Wang, B.; Sun, H.; and Su, Y.2023.Mind2Web: Towards a Generalist Agent for the Web.In NeurIPS Datasets and Benchmarks Track.
Drouin et al. (2024)
Drouin, A.; Gasse, M.; Caccia, M.; Laradji, I. H.; Del Verme, M.; Marty, T.; Boisvert, L.; Thakkar, M.; Cappart, Q.; Vazquez, D.; et al.2024.WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?arXiv preprint arXiv:2403.07718.
Jimenez et al. (2024)
Jimenez, C. E.; Yang, J.; Wettig, A.; Yao, S.; Pei, K.; Press, O.; and Narasimhan, K.2024.SWE-bench: Can Language Models Resolve Real-World GitHub Issues?In International Conference on Learning Representations (ICLR).
Kang et al. (2024)
Kang, D., et al.2024.AI Agent Benchmarks Are Broken: A Critical Analysis.Technical Report.
Kapoor et al. (2024)
Kapoor, S.; Stroebl, B.; Pandit, S.; Bommasani, R.; and Narayanan, A.2024.AI Agents That Matter.arXiv preprint arXiv:2407.01502.
Liu et al. (2023a)
Liu, X.; Yu, H.; Zhang, H.; Xu, Y.; Lei, X.; Lai, H.; Gu, Y.; Ding, H.; Men, K.; Yang, K.; et al.2023a.AgentBench: Evaluating LLMs as Agents.In International Conference on Learning Representations (ICLR).
Liu et al. (2023b)
Liu, Y.; Iter, D.; Xu, Y.; Wang, S.; Xu, R.; and Zhu, C.2023b.G-eval: NLG Evaluation using GPT-4 with Better Human Alignment.In Conference on Empirical Methods in Natural Language Processing (EMNLP).
Liu et al. (2024)
Liu, J.; Zhang, K.; Chen, W.; Alkhouli, T.; Negrinho, R.; Elluru, V. R.; Benajiba, Y.; et al.2024.Towards Effective GenAI Multi-Agent Collaboration: Design and Evaluation for Enterprise Applications.arXiv preprint arXiv:2412.05449.
Mialon et al. (2023)
Mialon, G.; Fourrier, C.; Swift, C.; Wolf, T.; LeCun, Y.; and Scialom, T.2023.GAIA: A Benchmark for General AI Assistants.arXiv preprint arXiv:2311.12983.
Patil et al. (2024)
Patil, S. G.; Yan, F.; Mao, H.; Ji, C. C.-W.; Zhang, T.; Stoica, I.; and Gonzalez, J. E.2024.Gorilla: Large Language Model Connected with Massive APIs.Berkeley Function Calling Leaderboard.
Qin et al. (2024)
Qin, Y.; Liang, S.; Ye, Y.; Zhu, K.; Yan, L.; Lu, Y.; Lin, Y.; Cong, X.; Tang, X.; Qian, B.; et al.2024.ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs.In International Conference on Learning Representations (ICLR).
Aisera Research Team (2024)
Aisera Research Team.2024.CLASSic: A Holistic Framework for Evaluating Enterprise AI Agents.Aisera Technical Report.
Salesforce AI Research (2024)
Salesforce AI Research.2024.First-Of-Its-Kind LLM Benchmark Ranks Generative AI Against Real-World Business Tasks.Salesforce Blog.
Samsung Research (2024)
Samsung Research.2024.TRUEBench: Trustworthy Real-world Usage Evaluation Benchmark for Enterprise LLMs.Samsung AI Research.
Schick et al. (2023)
Schick, T.; Dwivedi-Yu, J.; Dessì, R.; Raileanu, R.; Lomeli, M.; Zettlemoyer, L.; Cancedda, N.; and Scialom, T.2023.Toolformer: Language Models Can Teach Themselves to Use Tools.In NeurIPS.
Shinn et al. (2023)
Shinn, N.; Cassano, F.; Gopinath, A.; Narasimhan, K.; and Yao, S.2023.Reflexion: Language Agents with Verbal Reinforcement Learning.In NeurIPS.
Xie et al. (2024)
Xie, T.; Zhang, D.; Chen, J.; Li, X.; Zhao, S.; Cao, R.; Hua, T. J.; Shin, D.; Lei, F.; Liu, Y.; et al.2024.OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments.In NeurIPS Datasets and Benchmarks Track.
Yang et al. (2023)
Yang, J.; Prabhakar, A.; Narasimhan, K.; and Yao, S.2023.InterCode: Standardizing and Benchmarking Interactive Coding with Execution Feedback.In NeurIPS Datasets and Benchmarks Track.
Yao et al. (2023)
Yao, S.; Zhao, J.; Yu, D.; Du, N.; Shafran, I.; Narasimhan, K.; and Cao, Y.2023.ReAct: Synergizing Reasoning and Acting in Language Models.In International Conference on Learning Representations (ICLR).
Yao et al. (2024)
Yao, S.; Hu, J.; Shinn, N.; and Narasimhan, K.2024.
τ
-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.arXiv preprint arXiv:2406.12045.
Yehudai et al. (2025)
Yehudai, A.; Eden, L.; Li, A.; Uziel, G.; Zhao, Y.; Bar-Haim, R.; Cohan, A.; and Shmueli-Scheuer, M.2025.Survey on Evaluation of LLM-based Agents.arXiv preprint arXiv:2503.16416.
Zhang et al. (2024)
Zhang, Z., et al.2024.Agent-SafetyBench: Evaluating the Safety of LLM Agents.arXiv preprint arXiv:2412.14470.
Zhou et al. (2023)
Zhou, S.; Xu, F. F.; Zhu, H.; Zhou, X.; Lo, R.; Sridhar, A.; Cheng, X.; Bisk, Y.; Fried, D.; Alon, U.; et al.2023.WebArena: A Realistic Web Environment for Building Autonomous Agents.In Advances in Neural Information Processing Systems, volume 36.
