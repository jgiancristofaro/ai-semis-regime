# Is AI compute demand entering a new step-change regime (Nov 2026)? RSI / AI-accelerated AI R&D and multi-agent "swarms" beyond software engineering

Method note: The session's network blocked direct page fetches (metr.org, cnbc.com and gigazine.net all failed DNS resolution). Every finding below therefore comes from search-engine result summaries of the cited pages, not from reading the full documents. Figures should be checked against the primary pages before anyone relies on them in a publication. Where the summaries flagged conflicts or secondary-only sourcing, that is noted inline. Research date: 2026-11-15.

## 1. Agentic token consumption and inference demand in 2026; compute per multi-agent workflow vs. a chatbot query

### Takeaway
Company-disclosed token volumes grew roughly 5-7x year over year in 2026: Google about 7x, Microsoft about 5x. Anthropic's revenue run-rate went from about $9B at end-2025 to about $65B by end-July 2026, roughly 7x, which is a bigger step-change than the late-2025 "Claude Code moment". Agentic and multi-agent tasks use roughly 4-15x the tokens of a chat turn (Anthropic's own figures), and some third-party estimates go much higher.

### Cited Findings
**Token volumes**
- At Google I/O in May 2026, Sundar Pichai said Google processes about 3.2 quadrillion tokens per month, about 7x the prior year's ~480T. Google model APIs handle about 19B tokens per minute, and more than 8.5M developers use Google AI monthly. — [GIGAZINE, 2026-05-20](https://gigazine.net/gsc_news/en/20260520-google-monthly-tokens-processed/); [keepingupwith.ai](https://keepingupwith.ai/articles/googles-agentic-gemini-era-token-consumption-surges-to-32-quadrillion-monthly/)
- On a later Alphabet earnings call, API throughput was reported at about 22B tokens per minute, up from 16B a quarter earlier. More than 375 Google Cloud customers each processed more than 1T tokens over the past year. — [ai.blocksize.hr summary of Alphabet call](https://ai.blocksize.hr/blog/en/ai-token-usage-growth-2026) (secondary; verify against the transcript)
- Microsoft: Nadella reportedly said Microsoft processed more than 100T tokens in the quarter, about 5x YoY (April 2026 call). Foundry customers running at a 1T-token annualized rate grew 4x YoY (July 2026 call). — [I/O Fund / Beth Kindig](https://io-fund.com/ai-stocks/ai-token-demand-shattering-forecasts) (secondary)
- Goldman Sachs (May 2026, as cited by a secondary source) projected that global monthly token consumption rises 24x from 2026 to 2030, to about 120 quadrillion per month, with agentic workloads more than 80% of the total. — [I/O Fund](https://io-fund.com/ai-stocks/ai-token-demand-shattering-forecasts) (secondary citation of Goldman)
- Caveat: "tokens processed" is defined differently by each company. Google's figure includes consumer product distribution (Search/AI Overviews), not only paid API inference. — [ai.blocksize.hr](https://ai.blocksize.hr/blog/en/ai-token-usage-growth-2026)

**Lab revenue run-rates (a proxy for paid inference demand)**
- Anthropic told investors its annualized run-rate reached about $65B at end-July 2026, about 7x YoY. Milestones were about $9B at end-2025, about $14B in February 2026, more than $30B in April, more than $47B in May, and about $65B in July. — [CNBC, 2026-08-17](https://www.cnbc.com/2026/08/17/anthropic-says-annualized-revenue-climbed-to-65-billion-in-july.html); [Yahoo Finance](https://finance.yahoo.com/technology/ai/articles/anthropic-run-rate-hits-65-032555081.html)
- OpenAI's run-rate was reported at about $40B in mid-August 2026. One report puts it at about $50B in October 2026, which was not confirmed. Yahoo reported Anthropic about $25B ahead of OpenAI. — [Yahoo Finance](https://finance.yahoo.com/technology/ai/articles/anthropic-run-rate-hits-65-032555081.html); [explodingtopics](https://explodingtopics.com/blog/anthropic-revenue) (aggregator)
- Run-rate is not recognized revenue. — [valueaddvc](https://valueaddvc.com/blog/anthropic-revenue-hits-47b-run-rate-how-it-passed-openai-in-just-five-months)
- **The "Claude Code moment" as a baseline:** Claude Code's run-rate was more than $500M in September 2025, about $1B in November 2025, and more than $2.5B on 2026-02-12 (per Anthropic). A secondary claim of $8B by May 2026 has no primary source. — [Enterprise DNA](https://enterprisedna.co/resources/news/claude-code-25-billion-arr-anthropic-2026/); [gradually.ai](https://www.gradually.ai/en/claude-code-statistics/)

**Multiplier per workflow**
- Anthropic's June 2025 engineering write-up on its multi-agent research system put single-agent use at about 4x the tokens of a chat interaction and multi-agent (orchestrator plus parallel subagents) at about 15x. — cited via [getnadir.com](https://getnadir.com/blog/multi-agent-orchestration-15x-token-cost/) (secondary; the primary is Anthropic's "How we built our multi-agent research system", June 2025)
- Gartner (March 2026, secondhand) is cited as saying agentic models need 5-30x more tokens per task than standard chatbots. One agentic task can trigger 10-20 model calls. — [Spheron](https://www.spheron.network/blog/agentic-ai-inference-cost-2026/) (secondary)
- Rough third-party estimates: complex multi-agent tasks use 200K to more than 1M tokens per task, and SWE-bench-style coding agents cost up to about 1000x a simple code chat. These look like estimates, not measurements. — [getnadir.com](https://getnadir.com/blog/multi-agent-orchestration-15x-token-cost/); [cloudzero](https://www.cloudzero.com/blog/agentic-ai-cost/)
- Jensen Huang (GTC, March 2026) said the shift from chatbots to agentic apps has made tokens generated "explode". At Q1 FY27 (2026-05-20) he said "Agentic AI has arrived" and called demand "parabolic". — [CNBC GTC, 2026-03-16](https://www.cnbc.com/2026/03/16/nvidia-gtc-2026-ceo-jensen-huang-keynote-blackwell-vera-rubin.html); [CNBC Q1 FY27, 2026-05-20](https://www.cnbc.com/2026/05/20/nvidia-nvda-earnings-report-q1-2027.html)

### Inferences
- Token volume at the largest platforms is growing about 5-7x per year, faster than accelerator installed base (roughly 2x per year in capex terms). That gap is consistent with reports of compute scarcity, and with tokens per FLOP rising through efficiency gains.
- Anthropic's roughly 7x run-rate increase in seven months of 2026 is several times larger than the Claude Code-only step in late 2025 (about $1B to $2.5B). The "Claude Code moment" appears to have generalized into a company-wide agentic step-change rather than fading.
- If agentic tasks are about 15x a chat turn and agentic work grows from a small to a dominant share of usage (Goldman cites more than 80% by 2030), the mix shift alone supports multi-x growth in inference compute even before user growth.

### Gaps
- No primary OpenRouter 2026 token totals were retrieved. A "250x growth" claim appears only on a blog.
- No audited, like-for-like cross-company token series exists. Microsoft's July/October 2026 token figures were not confirmed.
- I could not find a 2026 primary Anthropic or OpenAI disclosure of tokens per agentic session for non-coding work.

## 2. Agent swarms spreading from software engineering to non-technical knowledge work

### Takeaway
There is credible early evidence of a spread. OpenAI's own telemetry shows Legal, Finance and Recruiting adopting Codex/agent tools faster than Engineering by mid-2026. Anthropic made Cowork ("Claude Code for the rest of your work") generally available in April 2026. Surveys show single-agent deployment is common at large firms, but orchestrated multi-agent "swarms" are still a minority, with roughly 15-18% at scale.

### Cited Findings
- OpenAI reports that Legal, Finance and Recruiting made Codex their primary AI tool around April 2026. Weekly active enterprise Codex users in Legal grew about 108x from February to June 2026, versus about 5x in Engineering. This is vendor telemetry, so it is low-base and self-selected. — [OpenAI, "How agents are transforming work"](https://openai.com/index/how-agents-are-transforming-work/)
- Anthropic's Claude Cowork launched as a research preview in January 2026, described as "Claude Code for the rest of your work": the user gives it a folder and assigns multi-step tasks, which run in a sandboxed VM. It became generally available for all paid subscribers on macOS and Windows on 2026-04-09. — [Linas Substack, 2026 launch guide](https://linas.substack.com/p/anthropic-claude-2026-every-launch-guide) (secondary)
- KPMG data (via a roundup): 53% of $1B+ revenue companies report agents deployed, and 18% are orchestrating multi-agent systems. Finance-function agent deployment reportedly rose from 10% to 60% in one quarter (Q2 to Q3 2026), but that sample is narrow (tech leaders). — [Joget](https://joget.com/ai-agent-adoption-in-2026-what-the-analysts-data-shows/); [axis-intelligence](https://axis-intelligence.com/agentic-ai-adoption-statistics/) (secondary)
- In a Deloitte survey of 121 senior legal leaders, only 15% said their organization had scaled orchestrated, cross-functional multi-agent adoption. 75% of executives say human plus agent collaboration beats agent-only automation. — via [Joget](https://joget.com/ai-agent-adoption-in-2026-what-the-analysts-data-shows/)
- Forrester and Gartner both frame 2026 as the breakthrough year for multi-agent systems, meaning specialized agents under central orchestration. — [Joget](https://joget.com/ai-agent-adoption-in-2026-what-the-analysts-data-shows/)
- The World Economic Forum published "The AI Playbook for Financial Services 2026". Regulation is cited as slowing adoption in finance. — [WEF](https://reports.weforum.org/docs/WEF_The_AI_Playbook_for_Financial_Services_2026.pdf); [First Page Sage](https://firstpagesage.com/reports/agentic-ai-adoption-statistics/)
- Agentic EDA is a knowledge-work vertical adjacent to semis. At DAC 2026, Synopsys announced fully autonomous, long-running agentic design workflows; it puts itself at "L3" on an L1-L5 autonomy ladder and claims up to 50x faster RTL validation. Cadence launched the ChipStack and AuraStack agents. Siemens added self-verifying Fuse agents. — [Tom's Hardware](https://www.tomshardware.com/tech-industry/semiconductors/the-state-of-agentic-ai-in-chip-design-tools-in-2026-cadence-synopsys-and-siemens-all-pitch-autonomous-engineers); [Futurum](https://futurumgroup.com/insights/synopsys-cadence-and-siemens-take-agentic-chip-design-autonomous-at-dac/)

### Inferences
- The pattern looks like the early phase of the coding step-change: vendor telemetry shows hyper-growth from a low base, while broad enterprise surveys show multi-agent at scale in under 20% of organizations. That implies most of the token upside from non-technical swarms is still ahead (2027-2028) rather than priced into current usage.
- Non-coding knowledge workers far outnumber software engineers. If even a fraction move to multi-agent workflows at 4-15x chat token intensity, the inference demand is larger than the coding wave. This is speculative and rests on the multipliers in section 1 holding.

### Gaps
- No McKinsey State of AI 2026, Menlo Ventures 2026 or a16z 2026 enterprise survey figures were retrieved.
- No Cowork usage or token statistics were found.
- Gartner's primary 2026 agentic forecasts were not verified.

## 3. RSI and AI-accelerated AI R&D: is it real and quantifiable?

### Takeaway
The most credible quantitative evidence is METR's 2026-11-05 independent assessment of Anthropic. It found interviews and surveys "consistent with AI usage causing a doubling in the pace of capabilities progress", mostly through AI assistance rather than autonomous contributions. METR's Time Horizon 1.1 shows doubling times shortening to about 89 days since 2024 (about 131 days post-2023). Lab leaders openly say they are pursuing RSI, but METR cautions that longer time horizons do not translate linearly into automation of research.

### Cited Findings
- METR, "Independent Assessment of AI R&D Acceleration at Anthropic in October 2026" (2026-11-05):
  - Interviews and surveys are consistent with roughly a 2x speedup in the pace of capabilities progress.
  - Acceleration comes primarily through AI assistance, though there are "some signs that fully autonomous contributions will play a larger role soon".
  - Across 9 other benchmarks, improvement rates are similar to the 7-month doubling.
  - — [METR](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/) (search summary only; the full text could not be fetched)
- Ryan Greenblatt, as quoted by Zvi Mowshowitz, read the report as RSI currently speeding AI progress by about 2x, and the post is titled "AI R&D Is Accelerating Towards Potential RSI in 2027". This is commentary. — [Zvi Mowshowitz Substack](https://thezvi.substack.com/p/ai-r-and-d-is-accelerating-towards?r=67wny)
- METR Time Horizon 1.1 (2026-01-29): the post-2023 doubling time is about 131 days (versus 165 under TH1), and the doubling time since 2024 is about 89 days. The long-run hybrid trend stays at about 196 days (7 months). — [METR TH1.1](https://metr.org/blog/2026-01-29-time-horizon-1-1/)
- METR (2026-01-22) warns that doubling the time horizon does not double the degree of automation, and that human-baseline conventions can shift horizons by more than 1.25x. — [METR limitations note](https://metr.org/notes/2026-01-22-time-horizon-limitations/)
- A LessWrong analysis ("METR Time Horizons: Now 10x/Year") argues the faster pace may revert toward 7-month doublings by end-2026. This is one commentator's view. — [LessWrong](https://www.lesswrong.com/posts/EYb2K9acKfyG2bome/metr-time-horizons-now-10x-year)
- Demis Hassabis (May 2026): "all the leading labs are quite focused on recursively self-improving AI". — via [Noahpinion](https://www.noahpinion.blog/p/should-we-pace-ai-self-improvement) (secondary)
- Dario Amodei reportedly said in January 2026 that automating AI research may be only 1-2 years away. He wrote that RSI "must be pursued very carefully, if at all", and on 2026-09-12 argued for slowing capability gains when safeguards lag. — [Business Standard](https://www.business-standard.com/technology/tech-news/why-altman-musk-and-amodei-want-to-slow-the-ai-race-126091400087_1.html); [Noahpinion](https://www.noahpinion.blog/p/should-we-pace-ai-self-improvement)
- Sam Altman: OpenAI's stated goal is a "true automated AI researcher" by March 2028. He said "it's very hard to say what a ban on RSI means". — [Noahpinion](https://www.noahpinion.blog/p/should-we-pace-ai-self-improvement); [LessWrong on RSI bans](https://www.lesswrong.com/posts/ZT2rKu3Z6RaargYYF/what-is-recursive-self-improvement-and-what-would-it-mean-to)
- Peter Wildeford interviewed 25 AI researchers. They disagreed on whether there is a clear continuous trajectory to automated AI research, but many believe RSI is a few years away. — [Wildeford blog](https://blog.peterwildeford.com/p/interviewing-25-ai-researchers-about)
- 2026 academic work on AI4AI (e.g. Frontis-MA1, "Recursive self-improvement of AI research agents") is active but shows no field-level effect. — [arXiv 2607.28568](https://arxiv.org/pdf/2607.28568); [arXiv 2609.26457](https://arxiv.org/pdf/2609.26457)
- Chip design: an agentic-EDA survey says no LLM agent has yet done a fully human-free industrial tape-out, although RL systems like AlphaChip have reached industrial tape-out. TSMC partners announced agentic flows for A14 in September 2026. — [arXiv 2512.23189](https://arxiv.org/pdf/2512.23189); [TechWire Asia, 2026-09](https://techwireasia.com/2026/09/what-is-agentic-ai-chip-design-tsmc-partners/)

### Inferences
- RSI's compute implication is mostly additive demand. A lab that gets about 2x research speed from AI runs many internal agents, which consume inference compute, and it can explore more experiments, which consume training compute. Labs therefore have strong incentive to buy more compute, not less. Compute becomes the binding input once researcher labor is partly automated.
- If research progress is about 2x faster, efficiency gains (kernels, architectures) also arrive faster. That lowers cost per token, which historically has expanded usage (Jevons). The net hardware effect therefore depends on demand elasticity, and so far elasticity has been strongly positive (tokens about 7x vs. prices down).
- RSI is a real but early signal. The evidence is one lab, assessed through interviews, with no autonomous research loop yet. Treat a "2027 takeoff" as speculation.

### Gaps
- I could not retrieve the full METR report for its precise speedup ranges or compute caveats.
- I found no 2026 data on NVIDIA's internal use of AI for GPU design, AlphaChip's 2026 status, or AlphaEvolve kernel and efficiency results.
- I found no Epoch AI 2026 quantification of AI-R&D acceleration.

## 4. Counter-evidence: efficiency, price declines, ROI, plateaus

### Takeaway
Bearish evidence centers on enterprise ROI and a price war. I found no evidence of falling aggregate demand. Token prices are falling fast (below $1/M tokens in August 2026), and GPU utilization at enterprises is often low. However, rental prices for leading GPUs rose and token volume growth far outpaces price declines.

### Cited Findings
- Inference unit prices fell below $1 per million tokens for the first time in August 2026, more than 50% below a May peak. Silicon Data cautions this may reflect list cuts or a shift to open models rather than lower usage. Goldman reportedly warned that compute oversupply undermines capex fundamentals. — [BigGo Finance](https://finance.biggo.com/news/8a9ab26e-9958-41db-92b7-51645a29ca08) (secondary; the Goldman warning is unverified)
- In a 2026 survey reported by VentureBeat, 79% of companies running AI in production say their GPUs sit idle at least half the time, yet most still plan new AI platforms. — [VentureBeat](https://venturebeat.com/infrastructure/ai-bubble-update-79-of-companies-say-their-gpus-sit-idle-at-least-half-the-time-yet-most-plan-new-ai-platforms)
- MIT's 2025 GenAI Divide study found most enterprise GenAI pilots show no measurable P&L impact within six months. Writer's 2026 survey found only 29% of organizations see significant ROI. Forbes (2026-06-11) describes a "vicious price war". — [Forbes](https://www.forbes.com/sites/petercohan/2026/06/11/the-ai-bubble-isnt-bursting-but-a-vicious-price-war-is-here/)
- Counterpoint: a CFA Institute author who tried to prove a bubble found that H100 one-year contract prices recovered from their late-2025 low and B200 pricing rose sharply. — [CFA Institute, 2026](https://rpc.cfainstitute.org/blogs/enterprising-investor/2026/i-tried-to-prove-ai-was-a-bubble)
- An efficiency argument (fewer GPUs for the same workloads) appears only as blog commentary. — [explainx](https://www.explainx.ai/blog/ai-bubble-2026-reality-check)
- Q3 2026 earnings: Google and Microsoft held off on raising capex forecasts, which CNBC framed as a "snag". Microsoft said spending accelerates in 1H 2027 because of higher component costs and delayed deliveries, which signals a supply constraint rather than weak demand. — [CNBC, 2026-10-29](https://www.cnbc.com/2026/10/29/microsoft-google-ai-capex-estimates.html)
- NVIDIA shares slid after its strong Q1 FY27 report, which suggests the market already priced high expectations. — [CNBC, 2026-05-20](https://www.cnbc.com/2026/05/20/nvidia-nvda-earnings-report-q1-2027.html)

### Inferences
- Jevons appears to be dominating. Price per token roughly halved within months while volumes grew 5-7x YoY, so dollar inference spend and compute demand still rise.
- The main medium-term risk to hardware demand is not efficiency per se. It is a financing or ROI air-pocket at enterprises and highly levered buyers, which could cause order timing to slip even if long-run demand holds. Low enterprise GPU utilization means on-prem buyers are the most exposed, more than frontier labs and hyperscalers, which report being capacity-short.

### Gaps
- I found no rigorous 2026 data on aggregate compute per task declining, nor on how much distillation and small models offset agentic growth.
- The MIT NANDA 2026 follow-up, if any, was not found.

## 5. Compute supply constraints and signed compute deals (2026)

### Takeaway
Supply is tight into 2027 and beyond. SK hynix says its DRAM and HBM are effectively sold out through 2029. Samsung says 2027 HBM is sold out. Micron says 2027 is largely or entirely sold. CoWoS is estimated to be fully allocated through at least mid-2027. Gigawatt-scale contracts (Anthropic about 3.5 GW of TPU via Broadcom from 2027; OpenAI 10 GW Broadcom, 2 GW Trainium) lock in multi-year demand.

### Cited Findings
- SK hynix told investors that its DRAM and HBM output is effectively sold out through 2029, and that confirmed contracts fill more than 50% of 2027-28 capacity. Samsung says its planned 2027 HBM is sold out at target prices. Micron's COO reportedly said all planned 2027 capacity is sold, though other accounts say "mostly contracted". — [VLSI.kr, 2026-11-01](https://www.vlsi.kr/en/daily-silicon-2026-11-01-en/); [tech-insider](https://tech-insider.org/sk-hynix-sold-out-2029-memory-shortage-2030-pc-shipments-2026/); [TweakTown/DigiTimes](https://www.tweaktown.com/news/113004/memory-capacity-for-all-of-2027-has-reportedly-been-booked-and-sold-with-no-more-dram-or-hbm-available/index.html)
- Caveat: no manufacturer has confirmed that every unit of 2027 DRAM and HBM is sold. — [remio.ai](https://www.remio.ai/post/samsung-sk-hynix-and-micron-reportedly-sell-out-2027-memory-supply)
- TSMC CoWoS is estimated as sold out or fully allocated through at least mid-2027, but TSMC publishes no CoWoS capacity figure, so all such numbers are models. — [siliconanalysts](https://siliconanalysts.com/market); [ravikant.dev](https://ravikant.dev/research/investments/universe/hbm-capacity)
- SK hynix plans its first US 2.5D packaging plant for HBM ($3.9B). — [Tom's Hardware](https://www.tomshardware.com/tech-industry/sk-hynix-to-build-first-us-2-5d-packaging-plant-for-hbm)
- Broadcom 8-K (April 2026): Anthropic can access about 3.5 GW of next-gen TPU capacity via Broadcom from 2027, with consumption tied to Anthropic's commercial success. It also covers a Google TPU supply agreement through 2031. Anthropic itself gave no GW figure, and some outlets say 5 GW. — [SEC 8-K](https://www.sec.gov/Archives/edgar/data/1730168/000119312526144028/d87999d8k.htm); [Anthropic](https://www.anthropic.com/news/google-broadcom-partnership-compute); [TechCrunch, 2026-04-07](https://techcrunch.com/2026/04/07/anthropic-compute-deal-google-broadcom-tpus/)
- This expands Anthropic's October 2025 deal for up to 1M TPUs (more than 1 GW in 2026). Meta has about 1 GW of Broadcom custom chips (April 2026). — [Tom's Hardware ASIC state of play, May 2026](https://www.tomshardware.com/tech-industry/semiconductors/custom-ai-asics-examined-from-broadcom-to-mtia)
- OpenAI has 10 GW of Broadcom custom accelerators (first deployment in 2H 2026) and 2 GW of AWS Trainium. Its total signed deals are reportedly about 26 GW and more than $1T, which is unverified. — [hashrateindex](https://hashrateindex.com/blog/hyperscaler-ai-asic-market-report-part-1/); [mlq.ai](https://mlq.ai/news/googles-anthropic-compute-buildout-splits-risk-among-broadcom-wall-street-and-data-center-developers/)
- NVIDIA: at GTC in March 2026, Huang said Blackwell plus Vera Rubin purchase orders reach $1T through 2027, up from $500B through 2026. That excludes Rubin Ultra, Feynman, standalone Vera and Groq, and he later called it a floor. NVIDIA's revenue opportunity per GW is about $18B for Hopper, $25B for Blackwell and $40B for Vera Rubin (Q2 FY27 call, 2026-08-26). Rubin ships in 2H 2026 and reaches full scale in 1H 2027. — [CNBC GTC](https://www.cnbc.com/2026/03/16/nvidia-gtc-2026-ceo-jensen-huang-keynote-blackwell-vera-rubin.html); [Yahoo Finance](https://finance.yahoo.com/sectors/technology/articles/nvidia-conference-huang-sees-agentic-101054514.html); [NVDA Q2 FY27 transcript](https://s201.q4cdn.com/141608511/files/content_files/TRANSCRIPT_-NVIDIA-Corp-NVDA-US-Q2-2027-Earnings-Call-26-August-2026-5_00-PM-ET.pdf); [BigGo](https://finance.biggo.com/news/xmOaSJ4BrX5PFN7B0Zbg)

### Inferences
- Because HBM and CoWoS are booked, a further demand step-change in 2027 would mostly show up as pricing power (HBM and memory ASPs, foundry and packaging pricing) and longer lead times, not as a big upside surprise in units. 2028-2029 capacity decisions are where incremental demand turns into volume.
- Per-GW NVIDIA content rising from $25B to $40B means that even at a fixed GW build rate, dollar silicon demand rises about 60% on the Rubin transition.

### Gaps
- No primary TSMC 2027 CoWoS figures were found. AMD-OpenAI or AMD-Anthropic 2026 deal details did not appear in results.
- No 2026 power or interconnection data were retrieved (IEA 2026 update, US grid queues).
- NVIDIA's Q3 FY27 results (due around late November 2026) are not yet covered.

## 6. Credible forecasts of AI compute and data center spending, 2027-2030; what markets price

### Takeaway
Consensus has the big four hyperscalers spending about $935B in 2027 (+28%). Estimates with Oracle are $1.2-1.3T, and CNBC says more than $1T. Alphabet guides capex to "increase significantly" in 2027. Longer-run forecasts are McKinsey's ~$5.2T in AI data center investment by 2030 (range $3-8T), Goldman's 24x token growth from 2026 to 2030, and Epoch's ~100 GW of US AI power by 2030 if trends hold. A demand regime driven by agents and RSI would push toward the upper ends of these ranges.

### Cited Findings
- **Alphabet:** held its 2026 range at $195-205B and said capex will "increase significantly in 2027" (2026-10-28 call). — [yieldtheory](https://www.yieldtheory.app/research/hyperscaler-capex-2027-forecast); [CNBC, 2026-10-29](https://www.cnbc.com/2026/10/29/microsoft-google-ai-capex-estimates.html)
- **Amazon:** about $220B in 2026. **Meta:** $135-145B, with no 2027 guide yet. **Microsoft:** CNBC reports a cut from $175B to $170B, which another source attributes to lease reclassification; Microsoft expects acceleration in 1H 2027. — [CNBC](https://www.cnbc.com/2026/10/29/microsoft-google-ai-capex-estimates.html); [useluminix](https://www.useluminix.com/reports/industry-analysis/hyperscaler-capex-q3-2026)
- **2027 totals:** the Street sees about $934.5B for the big four (+28%; this predates the October reports). Sell-side estimates including Oracle are $1.2-1.3T. CNBC says capex is expected to top $1T next year. — [yieldtheory](https://www.yieldtheory.app/research/hyperscaler-capex-2027-forecast); [alcapitaladvisory](https://alcapitaladvisory.com/research/intelligence/ai-infrastructure.html); [CNBC](https://www.cnbc.com/2026/10/29/microsoft-google-ai-capex-estimates.html)
- **McKinsey:** about $5.2T in AI data center investment needed by 2030, within a $3-8T range. — [McKinsey](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-cost-of-compute-a-7-trillion-dollar-race-to-scale-data-centers)
- **Epoch AI:**
  - US AI data center power demand could reach about 100 GW by 2030 if trends hold (for comparison, the US industrial sector averaged 120 GW in 2025).
  - Campuses of 1-5 GW are feasible by 2030.
  - Frontier training cost is growing about 3.5x per year.
  - More than 200 models will exceed 1e26 FLOP by 2030.
  - — [Epoch energy](https://epoch.ai/publications/ai-energy); [Epoch scaling 2030](https://epoch.ai/publications/can-ai-scaling-continue-through-2030); [Epoch trends](https://epoch.ai/trends); [Epoch model counts](https://epoch.ai/blog/model-counts-compute-thresholds)
- **AI 2027 compute forecast** (scenario, not consensus): about $600B in AI data center spend in 2026 and $1T in 2027. — [AI 2027](https://ai-2027.com/research/compute-forecast)
- **Revenue gap:** TechRadar reports that buildouts requiring about $6T by 2031 imply very large annual revenue needs, and that enterprise productivity may not cover them. — [TechRadar](https://www.techradar.com/pro/generate-usd6-trillion-in-annual-revenue-or-face-a-major-collapse-ai-data-center-costs-are-doubling-every-12-months)

### Inferences
- **Market pricing vs. demand indicators.** Consensus 2027 capex growth of about 28% looks conservative relative to the demand indicators:
  - tokens growing 5-7x YoY
  - lab run-rates growing about 7x
  - NVIDIA's $1T+ "floor" through 2027
  - memory sold out through 2027-2029

  The binding constraint is supply (HBM, CoWoS, power), not demand. Upside therefore shows up mostly as pricing and margins for the constrained layers (HBM, advanced packaging, leading-edge foundry, power equipment) in 2027, and as volume in 2028. This is analyst inference, not a sourced forecast.
- **Is it a new regime? Evidence vs. speculation.**
  - Evidence: a 2026 agentic step-change that is larger than the late-2025 Claude Code moment (Anthropic about 7x, Google tokens about 7x).
  - Evidence: early but rapid spread of agents to legal and finance in vendor telemetry.
  - Evidence: one credible independent measurement of about 2x AI-R&D speedup at a frontier lab.
  - Speculation: that non-technical swarms reach coding-level intensity by 2027-2028.
  - Speculation: that RSI produces a discontinuous takeoff in 2027.
- **Key bear risks.** Enterprise ROI disappointment and financing stress among levered buyers, which affect order timing. Lab revenue concentration: Anthropic's and OpenAI's run-rates underpin GW-scale contracts tied to their "commercial success".

### Gaps
- No public SemiAnalysis 2027-2028 accelerator or HBM model was retrieved.
- No Goldman primary data center spend forecast was retrieved.
- No IEA 2026 update was retrieved.
- No Stanford AI Index 2026 figures were retrieved.
- No measure of what equity markets explicitly price (e.g. consensus NVDA/TSMC/HBM 2028 revenue) was obtained; this needs a sell-side or consensus data source.
