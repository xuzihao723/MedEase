const APP_MODE = window.MEDEASE_API_MODE || "mock";
const API_ENDPOINT = window.MEDEASE_API_ENDPOINT || "/api/explain";
const STORAGE_KEY = "medease:sessions";
const LANGUAGE_KEY = "medease:language";

const text = {
  en: {
    appTitle: "MedEase",
    subtitle: "Understand medical information in plain language.",
    history: "History",
    inputTitle: "What medical text do you want to understand?",
    inputHelp: "Paste a test result, doctor's note, medication instruction, or medical AI response.",
    inputPlaceholder: "Paste medical text here...",
    privacy: "Please avoid entering names, phone numbers, ID numbers, or other personal information.",
    explain: "Explain this",
    clear: "Clear",
    examples: "Examples",
    emptyTitle: "Your explanation will appear here.",
    emptyText: "Paste medical text and click Explain this to get a plain-language explanation.",
    loadingTitle: "Generating a clearer explanation...",
    loadingText: "Analyzing clinical terminology and preparing a simpler explanation.",
    safetyTitle: "Important",
    plain: "In plain language",
    explanation: "Explanation",
    terms: "Terms explained",
    watch: "What to watch for",
    next: "What you can do next",
    detail: "More medical detail",
    trust: "AI-generated explanation for understanding only. It may be incomplete or incorrect.",
    feedbackTitle: "Was this explanation clear?",
    understand: "I understand this",
    helpful: "This was helpful",
    confused: "I am still confused",
    thanks: "Thanks. Your feedback has been recorded.",
    confusedToast: "Thanks for your feedback. Medical information can be complex. If this is about your own health, please discuss it with a qualified clinician.",
    showMore: "Show more",
    showLess: "Show less",
    close: "Close",
    previous: "Previous explanations",
    previousCopy: "Review explanations you generated earlier.",
    all: "All",
    needsAttention: "Needs attention",
    stillConfusing: "Still confusing",
    noHistory: "No previous explanations yet.",
    newExplanation: "New explanation",
    back: "Back",
    backHistory: "Back to history",
    open: "Open",
    delete: "Delete",
    clearHistory: "Clear history",
    exportJson: "Export JSON",
    details: "Explanation details",
    original: "Original text",
    notFound: "This explanation could not be found.",
    tryAgain: "Try again",
    useExample: "Use an example",
    emptyInput: "Please paste or type some medical text first.",
    tooShort: "This is too brief to generate a structured explanation. Please add more context, such as symptoms, test results, duration, or a doctor's note.",
    nonMedical: "This does not look like medical text. Please paste a test result, doctor's note, medication instruction, or medical AI response.",
    apiError: "We could not generate an explanation right now. Please try again or use one of the examples.",
    charCount: "characters",
    created: "Created",
    inputPreview: "Input",
    summaryPreview: "Summary",
    feedback: "Feedback",
    pending: "Pending",
    understood: "Understood",
    helpfulStatus: "Helpful",
    confusedStatus: "Still confusing",
    riskLow: "General awareness",
    riskMedium: "Worth discussing with a clinician",
    riskHigh: "Seek medical care promptly",
    whyMatters: "Why it matters",
    noTerms: "No medical terms were detected, so this explanation is shown without term highlights.",
    serviceUnavailable: "Service unavailable",
    contextRequired: "Context required",
  },
  zh: {
    appTitle: "MedEase",
    subtitle: "用更容易理解的方式阅读医学信息。",
    history: "历史",
    inputTitle: "你想看懂哪段医学内容？",
    inputHelp: "粘贴检查报告、医生回复、用药说明或医学 AI 回复。",
    inputPlaceholder: "在这里粘贴医学文本……",
    privacy: "请尽量不要输入姓名、手机号、身份证号等个人敏感信息。",
    explain: "帮我解释",
    clear: "清空",
    examples: "示例",
    emptyTitle: "解释会显示在这里。",
    emptyText: "粘贴医学文本并点击帮我解释，即可获得更容易理解的说明。",
    loadingTitle: "正在生成更容易理解的解释……",
    loadingText: "正在分析医学术语，并准备更通俗的说明。",
    safetyTitle: "重要提示",
    plain: "简单来说",
    explanation: "解释",
    terms: "这些词是什么意思",
    watch: "你需要关注什么",
    next: "接下来可以做什么",
    detail: "专业细节",
    trust: "此解释由 AI 生成，仅用于帮助理解，可能存在不完整或不准确之处。",
    feedbackTitle: "这个解释清楚吗？",
    understand: "我看懂了",
    helpful: "这个解释有帮助",
    confused: "我还不太明白",
    thanks: "感谢反馈，已记录。",
    confusedToast: "感谢反馈。医学信息有时确实比较复杂。如果这与你自己的健康有关，请尽量携带报告咨询专业医生。",
    showMore: "展开",
    showLess: "收起",
    close: "关闭",
    previous: "历史解释",
    previousCopy: "查看之前生成过的解释。",
    all: "全部",
    needsAttention: "需要关注",
    stillConfusing: "仍不清楚",
    noHistory: "还没有历史解释。",
    newExplanation: "新的解释",
    back: "返回",
    backHistory: "返回历史",
    open: "打开",
    delete: "删除",
    clearHistory: "清空历史",
    exportJson: "导出 JSON",
    details: "解释详情",
    original: "原始文本",
    notFound: "未找到这次解释记录。",
    tryAgain: "重试",
    useExample: "使用示例",
    emptyInput: "请先粘贴或输入一段医学内容。",
    tooShort: "这段内容太短，无法生成结构化医学解释。请补充症状、检查结果、持续时间或医生说明等信息。",
    nonMedical: "这看起来不像医学文本。请粘贴检查报告、医生回复、用药说明或医学 AI 回复。",
    apiError: "暂时无法生成解释。请稍后重试，或使用一个示例。",
    charCount: "字符",
    created: "创建时间",
    inputPreview: "输入",
    summaryPreview: "摘要",
    feedback: "反馈",
    pending: "待反馈",
    understood: "已看懂",
    helpfulStatus: "有帮助",
    confusedStatus: "仍不清楚",
    riskLow: "一般关注",
    riskMedium: "建议咨询医生",
    riskHigh: "建议尽快线下就医",
    whyMatters: "为什么重要",
    noTerms: "未检测到医学术语，因此本次解释不显示术语高亮。",
    serviceUnavailable: "服务暂不可用",
    contextRequired: "需要更多信息",
  },
};

const examples = [
  {
    id: "blood-test-anemia",
    label: { en: "Blood test result", zh: "血液检查结果" },
    session: {
      input_text: {
        en: "Your hemoglobin level is 11.2 g/dL, which is slightly below the normal reference range of 12.0-15.5 g/dL. This finding is consistent with mild anemia.",
        zh: "你的血红蛋白水平为 11.2 g/dL，略低于 12.0-15.5 g/dL 的正常参考范围。该结果与轻度贫血相符。",
      },
      summary: {
        en: "Your blood test suggests mild anemia. This means your blood may be carrying a little less oxygen than usual, but this single result should be discussed with a clinician.",
        zh: "这项血液检查提示可能存在轻度贫血。也就是说，血液携带氧气的能力可能略低于平时，但单项结果仍需要和医生讨论。",
      },
      explanation: {
        en: "Hemoglobin is a protein in red blood cells that carries oxygen. A value of 11.2 g/dL is slightly below the listed reference range, so the report describes it as mild anemia. Mild anemia can be related to iron deficiency, blood loss, chronic inflammation, or other causes. The result should be interpreted together with symptoms and other blood test values.",
        zh: "血红蛋白是红细胞中负责携带氧气的蛋白质。11.2 g/dL 略低于报告中的参考范围，所以报告将其描述为轻度贫血。轻度贫血可能与缺铁、失血、慢性炎症或其他原因有关。这个结果需要结合症状和其他血液检查指标一起判断。",
      },
      terms: [
        {
          id: "hemoglobin",
          term: { en: "Hemoglobin", zh: "血红蛋白" },
          definition: { en: "A protein in red blood cells that carries oxygen.", zh: "红细胞中负责携带氧气的蛋白质。" },
          why_it_matters: { en: "Low levels may reduce oxygen delivery and can be related to anemia.", zh: "水平偏低可能影响身体供氧，并可能与贫血有关。" },
        },
        {
          id: "red-blood-cells",
          term: { en: "red blood cells", zh: "红细胞" },
          definition: { en: "Blood cells that help carry oxygen through the body.", zh: "帮助把氧气运输到全身的血细胞。" },
          why_it_matters: { en: "They are central to understanding anemia and oxygen delivery.", zh: "它们是理解贫血和身体供氧情况的关键。" },
        },
        {
          id: "anemia",
          term: { en: "anemia", zh: "贫血" },
          definition: { en: "A condition where the blood may not carry enough oxygen.", zh: "血液携带氧气能力不足的一类情况。" },
          why_it_matters: { en: "It can cause tiredness, dizziness, shortness of breath, or weakness.", zh: "可能导致乏力、头晕、气短或虚弱。" },
        },
      ],
      technical_details: {
        en: "Hemoglobin should be interpreted with hematocrit, red blood cell count, mean corpuscular volume, ferritin, and clinical symptoms. A mild isolated decrease does not identify the cause by itself.",
        zh: "血红蛋白需要结合红细胞压积、红细胞计数、平均红细胞体积、铁蛋白以及临床症状一起判断。单独的轻度降低不能直接说明病因。",
      },
      risk: {
        level: "medium",
        reason: {
          en: "This is worth discussing with a clinician, especially if you have fatigue, dizziness, shortness of breath, chest discomfort, or heavy bleeding.",
          zh: "建议与医生讨论，尤其是伴有乏力、头晕、气短、胸部不适或明显出血时。",
        },
      },
      next_steps: {
        en: ["Bring the result to your clinician.", "Ask whether follow-up blood tests or iron studies are needed.", "Seek prompt care if you feel faint, have chest pain, or shortness of breath."],
        zh: ["将检查结果带给医生查看。", "询问是否需要复查血常规或进一步检查铁代谢。", "如果出现晕厥感、胸痛或气短，请及时就医。"],
      },
      ui_actions: { show_summary: true, show_inline_terms: true, collapse_technical: true, highlight_risk: true },
    },
  },
  {
    id: "medication-antibiotic",
    label: { en: "Medication instruction", zh: "用药说明" },
    session: {
      input_text: {
        en: "Take amoxicillin-clavulanate 875/125 mg by mouth twice daily for 7 days. Complete the full course unless your clinician tells you to stop.",
        zh: "口服阿莫西林克拉维酸 875/125 mg，每日两次，连续 7 天。除非医生要求停止，否则请完成整个疗程。",
      },
      summary: {
        en: "This instruction says to take the antibiotic twice a day for 7 days and not stop early unless a clinician tells you to.",
        zh: "这条说明的意思是：抗生素每天服用两次，连续 7 天，除非医生要求，否则不要提前停药。",
      },
      explanation: {
        en: "Amoxicillin-clavulanate is an antibiotic used for some bacterial infections. The dose listed means each tablet contains amoxicillin plus clavulanate. Completing the full course helps reduce the chance that the infection returns or becomes harder to treat.",
        zh: "阿莫西林克拉维酸是一种用于部分细菌感染的抗生素。这个剂量表示每片药中含有阿莫西林和克拉维酸。完成整个疗程有助于减少感染复发或变得更难治疗的可能。",
      },
      terms: [
        {
          id: "antibiotic",
          term: { en: "antibiotic", zh: "抗生素" },
          definition: { en: "A medicine used to treat bacterial infections.", zh: "用于治疗细菌感染的药物。" },
          why_it_matters: { en: "It does not treat viral infections such as most colds.", zh: "它不能治疗大多数由病毒引起的感冒等疾病。" },
        },
        {
          id: "full-course",
          term: { en: "full course", zh: "完整疗程" },
          definition: { en: "The full number of days your clinician prescribed.", zh: "医生要求服药的完整天数。" },
          why_it_matters: { en: "Stopping early can make an infection return or become harder to treat.", zh: "过早停药可能导致感染复发或更难治疗。" },
        },
      ],
      technical_details: {
        en: "The clavulanate component helps block some bacterial resistance mechanisms. Side effects can include stomach upset, diarrhea, rash, or allergic reaction.",
        zh: "克拉维酸成分可帮助抑制部分细菌耐药机制。常见不适可能包括胃肠不适、腹泻、皮疹或过敏反应。",
      },
      risk: {
        level: "medium",
        reason: {
          en: "Medication instructions should be followed carefully. Seek medical help for signs of allergy such as swelling, trouble breathing, or widespread rash.",
          zh: "用药说明需要谨慎遵循。如出现肿胀、呼吸困难或大面积皮疹等过敏迹象，请及时就医。",
        },
      },
      next_steps: {
        en: ["Take the medicine as prescribed.", "Ask your clinician or pharmacist if you miss a dose.", "Get urgent help for breathing trouble, facial swelling, or severe rash."],
        zh: ["按医嘱服药。", "如果漏服，请咨询医生或药师。", "如果出现呼吸困难、面部肿胀或严重皮疹，请立即就医。"],
      },
      ui_actions: { show_summary: true, show_inline_terms: true, collapse_technical: true, highlight_risk: true },
    },
  },
  {
    id: "imaging-report-lung-nodule",
    label: { en: "Imaging report", zh: "影像检查报告" },
    session: {
      input_text: {
        en: "CT chest shows a 5 mm solitary pulmonary nodule in the right upper lobe. No pleural effusion. Recommend interval follow-up imaging based on risk factors.",
        zh: "胸部 CT 显示右上肺叶有一个 5 mm 孤立性肺结节。未见胸腔积液。建议根据风险因素进行间隔随访影像检查。",
      },
      summary: {
        en: "The scan found a very small lung nodule. Many small nodules are not cancer, but follow-up depends on your risk factors and your clinician's judgment.",
        zh: "检查发现一个很小的肺结节。许多小结节并不是癌症，但是否需要随访取决于你的风险因素和医生判断。",
      },
      explanation: {
        en: "A pulmonary nodule is a small spot in the lung seen on imaging. A 5 mm nodule is small. The report does not describe fluid around the lung. Follow-up imaging may be recommended to check whether the nodule changes over time.",
        zh: "肺结节是在影像检查中看到的肺部小点。5 mm 的结节属于较小的结节。报告没有描述肺周围有积液。医生可能会建议之后复查影像，以观察结节是否变化。",
      },
      terms: [
        {
          id: "pulmonary-nodule",
          term: { en: "pulmonary nodule", zh: "肺结节" },
          definition: { en: "A small spot or rounded area seen in the lung on imaging.", zh: "影像检查中看到的肺部小点或圆形区域。" },
          why_it_matters: { en: "Most small nodules are benign, but some need follow-up to watch for change.", zh: "多数小结节是良性的，但有些需要随访观察变化。" },
        },
        {
          id: "pleural-effusion",
          term: { en: "pleural effusion", zh: "胸腔积液" },
          definition: { en: "Extra fluid around the lungs.", zh: "肺周围出现额外液体。" },
          why_it_matters: { en: "The report says this was not seen, which is generally reassuring.", zh: "报告显示未见胸腔积液，通常是相对放心的表现。" },
        },
      ],
      technical_details: {
        en: "Follow-up timing depends on nodule size, appearance, smoking history, prior cancer history, age, and comparison with previous imaging.",
        zh: "随访时间取决于结节大小、形态、吸烟史、既往肿瘤史、年龄，以及是否能与既往影像对比。",
      },
      risk: {
        level: "medium",
        reason: {
          en: "This is not usually an emergency, but it should be reviewed with a clinician to decide whether follow-up imaging is needed.",
          zh: "这通常不是急症，但需要和医生讨论是否需要后续影像随访。",
        },
      },
      next_steps: {
        en: ["Ask your clinician what follow-up schedule applies to you.", "Bring prior chest imaging if available.", "Seek care sooner if you have coughing blood, unexplained weight loss, or worsening shortness of breath."],
        zh: ["询问医生适合你的随访时间。", "如有既往胸部影像，请一并带给医生。", "如果出现咳血、原因不明的体重下降或气短加重，请尽快就医。"],
      },
      ui_actions: { show_summary: true, show_inline_terms: true, collapse_technical: true, highlight_risk: true },
    },
  },
  {
    id: "child-fever-warning",
    label: { en: "Child fever advice", zh: "儿童发热建议" },
    session: {
      input_text: {
        en: "A 2-year-old child has fever up to 39.5 C, poor oral intake, reduced urine output, and unusual sleepiness.",
        zh: "一名 2 岁儿童发热最高 39.5 摄氏度，进食饮水减少，尿量减少，并出现异常嗜睡。",
      },
      summary: {
        en: "This description includes warning signs in a young child: high fever, reduced drinking, less urine, and unusual sleepiness. This should be assessed promptly by a clinician.",
        zh: "这段描述包含儿童警示信号：高热、饮水减少、尿量减少和异常嗜睡。建议尽快由医生评估。",
      },
      explanation: {
        en: "Fever can be common in children, but reduced urine output and unusual sleepiness can suggest dehydration or a more serious illness. Poor oral intake means the child may not be getting enough fluids. These signs make the situation more urgent than fever alone.",
        zh: "儿童发热很常见，但尿量减少和异常嗜睡可能提示脱水或更严重的问题。进食饮水减少意味着孩子可能没有摄入足够液体。这些信号让情况比单纯发热更需要重视。",
      },
      terms: [
        {
          id: "reduced-urine-output",
          term: { en: "reduced urine output", zh: "尿量减少" },
          definition: { en: "Urinating less often or producing less urine than usual.", zh: "排尿次数或尿量比平时少。" },
          why_it_matters: { en: "It can be a sign of dehydration, especially with fever.", zh: "发热时尿量减少可能提示脱水。" },
        },
        {
          id: "poor-oral-intake",
          term: { en: "poor oral intake", zh: "进食饮水减少" },
          definition: { en: "Not drinking or eating enough by mouth.", zh: "经口摄入的饮水或食物不足。" },
          why_it_matters: { en: "Children can become dehydrated faster than adults.", zh: "儿童比成人更容易较快发生脱水。" },
        },
      ],
      technical_details: {
        en: "Clinicians may assess hydration, breathing, alertness, fever duration, infection source, and whether urgent testing or treatment is needed.",
        zh: "医生可能会评估脱水情况、呼吸、意识状态、发热持续时间、感染来源，以及是否需要紧急检查或治疗。",
      },
      risk: {
        level: "high",
        reason: {
          en: "High fever together with reduced urine output and unusual sleepiness in a young child should be assessed promptly.",
          zh: "幼儿高热伴尿量减少和异常嗜睡，需要尽快评估。",
        },
      },
      next_steps: {
        en: ["Contact a clinician or urgent care service promptly.", "Seek emergency care if the child is hard to wake, breathing abnormally, or cannot keep fluids down.", "Keep track of temperature, fluids, urine, and behavior changes."],
        zh: ["尽快联系医生或急诊/急救服务。", "如果孩子难以唤醒、呼吸异常或无法喝水，请立即就医。", "记录体温、饮水量、尿量和精神状态变化。"],
      },
      ui_actions: { show_summary: true, show_inline_terms: true, collapse_technical: true, highlight_risk: true },
    },
  },
  {
    id: "post-surgery-followup",
    label: { en: "Post-surgery follow-up", zh: "术后复查说明" },
    session: {
      input_text: {
        en: "Follow up in clinic in 2 weeks for wound check. Keep the incision clean and dry. Call if redness, swelling, drainage, fever, or worsening pain develops.",
        zh: "术后 2 周门诊复查伤口。保持切口清洁干燥。如出现发红、肿胀、渗液、发热或疼痛加重，请联系医生。",
      },
      summary: {
        en: "You should have the wound checked in about 2 weeks and watch for signs that could suggest infection.",
        zh: "你需要大约 2 周后复查伤口，并留意可能提示感染的迹象。",
      },
      explanation: {
        en: "The instruction is about routine wound care after surgery. Keeping the incision clean and dry helps healing. Redness, swelling, drainage, fever, or worsening pain can be signs that the wound needs medical attention.",
        zh: "这条说明主要是术后常规伤口护理。保持切口清洁干燥有助于愈合。发红、肿胀、渗液、发热或疼痛加重可能提示伤口需要医生评估。",
      },
      terms: [
        {
          id: "incision",
          term: { en: "incision", zh: "切口" },
          definition: { en: "The surgical cut made in the skin.", zh: "手术时在皮肤上形成的切开部位。" },
          why_it_matters: { en: "The incision needs care while it heals.", zh: "切口在愈合期间需要护理。" },
        },
        {
          id: "drainage",
          term: { en: "drainage", zh: "渗液" },
          definition: { en: "Fluid coming out from the wound.", zh: "从伤口流出的液体。" },
          why_it_matters: { en: "New or worsening drainage can be a sign of infection or delayed healing.", zh: "新出现或加重的渗液可能提示感染或愈合延迟。" },
        },
      ],
      technical_details: {
        en: "Clinicians check wound edges, redness, warmth, swelling, drainage, pain pattern, and systemic symptoms such as fever.",
        zh: "医生会检查伤口边缘、发红、发热、肿胀、渗液、疼痛变化，以及发热等全身症状。",
      },
      risk: {
        level: "low",
        reason: {
          en: "This sounds like routine follow-up advice, but the listed symptoms should prompt contact with a clinician.",
          zh: "这看起来是常规复查建议，但如果出现列出的症状，应联系医生。",
        },
      },
      next_steps: {
        en: ["Schedule or attend the 2-week wound check.", "Keep the incision clean and dry as instructed.", "Call the clinic if redness, swelling, drainage, fever, or worsening pain appears."],
        zh: ["安排或按时参加 2 周后的伤口复查。", "按说明保持切口清洁干燥。", "如出现发红、肿胀、渗液、发热或疼痛加重，请联系门诊。"],
      },
      ui_actions: { show_summary: true, show_inline_terms: true, collapse_technical: false, highlight_risk: false },
    },
  },
];

const safetyNotice = {
  en: "This tool helps explain medical information. It does not replace professional medical advice.",
  zh: "本工具仅帮助理解医学信息，不能替代专业医疗建议。",
};

let state = {
  language: localStorage.getItem(LANGUAGE_KEY) || "en",
  input: "",
  currentSession: null,
  loading: false,
  fallback: null,
  filter: "all",
};

function t(key) {
  return text[state.language][key] || text.en[key] || key;
}

function local(value) {
  if (!value) return "";
  if (typeof value === "string") return value;
  return value[state.language] || value.en || value.zh || "";
}

function icon(symbol) {
  return `<span aria-hidden="true">${symbol}</span>`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function sessions() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
}

function saveSessions(items) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

function saveSession(session) {
  const list = sessions().filter((item) => item.session_id !== session.session_id);
  list.unshift(session);
  saveSessions(list.slice(0, 50));
}

function normalizeSession(base) {
  return {
    session_id: base.session_id || `sess_${Date.now()}_${Math.random().toString(16).slice(2, 8)}`,
    created_at: base.created_at || new Date().toISOString(),
    input_text: base.input_text,
    summary: base.summary,
    explanation: base.explanation,
    terms: base.terms || [],
    technical_details: base.technical_details || { en: "", zh: "" },
    risk: base.risk || { level: "low", reason: { en: "", zh: "" } },
    next_steps: base.next_steps || { en: [], zh: [] },
    safety_notice: base.safety_notice || safetyNotice,
    trust_note: base.trust_note || { en: t("trust"), zh: text.zh.trust },
    cognitive_load_label: base.cognitive_load_label || "medium",
    cognitive_load_score: typeof base.cognitive_load_score === "number" ? base.cognitive_load_score : 0.5,
    semantic_complexity_features: base.semantic_complexity_features || null,
    ui_actions: base.ui_actions || { show_summary: true, show_inline_terms: true, collapse_technical: true, highlight_risk: false },
    annotations: base.annotations || { en: [], zh: [] },
    feedback: base.feedback || {},
    fallback_type: base.fallback_type || "none",
    fallback_message: base.fallback_message,
  };
}

function getExample(id) {
  const found = examples.find((item) => item.id === id) || examples[0];
  return normalizeSession(JSON.parse(JSON.stringify(found.session)));
}

function isMedicalLike(input) {
  const words = [
    "blood", "test", "doctor", "note", "pain", "fever", "dose", "tablet", "mg", "g/dl", "ct", "mri", "scan", "report",
    "symptom", "hemoglobin", "anemia", "infection", "surgery", "wound", "urine", "nodule", "diagnosis", "treatment",
    "patient", "clinic", "clinician", "medication", "antibiotic", "follow-up", "follow up",
  ];
  const wordsZh = [
    "心功能", "心律", "冠心病", "肺部", "甲状腺", "气短", "下肢水肿", "水肿", "心脏", "泵血",
    "血压", "血糖", "血红蛋白", "贫血", "红细胞", "白细胞", "报告", "检查", "影像", "用药",
    "药物", "剂量", "发热", "发烧", "胸痛", "呼吸困难", "医生", "术后", "切口", "渗液",
  ];
  const lower = input.toLowerCase();
  return words.some((word) => lower.includes(word)) || wordsZh.some((word) => input.includes(word));
}

function chooseMock(input) {
  const lower = input.toLowerCase();
  if (lower.includes("hemoglobin") || lower.includes("anemia") || lower.includes("blood")) return getExample("blood-test-anemia");
  if (lower.includes("amoxicillin") || lower.includes("antibiotic") || lower.includes("tablet") || lower.includes("dose")) return getExample("medication-antibiotic");
  if (lower.includes("nodule") || lower.includes("ct") || lower.includes("mri") || lower.includes("scan")) return getExample("imaging-report-lung-nodule");
  if (lower.includes("child") || lower.includes("fever") || lower.includes("urine") || lower.includes("sleepy")) return getExample("child-fever-warning");
  if (lower.includes("surgery") || lower.includes("wound") || lower.includes("incision")) return getExample("post-surgery-followup");
  const generic = getExample("blood-test-anemia");
  generic.input_text = { en: input, zh: input };
  generic.summary = {
    en: "Here is a plain-language explanation based on the medical wording you provided. For personal health decisions, review it with a qualified clinician.",
    zh: "以下是基于你提供的医学表述生成的通俗解释。涉及个人健康决策时，请与专业医生确认。",
  };
  generic.explanation = {
    en: "The text appears to describe a medical finding or instruction. The key idea is to identify what the result says, why it may matter, and what follow-up may be needed. Because the information is incomplete, this explanation should be treated as a general reading aid rather than a diagnosis.",
    zh: "这段文字看起来是在描述医学结果或医嘱。理解重点是：它说了什么、为什么可能重要，以及是否需要后续处理。由于信息不完整，本解释只能作为阅读辅助，不能作为诊断。",
  };
  generic.terms = [];
  generic.risk = {
    level: "medium",
    reason: {
      en: "The text may relate to health decisions, so it is worth discussing with a clinician if it concerns your own care.",
      zh: "这段内容可能与健康决策有关，如果与你自己的情况相关，建议咨询医生。",
    },
  };
  return generic;
}

function fallback(type) {
  const messages = {
    empty: { en: text.en.emptyInput, zh: text.zh.emptyInput },
    short: { en: text.en.tooShort, zh: text.zh.tooShort },
    nonMedical: { en: text.en.nonMedical, zh: text.zh.nonMedical },
    api: { en: text.en.apiError, zh: text.zh.apiError },
  };
  return {
    type,
    message: messages[type] || messages.api,
  };
}

async function explainMedicalText(input) {
  const trimmed = input.trim();
  if (!trimmed) throw fallback("empty");
  if (trimmed.length < 24) throw fallback("short");
  if (!looksMedical(trimmed)) throw fallback("nonMedical");

  const requestLanguage = detectInputLanguage(trimmed);

  if (APP_MODE === "api") {
    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input_text: trimmed, language: requestLanguage, translate_to_zh: true, save_session: true }),
    });
    if (!response.ok) throw fallback("api");
    const data = await response.json();
    return normalizeSession(data);
  }

  await new Promise((resolve) => setTimeout(resolve, 520));
  const session = chooseMock(trimmed);
  session.input_text = session.input_text.en === trimmed || session.input_text.zh === trimmed ? session.input_text : { en: trimmed, zh: trimmed };
  return session;
}

function detectInputLanguage(value) {
  return /[\u4e00-\u9fff]/.test(value) ? "zh" : "en";
}

function looksMedical(input) {
  const wordsEn = [
    "blood", "test", "doctor", "note", "pain", "fever", "dose", "tablet", "mg", "g/dl", "ct", "mri", "scan", "report",
    "symptom", "hemoglobin", "anemia", "infection", "surgery", "wound", "urine", "nodule", "diagnosis", "treatment",
    "patient", "clinic", "clinician", "medication", "antibiotic", "follow-up", "follow up",
  ];
  const wordsZh = [
    "\u5fc3\u529f\u80fd", "\u5fc3\u5f8b", "\u51a0\u5fc3\u75c5", "\u80ba\u90e8", "\u7532\u72b6\u817a", "\u6c14\u77ed",
    "\u4e0b\u80a2\u6c34\u80bf", "\u6c34\u80bf", "\u5fc3\u810f", "\u6cf5\u8840", "\u8840\u538b", "\u8840\u7cd6",
    "\u8840\u7ea2\u86cb\u767d", "\u8d2b\u8840", "\u7ea2\u7ec6\u80de", "\u767d\u7ec6\u80de", "\u62a5\u544a", "\u68c0\u67e5",
    "\u5f71\u50cf", "\u7528\u836f", "\u836f\u7269", "\u5242\u91cf", "\u53d1\u70ed", "\u53d1\u70e7",
    "\u80f8\u75db", "\u547c\u5438\u56f0\u96be", "\u533b\u751f", "\u672f\u540e", "\u5207\u53e3", "\u6e17\u6db2",
  ];
  const lower = input.toLowerCase();
  return wordsEn.some((word) => lower.includes(word)) || wordsZh.some((word) => input.includes(word));
}

function renderShell(content) {
  return `
    <div class="app-shell">
      <header class="topbar">
        <a class="brand" href="#/">
          <span class="brand-mark">+</span>
          <span>${t("appTitle")}</span>
        </a>
        <div class="top-actions">
          <button class="ghost-button" data-action="go-history">${t("history")}</button>
          <button class="icon-button" data-action="toggle-language" aria-label="Toggle language">${state.language === "en" ? "中文" : "English"}</button>
        </div>
      </header>
      ${content}
      <footer class="footer">
        <div class="footer-inner">
          <strong>MedEase</strong>
          <span>${state.language === "en" ? "For understanding only. Always consult a professional." : "仅用于帮助理解。请始终咨询专业人士。"}</span>
        </div>
      </footer>
    </div>
  `;
}

function renderWorkspace() {
  const result = state.loading
    ? renderLoading()
    : state.fallback
      ? renderFallback(state.fallback)
      : state.currentSession
        ? renderExplanation(state.currentSession, false)
        : renderEmpty();

  return renderShell(`
    <main class="workspace">
      <section class="side-column">
        <div class="panel input-panel">
          <h1 class="section-title">${t("inputTitle")}</h1>
          <p class="section-subtitle">${t("inputHelp")}</p>
          <div class="textarea-wrap">
            <textarea id="medical-input" placeholder="${t("inputPlaceholder")}">${escapeHtml(state.input)}</textarea>
          </div>
          <div class="input-actions">
            <span class="char-count"><span id="char-count">${state.input.length}</span> ${t("charCount")}</span>
            <div class="button-row">
              <button class="ghost-button" data-action="clear">${t("clear")}</button>
              <button class="primary-button" data-action="submit" ${state.loading || !state.input.trim() ? "disabled" : ""}>${t("explain")}</button>
            </div>
          </div>
          <div class="privacy-note">${icon("lock")}<span>${t("privacy")}</span></div>
        </div>
        <div class="examples">
          <p class="eyebrow">${t("examples")}</p>
          <div class="chip-row">
            ${examples.map((item) => `<button class="chip" data-action="example" data-id="${item.id}">${local(item.label)}</button>`).join("")}
          </div>
        </div>
      </section>
      <section class="result-column">${result}</section>
    </main>
  `);
}

function renderEmpty() {
  return `
    <div class="panel state-panel">
      <div class="state-inner">
        <div class="state-icon">${icon("text")}</div>
        <h2 class="state-title">${t("emptyTitle")}</h2>
        <p class="state-text">${t("emptyText")}</p>
      </div>
    </div>
  `;
}

function renderLoading() {
  return `
    <div class="panel state-panel">
      <div class="state-inner">
        <div class="state-icon">${icon("...")}</div>
        <h2 class="state-title">${t("loadingTitle")}</h2>
        <p class="state-text">${t("loadingText")}</p>
        <div class="loading-bar"></div>
      </div>
    </div>
  `;
}

function renderFallback(item) {
  return `
    <div class="panel state-panel">
      <div class="state-inner">
        <div class="state-icon">${icon("!")}</div>
        <h2 class="state-title">${item.type === "api" ? t("serviceUnavailable") : t("contextRequired")}</h2>
        <p class="state-text">${escapeHtml(local(item.message))}</p>
        <div class="button-row" style="justify-content:center;margin-top:22px">
          <button class="primary-button" data-action="submit">${t("tryAgain")}</button>
          <button class="ghost-button" data-action="example" data-id="blood-test-anemia">${t("useExample")}</button>
        </div>
      </div>
    </div>
  `;
}

function renderExplanation(session, detailPage) {
  const showSummary = session.ui_actions.show_summary && local(session.summary);
  const showInlineTerms = session.ui_actions.show_inline_terms && session.terms.length > 0;
  const collapse = session.ui_actions.collapse_technical && !detailPage;
  return `
    <div class="result-stack">
      <div class="notice">
        ${icon("i")}
        <div>
          <strong>${t("safetyTitle")}</strong>
          <p>${escapeHtml(local(session.safety_notice))}</p>
        </div>
      </div>
      <article class="panel result-card">
        <div class="result-stack">
          ${showSummary ? `
            <section class="content-section summary-section">
              <h2>${t("plain")}</h2>
              <p>${escapeHtml(local(session.summary))}</p>
            </section>
          ` : ""}
          <section class="content-section">
            <h2>${t("explanation")}</h2>
            <div class="annotated-box">
              <p class="annotated-text">${showInlineTerms ? renderAnnotatedText(local(session.explanation), session.terms, session.annotations) : escapeHtml(local(session.explanation))}</p>
              ${!showInlineTerms ? `<p class="small-note" style="margin-top:12px">${t("noTerms")}</p>` : ""}
            </div>
          </section>
          ${showInlineTerms ? `
            <section class="content-section">
              <h3>${t("terms")}</h3>
              <div class="terms-list">
                ${session.terms.map((term) => `
                  <div class="term-item">
                    <strong>${escapeHtml(local(term.term))}</strong>
                    <p>${escapeHtml(local(term.definition))}</p>
                  </div>
                `).join("")}
              </div>
            </section>
          ` : ""}
          <div class="risk-next-grid">
            <section class="risk-panel ${session.risk.level}">
              <h3>${t("watch")}</h3>
              <p><strong>${riskLabel(session.risk.level)}.</strong> ${escapeHtml(local(session.risk.reason))}</p>
            </section>
            <section class="next-panel">
              <h3>${t("next")}</h3>
              <ol>${(session.next_steps[state.language] || session.next_steps.en || []).map((step) => `<li>${escapeHtml(step)}</li>`).join("")}</ol>
            </section>
          </div>
          ${local(session.technical_details) ? `
            <section class="content-section">
              <button class="details-toggle" data-action="toggle-details" aria-expanded="${collapse ? "false" : "true"}">
                <span>${t("detail")}</span>
                <span>${collapse ? t("showMore") : t("showLess")}</span>
              </button>
              <div class="details-content ${collapse ? "hidden" : ""}">
                ${escapeHtml(local(session.technical_details))}
              </div>
            </section>
          ` : ""}
          <div class="trust-note">${icon("shield")}<span>${escapeHtml(local(session.trust_note))}</span></div>
          ${renderFeedback(session)}
        </div>
      </article>
    </div>
  `;
}

function annotate(content, terms) {
  if (!terms.length) return escapeHtml(content);

  const matches = [];
  const occupied = [];

  const isFree = (start, end) => occupied.every((range) => end <= range.start || start >= range.end);
  const addMatch = (start, end, index) => {
    occupied.push({ start, end });
    matches.push({ start, end, index });
  };

  const variants = [];
  terms.forEach((term, index) => {
    const localizedSurfaceForms = term.surface_forms?.[state.language] || [];
    const localizedAliases = term.aliases?.[state.language] || [];
    const canonical = local(term.term);
    const values = [...localizedSurfaceForms, ...localizedAliases, canonical]
      .map((value) => (value || "").trim())
      .filter(Boolean);
    values.forEach((value) => variants.push({ index, value }));
  });

  variants.sort((a, b) => b.value.length - a.value.length);

  variants.forEach(({ index, value }) => {
    const lowerContent = content.toLowerCase();
    const lowerValue = value.toLowerCase();
    let searchFrom = 0;
    while (searchFrom < content.length) {
      const start = lowerContent.indexOf(lowerValue, searchFrom);
      if (start === -1) break;
      const end = start + value.length;
      if (isFree(start, end)) addMatch(start, end, index);
      searchFrom = end;
    }
  });

  matches.sort((a, b) => a.start - b.start);
  let cursor = 0;
  let html = "";
  for (const match of matches) {
    if (cursor < match.start) html += escapeHtml(content.slice(cursor, match.start));
    const raw = content.slice(match.start, match.end);
    html += `<button class="inline-term" data-action="term" data-term="${match.index}">${escapeHtml(raw)}</button>`;
    cursor = match.end;
  }
  if (cursor < content.length) html += escapeHtml(content.slice(cursor));
  return html;
}

function renderAnnotatedText(content, terms, annotations) {
  const localizedAnnotations = annotations?.[state.language] || [];
  if (localizedAnnotations.length) {
    return annotateWithPositions(content, terms, localizedAnnotations);
  }
  return annotate(content, terms);
}

function annotateWithPositions(content, terms, localizedAnnotations) {
  const termIndexById = new Map(terms.map((term, index) => [term.id, index]));
  let html = "";
  let cursor = 0;

  [...localizedAnnotations]
    .sort((a, b) => a.start - b.start)
    .forEach((annotation) => {
      const termIndex = termIndexById.get(annotation.term_id);
      if (termIndex === undefined) return;
      if (annotation.start < cursor || annotation.end > content.length) return;
      if (cursor < annotation.start) html += escapeHtml(content.slice(cursor, annotation.start));
      html += `<button class="inline-term" data-action="term" data-term="${termIndex}">${escapeHtml(content.slice(annotation.start, annotation.end))}</button>`;
      cursor = annotation.end;
    });

  if (cursor < content.length) html += escapeHtml(content.slice(cursor));
  return html;
}

function riskLabel(level) {
  if (level === "high") return t("riskHigh");
  if (level === "medium") return t("riskMedium");
  return t("riskLow");
}

function renderFeedback(session) {
  const feedback = session.feedback || {};
  const active = (key) => feedback[key] ? " active" : "";
  return `
    <section class="feedback">
      <span class="feedback-title">${t("feedbackTitle")}</span>
      <div class="button-row">
        <button class="feedback-button${active("understood")}" data-action="feedback" data-feedback="understood">${t("understand")}</button>
        <button class="feedback-button${active("helpful")}" data-action="feedback" data-feedback="helpful">${t("helpful")}</button>
        <button class="feedback-button${active("still_confused")}" data-action="feedback" data-feedback="still_confused">${t("confused")}</button>
      </div>
    </section>
  `;
}

function renderHistory() {
  const list = filteredSessions();
  return renderShell(`
    <main class="page">
      <header class="page-header">
        <div>
          <h1 class="page-title">${t("previous")}</h1>
          <p class="page-copy">${t("previousCopy")}</p>
        </div>
        <div class="button-row">
          <button class="primary-button" data-action="go-home">${t("newExplanation")}</button>
          <button class="danger-button" data-action="clear-history">${t("clearHistory")}</button>
        </div>
      </header>
      <div class="filter-row">
        ${["all", "attention", "confusing"].map((key) => `<button class="${state.filter === key ? "primary-button" : "soft-button"}" data-action="filter" data-filter="${key}">${filterLabel(key)}</button>`).join("")}
      </div>
      ${list.length ? `<div class="history-list">${list.map(renderHistoryCard).join("")}</div>` : `
        <div class="panel state-panel" style="margin-top:20px">
          <div class="state-inner">
            <div class="state-icon">${icon("0")}</div>
            <h2 class="state-title">${t("noHistory")}</h2>
            <div class="button-row" style="justify-content:center;margin-top:20px">
              <button class="primary-button" data-action="go-home">${t("newExplanation")}</button>
            </div>
          </div>
        </div>
      `}
    </main>
  `);
}

function filterLabel(key) {
  if (key === "attention") return t("needsAttention");
  if (key === "confusing") return t("stillConfusing");
  return t("all");
}

function filteredSessions() {
  const list = sessions();
  if (state.filter === "attention") return list.filter((item) => ["medium", "high"].includes(item.risk.level));
  if (state.filter === "confusing") return list.filter((item) => item.feedback && item.feedback.still_confused);
  return list;
}

function feedbackLabel(feedback = {}) {
  if (feedback.still_confused) return t("confusedStatus");
  if (feedback.understood) return t("understood");
  if (feedback.helpful) return t("helpfulStatus");
  return t("pending");
}

function renderHistoryCard(session) {
  return `
    <article class="panel history-card">
      <div>
        <div class="history-meta">${t("created")}: ${formatDate(session.created_at)}</div>
        <p class="preview-label">${t("inputPreview")}</p>
        <p class="preview-text">${truncate(local(session.input_text), 190)}</p>
        <p class="history-feedback" style="margin-top:18px">${t("feedback")}: ${feedbackLabel(session.feedback)}</p>
      </div>
      <div>
        <span class="risk-pill ${session.risk.level}">${riskLabel(session.risk.level)}</span>
        <div class="summary-preview" style="margin-top:14px">
          <p class="preview-label" style="margin-top:0">${t("summaryPreview")}</p>
          <p class="preview-text">${truncate(local(session.summary), 180)}</p>
        </div>
        <div class="history-card-actions">
          <button class="danger-button" data-action="delete-session" data-id="${session.session_id}">${t("delete")}</button>
          <button class="primary-button" data-action="open-session" data-id="${session.session_id}">${t("open")}</button>
        </div>
      </div>
    </article>
  `;
}

function renderSessionDetail(id) {
  const session = sessions().find((item) => item.session_id === id);
  if (!session) {
    return renderShell(`
      <main class="page">
        <div class="panel state-panel">
          <div class="state-inner">
            <div class="state-icon">${icon("?")}</div>
            <h1 class="state-title">${t("notFound")}</h1>
            <div class="button-row" style="justify-content:center;margin-top:20px">
              <button class="ghost-button" data-action="go-history">${t("backHistory")}</button>
              <button class="primary-button" data-action="go-home">${t("newExplanation")}</button>
            </div>
          </div>
        </div>
      </main>
    `);
  }

  state.currentSession = session;
  return renderShell(`
    <main class="page">
      <header class="page-header">
        <div>
          <h1 class="page-title">${t("details")}</h1>
          <p class="page-copy">${formatDate(session.created_at)}</p>
        </div>
        <div class="button-row">
          <button class="ghost-button" data-action="go-history">${t("backHistory")}</button>
          <button class="primary-button" data-action="go-home">${t("newExplanation")}</button>
          <button class="soft-button" data-action="export-json" data-id="${session.session_id}">${t("exportJson")}</button>
          <button class="danger-button" data-action="delete-session" data-id="${session.session_id}">${t("delete")}</button>
        </div>
      </header>
      <div class="session-layout">
        <section class="panel result-card">
          <h2>${t("original")}</h2>
          <div class="original-text">${escapeHtml(local(session.input_text))}</div>
        </section>
        ${renderExplanation(session, true)}
      </div>
    </main>
  `);
}

function truncate(value, max) {
  const str = String(value || "");
  return str.length > max ? `${str.slice(0, max - 1)}...` : str;
}

function formatDate(value) {
  try {
    return new Intl.DateTimeFormat(state.language === "zh" ? "zh-CN" : "en-US", {
      year: "numeric",
      month: "short",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(value));
  } catch {
    return value;
  }
}

function route() {
  const hash = window.location.hash || "#/";
  if (hash.startsWith("#/history")) return { page: "history" };
  if (hash.startsWith("#/session/")) return { page: "session", id: decodeURIComponent(hash.replace("#/session/", "")) };
  return { page: "workspace" };
}

function render() {
  const current = route();
  const html = current.page === "history" ? renderHistory() : current.page === "session" ? renderSessionDetail(current.id) : renderWorkspace();
  document.getElementById("app").innerHTML = html;
  bindInputs();
}

function bindInputs() {
  const input = document.getElementById("medical-input");
  if (!input) return;
  input.addEventListener("input", (event) => {
    state.input = event.target.value;
    const count = document.getElementById("char-count");
    if (count) count.textContent = state.input.length;
    const submit = document.querySelector('[data-action="submit"]');
    if (submit) submit.disabled = state.loading || !state.input.trim();
  });
  input.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      event.preventDefault();
      submitInput();
    }
  });
}

async function submitInput() {
  state.loading = true;
  state.fallback = null;
  state.currentSession = null;
  render();
  try {
    const session = await explainMedicalText(state.input);
    state.currentSession = session;
    saveSession(session);
  } catch (error) {
    state.fallback = error && error.type && error.message ? error : fallback("api");
  } finally {
    state.loading = false;
    render();
  }
}

function showTerm(index, target) {
  const session = state.currentSession;
  if (!session || !session.terms[index]) return;
  const term = session.terms[index];
  const layer = document.getElementById("term-layer");
  const rect = target.getBoundingClientRect();
  const top = Math.min(window.innerHeight - 220, rect.bottom + 10);
  const left = Math.min(window.innerWidth - 340, Math.max(14, rect.left));
  layer.innerHTML = `
    <div class="term-popover" style="left:${left}px;top:${top}px">
      <h4>${escapeHtml(local(term.term))}</h4>
      <p>${escapeHtml(local(term.definition))}</p>
      <p><strong>${t("whyMatters")}:</strong> ${escapeHtml(local(term.why_it_matters))}</p>
      <button class="ghost-button close-popover" data-action="close-term">${t("close")}</button>
    </div>
  `;
}

function hideTerm() {
  document.getElementById("term-layer").innerHTML = "";
}

function updateSession(session) {
  state.currentSession = session;
  saveSession(session);
}

function handleFeedback(kind) {
  const session = state.currentSession;
  if (!session) return;
  session.feedback = {
    ...session.feedback,
    [kind]: true,
  };
  updateSession(session);
  toast(kind === "still_confused" ? t("confusedToast") : t("thanks"));
  render();
}

function toast(message) {
  const el = document.getElementById("toast");
  el.textContent = message;
  el.classList.add("show");
  window.clearTimeout(toast.timer);
  toast.timer = window.setTimeout(() => el.classList.remove("show"), 3800);
}

function exportJson(id) {
  const session = sessions().find((item) => item.session_id === id);
  if (!session) return;
  const blob = new Blob([JSON.stringify(session, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${session.session_id}.json`;
  link.click();
  URL.revokeObjectURL(url);
}

document.addEventListener("click", (event) => {
  const actionEl = event.target.closest("[data-action]");
  if (!actionEl) {
    hideTerm();
    return;
  }

  const action = actionEl.dataset.action;
  if (action === "toggle-language") {
    state.language = state.language === "en" ? "zh" : "en";
    localStorage.setItem(LANGUAGE_KEY, state.language);
    render();
  }
  if (action === "go-history") window.location.hash = "#/history";
  if (action === "go-home") {
    state.currentSession = null;
    state.fallback = null;
    window.location.hash = "#/";
  }
  if (action === "submit") submitInput();
  if (action === "clear") {
    state.input = "";
    state.currentSession = null;
    state.fallback = null;
    render();
  }
  if (action === "example") {
    const session = getExample(actionEl.dataset.id);
    state.input = session.input_text.en;
    state.currentSession = session;
    state.fallback = null;
    saveSession(session);
    window.location.hash = "#/";
    render();
  }
  if (action === "toggle-details") {
    const content = actionEl.nextElementSibling;
    const expanded = actionEl.getAttribute("aria-expanded") === "true";
    actionEl.setAttribute("aria-expanded", String(!expanded));
    actionEl.querySelector("span:last-child").textContent = expanded ? t("showMore") : t("showLess");
    content.classList.toggle("hidden", expanded);
  }
  if (action === "term") {
    event.stopPropagation();
    showTerm(Number(actionEl.dataset.term), actionEl);
  }
  if (action === "close-term") hideTerm();
  if (action === "feedback") handleFeedback(actionEl.dataset.feedback);
  if (action === "filter") {
    state.filter = actionEl.dataset.filter;
    render();
  }
  if (action === "open-session") window.location.hash = `#/session/${encodeURIComponent(actionEl.dataset.id)}`;
  if (action === "delete-session") {
    if (confirm(state.language === "en" ? "Delete this explanation?" : "删除这条解释？")) {
      saveSessions(sessions().filter((item) => item.session_id !== actionEl.dataset.id));
      if (route().page === "session") window.location.hash = "#/history";
      render();
    }
  }
  if (action === "clear-history") {
    if (confirm(state.language === "en" ? "Clear all history?" : "清空全部历史？")) {
      saveSessions([]);
      render();
    }
  }
  if (action === "export-json") exportJson(actionEl.dataset.id);
});

document.addEventListener("mouseover", (event) => {
  const term = event.target.closest('[data-action="term"]');
  if (term) showTerm(Number(term.dataset.term), term);
});

document.addEventListener("focusin", (event) => {
  const term = event.target.closest('[data-action="term"]');
  if (term) showTerm(Number(term.dataset.term), term);
});

document.addEventListener("mouseout", (event) => {
  if (event.target.closest('[data-action="term"]')) {
    window.clearTimeout(hideTerm.timer);
    hideTerm.timer = window.setTimeout(hideTerm, 260);
  }
});

window.addEventListener("hashchange", render);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") hideTerm();
});

render();
