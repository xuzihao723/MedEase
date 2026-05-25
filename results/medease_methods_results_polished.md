# Polished Methods and Results Text

## Methods: System Trace Logging

To examine whether the adaptive explanation pipeline operated as intended, MedEase recorded a lightweight internal trace for each explanation request. The trace was designed for system-level analysis rather than user surveillance: it did not store the raw medical text or the full generated explanation. Instead, each record contained a hashed input identifier, input length, language indicators, model provider metadata, the predicted cognitive load label and score, semantic complexity features, term and annotation counts, risk level, and the user-interface actions selected for the final presentation.

For each request, the backend first generated a structured plain-language medical explanation using an external LLM service. The English explanation, technical details, and extracted terminology were then passed to the cognitive load classifier. The classifier produced a categorical cognitive load estimate (`low`, `medium`, or `high`), a confidence-like score, and semantic complexity features including readability, term density, sentence length, and information density. These outputs were subsequently mapped to adaptive presentation actions, including whether to show a plain-language summary, activate inline term explanations, collapse technical details, and highlight risk-related guidance. The frontend used these actions to adjust the presentation, but the internal model outputs were not shown to users.

## Results: System Trace Analysis

The current trace file contained **13** logged explanation event(s). The fallback distribution was `none`=13, indicating how often the system returned a normal explanation versus a fallback state. The cognitive load distribution was `high`=7, `medium`=6, and the risk-level distribution was `high`=2, `medium`=11.

Across the logged events, the mean cognitive load score was **0.547414**. The corresponding semantic complexity profile showed a mean readability of **0.000000**, mean term density of **0.185159**, mean sentence length of **154.807692**, and mean information density of **0.208015**. Each explanation contained an average of **3.923** extracted terms, with **3.923** English inline annotations and **3.923** Chinese inline annotations.

The adaptive presentation policy was also observable in the trace data. The system triggered `show_summary` in **1.000** of sessions, `show_inline_terms` in **1.000**, `collapse_technical` in **1.000**, and `highlight_risk` in **1.000**. These results indicate that the interface behavior was linked to the output of the complexity-estimation module rather than being rendered as a fixed static explanation.

Overall, the trace analysis provides system-behavior evidence that the prototype implemented the intended pipeline: the LLM generated explanation content, the cognitive load model estimated explanation difficulty from the generated text, and the frontend adapted the explanation format accordingly. Because the current trace set is small, these descriptive statistics are reported as an implementation check rather than as evidence of end-user benefit. Direct claims about reduced user cognitive load should be supported by human-subject evaluation rather than by internal traces alone.
