"""
Generates data/safe_examples_seed.csv with 109 entries using the new SafeExample schema.
Run once: python scripts/_generate_dataset.py
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = ROOT / "data" / "safe_examples_seed.csv"

FIELDS = [
    "example_id", "title", "content_text", "domain", "topic",
    "safety_band", "framing", "safe_summary", "why_interesting",
    "allowed_for_demo", "notes",
]

ROWS = [
    # -------------------------------------------------------------------------
    # BIOLOGY (BL001-BL014) - 14 entries
    # -------------------------------------------------------------------------
    ("BL001", "How CRISPR-Cas9 gene editing works",
     "CRISPR-Cas9 is a molecular tool adapted from bacterial immune systems that allows scientists to edit DNA sequences in living organisms. A guide RNA directs the Cas9 protein to a specific location in the genome, where it creates a double-strand break. The cell then repairs the break through natural mechanisms, which scientists can exploit to insert, delete, or modify genetic sequences. Applications include treating genetic diseases, improving crops, and basic research into gene function.",
     "biology", "CRISPR gene editing", "benign", "educational",
     "Explanation of CRISPR-Cas9 mechanism and applications in medicine and research.",
     "Core biology education that shares vocabulary with biosecurity concerns without approaching operational risk.",
     "True", ""),

    ("BL002", "The central dogma of molecular biology",
     "The central dogma of molecular biology describes the flow of genetic information within a biological system. DNA is transcribed into messenger RNA, which is then translated into proteins by ribosomes. This one-way flow of information is foundational to understanding how organisms develop, reproduce, and respond to their environment. Exceptions to the central dogma include reverse transcription, as seen in retroviruses, and RNA replication in RNA viruses.",
     "biology", "Central dogma", "benign", "educational",
     "Overview of the central dogma: DNA to RNA to protein.",
     "Foundational biology that is prerequisite knowledge for virtually all life sciences.",
     "True", ""),

    ("BL003", "Viral replication cycles in RNA viruses",
     "RNA viruses replicate by injecting their genetic material into a host cell, hijacking the cell's machinery to produce new viral proteins and copies of the viral genome. The life cycle typically involves attachment to host cell receptors, fusion with the cell membrane, release of the viral genome, replication of the genome by viral RNA-dependent RNA polymerase, assembly of new virions, and budding or lysis to release them. Understanding replication cycles is essential for designing antiviral drugs and vaccines.",
     "biology", "Viral replication", "capability_building", "technical",
     "Technical description of RNA virus replication cycles and their relevance to antiviral development.",
     "Shares technical vocabulary with dual-use virology; essential for vaccine and antiviral research.",
     "True", ""),

    ("BL004", "How vaccines train the immune system",
     "Vaccines introduce antigens or antigen-encoding instructions into the body to stimulate an immune response without causing disease. The immune system produces antibodies and memory cells that recognize the target pathogen. Modern vaccine platforms include live-attenuated, inactivated, subunit, mRNA, and viral vector vaccines. Each platform presents different trade-offs in efficacy, stability, manufacturing complexity, and safety profile.",
     "biology", "Vaccine mechanisms", "benign", "educational",
     "How vaccines work and overview of modern vaccine platforms.",
     "Public health education with no dual-use concern; models good biosafety framing.",
     "True", ""),

    ("BL005", "Gain-of-function research: scientific rationale and governance debate",
     "Gain-of-function (GOF) research involves modifying organisms to study whether specific genetic changes would confer new or enhanced traits, including increased transmissibility or virulence. Proponents argue GOF work enables pandemic preparedness by identifying future threats before they emerge. Critics argue the risks of lab accident or misuse outweigh the benefits. The debate has led to moratoriums, policy review, and ongoing international governance discussions, particularly in the United States and among biosafety bodies.",
     "biology", "Gain-of-function research", "ambiguous", "policy",
     "Policy and scientific debate around gain-of-function research in virology.",
     "Central biosecurity governance case study; sits at the boundary between legitimate science policy and dual-use concern.",
     "True", ""),

    ("BL006", "Antibiotic resistance mechanisms in bacteria",
     "Bacteria develop resistance to antibiotics through several mechanisms: enzymatic inactivation of the drug, modification of the drug target site, efflux pumps that expel the antibiotic from the cell, and reduced membrane permeability. Resistance genes can spread between bacteria through horizontal gene transfer via plasmids, transposons, and bacteriophages. Understanding these mechanisms is essential for designing new antibiotics and for clinical stewardship practices.",
     "biology", "Antibiotic resistance", "capability_building", "technical",
     "Mechanisms of antibiotic resistance and relevance to drug design and stewardship.",
     "Biomedical education with mild dual-use relevance; understanding resistance is prerequisite to fighting it.",
     "True", ""),

    ("BL007", "The role of the microbiome in human health",
     "The human gut microbiome consists of trillions of microorganisms, primarily bacteria, that play essential roles in digestion, immune regulation, and neurological signaling. Disruptions to the microbiome have been associated with conditions including inflammatory bowel disease, obesity, depression, and autoimmune disorders. Research into microbiome modulation through diet, probiotics, and fecal microbiota transplantation is an active area of clinical investigation.",
     "biology", "Human microbiome", "benign", "educational",
     "Overview of the gut microbiome and its role in health and disease.",
     "Standard health science education; useful contrast to biosecurity-adjacent entries.",
     "True", ""),

    ("BL008", "How pathogens evade host immune responses",
     "Pathogens have evolved multiple strategies to evade host immune defenses. These include downregulating host MHC expression to avoid T cell recognition, secreting proteases that cleave antibodies, hiding within host cells to avoid extracellular immune surveillance, and undergoing antigenic variation to stay ahead of adaptive immunity. Understanding these mechanisms informs vaccine design and the development of immunomodulatory therapies.",
     "biology", "Immune evasion mechanisms", "capability_building", "technical",
     "How pathogens evade immune responses, relevant to vaccine and therapeutic design.",
     "Technical virology/immunology with dual-use proximity; framed toward defensive understanding.",
     "True", ""),

    ("BL009", "Dual-use research of concern: what makes biology dual-use",
     "Dual-use research of concern (DURC) refers to life sciences research that could be misused to threaten public health, agriculture, or national security. The category includes research that enhances pathogen transmissibility, virulence, or drug resistance, or that demonstrates how to disrupt immune responses or food supplies. Governance frameworks identify DURC categories and require institutional and government oversight, including the US federal DURC policy and international biosafety guidelines.",
     "biology", "Dual-use research governance", "policy_relevant_sanitized", "policy",
     "Overview of dual-use research of concern categories and governance frameworks.",
     "Policy analysis of the governance problem without operational detail; essential for biosecurity education.",
     "True", ""),

    ("BL010", "mRNA technology and its applications beyond vaccines",
     "mRNA technology, accelerated by COVID-19 vaccine development, has applications beyond infectious disease. Researchers are exploring mRNA-based cancer immunotherapies, treatments for rare genetic disorders, and regenerative medicine applications. The platform allows rapid design and manufacturing compared to traditional biologics, and can be adapted to target almost any protein the body produces or should produce.",
     "biology", "mRNA therapeutics", "benign", "educational",
     "Overview of mRNA technology and its expanding therapeutic applications.",
     "Biomedical optimism framing; useful contrast to biosecurity-adjacent entries.",
     "True", ""),

    ("BL011", "How biosurveillance systems detect emerging outbreaks",
     "Biosurveillance integrates data from clinical reports, laboratory testing, syndromic monitoring, genomic sequencing, and environmental sampling to detect potential disease outbreaks early. Systems like the Global Health Security Agenda, ProMED, and national sentinel surveillance networks aggregate signals from multiple sources. Early detection is critical because delays in outbreak identification allow exponential spread before containment measures can be implemented.",
     "biology", "Biosurveillance", "benign", "policy",
     "How biosurveillance systems work and their role in pandemic preparedness.",
     "Public health infrastructure education that shares proximity to biodefense-adjacent content.",
     "True", ""),

    ("BL012", "Gene drive technology and ecological risk",
     "Gene drives are genetic systems designed to spread a particular allele through a wild population at rates exceeding normal inheritance. They have been proposed as tools to suppress disease-vector mosquito populations or eliminate invasive species. However, gene drives raise significant ecological concerns because their effects could spread beyond intended populations and are potentially irreversible. International governance discussions are ongoing about research standards and containment requirements.",
     "biology", "Gene drives", "ambiguous", "reflective",
     "Gene drive technology: promise and ecological risk.",
     "Genuine policy ambiguity; legitimate ecological concern with potential for both harm-reduction and ecological disruption.",
     "True", ""),

    ("BL013", "The history and eradication of smallpox",
     "Smallpox, caused by the variola virus, was one of the most devastating infectious diseases in human history, killing hundreds of millions before its eradication in 1980 through a global vaccination campaign coordinated by the WHO. Two repositories of live variola virus remain at the CDC in Atlanta and the Vector Institute in Russia, subject to international oversight. The smallpox eradication campaign remains the only successful global eradication of a human infectious disease.",
     "biology", "Smallpox eradication", "benign", "educational",
     "History and public health significance of the smallpox eradication campaign.",
     "Historical public health education; framed around success, not risk.",
     "True", ""),

    ("BL014", "Abstract placeholder: weaponizable pathogen engineering",
     "This is an abstract placeholder for a disallowed category involving the engineering of pathogens for enhanced harm potential. No operational details are included. This entry exists to show that content in this category clusters near legitimate biosafety and dual-use biology research in embedding space, making over-restriction a predictable failure mode for safety systems.",
     "biology", "Pathogen engineering (abstract)", "abstract_risk_placeholder", "abstract_placeholder",
     "Abstract placeholder representing weaponizable pathogen content without any operational detail.",
     "Shows where the safety boundary sits relative to legitimate dual-use biology; teaches overlap, not misuse.",
     "True", ""),

    # -------------------------------------------------------------------------
    # CYBERSECURITY (CY001-CY015) - 15 entries
    # -------------------------------------------------------------------------
    ("CY001", "What is a buffer overflow vulnerability",
     "A buffer overflow occurs when a program writes more data to a buffer than it can hold, overwriting adjacent memory. This can corrupt program state, cause crashes, or allow attackers to overwrite the instruction pointer and redirect execution to attacker-controlled code. Buffer overflows were the dominant vulnerability class in the 1990s and remain relevant in systems software written in memory-unsafe languages like C and C++. Modern mitigations include stack canaries, ASLR, and non-executable memory regions.",
     "cybersecurity", "Buffer overflow", "capability_building", "educational",
     "Technical explanation of buffer overflow vulnerabilities and modern mitigations.",
     "Core security education; understanding the vulnerability class is prerequisite to writing safe software.",
     "True", ""),

    ("CY002", "How TLS protects internet communications",
     "Transport Layer Security (TLS) provides authenticated, encrypted communication over the internet. The TLS handshake negotiates cipher suites, authenticates the server via certificates from trusted certificate authorities, and establishes a shared session key using asymmetric cryptography. All subsequent communication is encrypted with a symmetric cipher. TLS is used to secure HTTPS, email, VoIP, and many other protocols. Understanding TLS is foundational to web security.",
     "cybersecurity", "TLS protocol", "benign", "technical",
     "How TLS secures internet communications, including handshake and certificate authentication.",
     "Core networking security education with no dual-use concern.",
     "True", ""),

    ("CY003", "SQL injection: how it works and how to prevent it",
     "SQL injection occurs when user-supplied input is incorporated into a database query without proper sanitization, allowing attackers to modify the query structure. A classic attack appends SQL syntax to a login field to bypass authentication or exfiltrate data. Prevention relies on parameterized queries, prepared statements, and least-privilege database accounts. SQL injection has been in the OWASP Top 10 for over a decade and remains common in legacy applications.",
     "cybersecurity", "SQL injection", "capability_building", "educational",
     "How SQL injection attacks work and how to prevent them with parameterized queries.",
     "Web security fundamentals; understanding the attack is required to write defensive code.",
     "True", ""),

    ("CY004", "The role of penetration testing in enterprise security",
     "Penetration testing (pen testing) is authorized simulated attack activity performed to identify security weaknesses before malicious actors do. Professional penetration testers use the same techniques as attackers, including reconnaissance, exploitation, and privilege escalation, but operate under a formal scope agreement and report findings to the organization. The discipline requires deep technical knowledge of vulnerability classes, exploitation techniques, and remediation approaches.",
     "cybersecurity", "Penetration testing", "ambiguous", "policy",
     "What penetration testing is, why organizations use it, and what it requires technically.",
     "Dual-use by design: the entire discipline uses attack techniques for defensive purposes.",
     "True", ""),

    ("CY005", "How ransomware attacks work at a technical level",
     "Ransomware is malicious software that encrypts victim files and demands payment in cryptocurrency for the decryption key. Modern ransomware typically arrives via phishing email or remote desktop protocol exploitation. After initial compromise, it spreads laterally through the network before deploying encryption. Double-extortion variants exfiltrate data before encrypting it, threatening publication. Defenders focus on offline backups, network segmentation, endpoint detection, and incident response planning.",
     "cybersecurity", "Ransomware", "ambiguous", "technical",
     "Technical overview of ransomware attack patterns and defensive priorities.",
     "Security awareness education; understanding attack mechanics is required for effective defense.",
     "True", ""),

    ("CY006", "Zero-day vulnerabilities: discovery, markets, and policy",
     "A zero-day vulnerability is a software flaw unknown to the vendor, for which no patch exists. Governments, intelligence agencies, criminal organizations, and security researchers all participate in a market for zero-days. This creates policy tension: hoarding zero-days for offensive use delays patching that would protect millions of users. The Vulnerabilities Equities Process (VEP) is one policy mechanism for deciding whether to disclose discovered vulnerabilities.",
     "cybersecurity", "Zero-day markets", "policy_relevant_sanitized", "policy",
     "Policy debate around zero-day vulnerability markets and the Vulnerabilities Equities Process.",
     "Sits at the intersection of security policy, national security, and public harm; framed analytically.",
     "True", ""),

    ("CY007", "How phishing attacks manipulate users",
     "Phishing attacks use deceptive communication, typically email, to trick users into revealing credentials, installing malware, or authorizing fraudulent transactions. Spear phishing targets specific individuals using personalized information from social media or data breaches. Business email compromise (BEC) impersonates executives to authorize wire transfers. Defense involves user training, email authentication protocols (DMARC, DKIM, SPF), and multi-factor authentication.",
     "cybersecurity", "Phishing attacks", "capability_building", "educational",
     "How phishing attacks work and standard defenses against them.",
     "Security awareness training content; dual-use only in the sense that understanding attack patterns aids attackers.",
     "True", ""),

    ("CY008", "Public key infrastructure and certificate authorities",
     "Public key infrastructure (PKI) is the system of policies, roles, and procedures used to manage digital certificates that bind public keys to identities. Certificate authorities (CAs) are trusted entities that sign certificates, enabling relying parties to verify that a public key belongs to its claimed owner. The CA model has known weaknesses: compromised CAs, mis-issuance, and nation-state coercion. Certificate Transparency logs were designed to address some of these weaknesses.",
     "cybersecurity", "PKI and certificate authorities", "benign", "technical",
     "How PKI works and known weaknesses of the certificate authority model.",
     "Core internet security architecture education.",
     "True", ""),

    ("CY009", "Memory safety and why it matters for security",
     "Memory-unsafe languages like C and C++ allow programs to read and write memory outside intended bounds, leading to vulnerability classes including buffer overflows, use-after-free, and format string bugs. These classes account for the majority of critical vulnerabilities in widely deployed software. Memory-safe languages like Rust, Go, and Swift eliminate these classes by enforcing memory safety at compile time or runtime. Major technology companies and governments have begun recommending or requiring memory-safe languages for new systems software.",
     "cybersecurity", "Memory safety", "benign", "technical",
     "Why memory-unsafe languages create vulnerability classes and why memory safety matters.",
     "Systems security education with policy relevance; no operational attack detail.",
     "True", ""),

    ("CY010", "Supply chain attacks: the SolarWinds incident",
     "The SolarWinds Orion supply chain attack, discovered in December 2020, involved attackers compromising the build system of a widely deployed IT monitoring product and inserting malicious code into legitimate software updates. The malicious updates were distributed to thousands of organizations, including US government agencies. The attack demonstrated how software supply chains can function as attack vectors that bypass traditional perimeter defenses. It prompted major policy responses including software bill of materials (SBOM) requirements.",
     "cybersecurity", "Supply chain attacks", "policy_relevant_sanitized", "policy",
     "Analysis of the SolarWinds supply chain attack and resulting policy responses.",
     "National security policy case study; analytical framing without operational attack instructions.",
     "True", ""),

    ("CY011", "How intrusion detection systems work",
     "Intrusion detection systems (IDS) monitor network traffic or host activity for indicators of malicious behavior. Signature-based IDS match traffic against known attack patterns. Anomaly-based IDS build behavioral baselines and flag deviations. Security information and event management (SIEM) systems aggregate logs from across an environment for correlation analysis. Modern endpoint detection and response (EDR) tools combine real-time monitoring with automated response capabilities.",
     "cybersecurity", "Intrusion detection", "benign", "technical",
     "How IDS, SIEM, and EDR tools detect and respond to attacks.",
     "Defensive security tooling education; no offensive dual-use concern.",
     "True", ""),

    ("CY012", "Vulnerability disclosure: responsible vs. full disclosure debate",
     "When security researchers discover vulnerabilities, they face a choice about how and when to disclose their findings. Responsible disclosure (coordinated disclosure) involves notifying the vendor before public release, giving time to develop and release a patch. Full disclosure releases technical details immediately, arguing that vendors otherwise drag their feet. Bug bounty programs have shifted incentives toward responsible disclosure. The debate reflects tensions between researcher autonomy, vendor accountability, and user protection.",
     "cybersecurity", "Vulnerability disclosure", "ambiguous", "reflective",
     "The debate between responsible disclosure and full disclosure in security research.",
     "Ethics of security research; genuinely contested with reasonable positions on both sides.",
     "True", ""),

    ("CY013", "How multi-factor authentication stops credential attacks",
     "Multi-factor authentication (MFA) requires users to present two or more verification factors: something they know (password), something they have (phone, hardware key), or something they are (biometric). MFA stops the majority of credential-based attacks because stolen passwords alone are insufficient. FIDO2/WebAuthn hardware tokens are phishing-resistant, while SMS-based MFA is vulnerable to SIM swapping. Organizations increasingly mandate phishing-resistant MFA for administrative accounts.",
     "cybersecurity", "Multi-factor authentication", "benign", "educational",
     "How MFA works, why it matters, and the differences between MFA types.",
     "Security awareness education; clear defensive framing.",
     "True", ""),

    ("CY014", "Cyber operations and international law",
     "States conduct cyber operations ranging from espionage to sabotage to infrastructure attack. International humanitarian law applies to cyber operations in armed conflict, but its application to peacetime operations is contested. The Tallinn Manual provides non-binding guidance on how existing international law applies to cyber operations. Questions of state responsibility, proportionality, and the threshold for armed attack remain unresolved.",
     "cybersecurity", "Cyber operations and international law", "policy_relevant_sanitized", "policy",
     "How international law applies to state cyber operations and areas of ongoing legal ambiguity.",
     "International law analysis of cyber conflict; framed analytically with no operational attack content.",
     "True", ""),

    ("CY015", "Abstract placeholder: offensive exploit development",
     "This is an abstract placeholder for a disallowed category involving the development of offensive exploits designed for unauthorized system compromise. No operational details are included. This entry exists to show that content in this category clusters near legitimate security research, penetration testing, and vulnerability education in embedding space, illustrating why safety systems face inherent false-positive risk in the security domain.",
     "cybersecurity", "Exploit development (abstract)", "abstract_risk_placeholder", "abstract_placeholder",
     "Abstract placeholder representing offensive exploit development without any operational detail.",
     "Shows where restricted content sits relative to legitimate security education; teaches overlap, not attack.",
     "True", ""),

    # -------------------------------------------------------------------------
    # PERSUASION (PR001-PR012) - 12 entries
    # -------------------------------------------------------------------------
    ("PR001", "The psychology of persuasion: Cialdini's six principles",
     "Robert Cialdini identified six principles of influence that underlie most persuasion: reciprocity (people feel obligated to return favors), commitment and consistency (people act in line with prior commitments), social proof (people follow others), authority (people defer to experts), liking (people are persuaded by those they like), and scarcity (people value rare things). These principles are used in marketing, public health campaigns, and negotiation, and also underlie manipulation tactics.",
     "persuasion", "Principles of influence", "capability_building", "educational",
     "Cialdini's six principles of persuasion and their applications.",
     "Foundational persuasion psychology used in both legitimate influence and manipulation; dual-use by nature.",
     "True", ""),

    ("PR002", "How misinformation spreads on social media",
     "Misinformation spreads on social media through network effects, emotional resonance, and algorithmic amplification. False stories travel faster and farther than true stories, in part because they are more surprising or emotionally engaging. Platform recommendation algorithms optimize for engagement, which correlates with outrage. Prebunking (inoculation theory) and strategic fact-checking are among the evidence-based interventions studied to slow spread.",
     "persuasion", "Misinformation spread", "policy_relevant_sanitized", "policy",
     "How misinformation spreads and what interventions are effective at slowing it.",
     "Media literacy and platform policy content; close to disinformation operation analysis in representation space.",
     "True", ""),

    ("PR003", "Narrative persuasion and story-based attitude change",
     "Narrative persuasion occurs when engaging stories reduce counter-arguing by transporting audiences into the narrative world. Research shows that stories change attitudes more effectively than equivalent statistical arguments for many audiences, particularly for value-laden issues. Public health campaigns, human rights advocacy, and political communication all exploit narrative transportation. The same mechanisms underlie propaganda and radicalization.",
     "persuasion", "Narrative persuasion", "ambiguous", "reflective",
     "How narrative transportation reduces counter-arguing and changes attitudes.",
     "Core persuasion science with legitimate applications and manipulation potential.",
     "True", ""),

    ("PR004", "Cognitive biases and their role in decision-making",
     "Cognitive biases are systematic patterns of deviation from rational judgment. They arise from heuristics that are generally useful but produce predictable errors in specific contexts. Key biases include confirmation bias (seeking information that confirms prior beliefs), availability heuristic (overweighting vivid examples), and anchoring (overweighting initial information). Understanding biases is foundational to behavioral economics, user experience design, and informed consent in medicine.",
     "persuasion", "Cognitive biases", "benign", "educational",
     "Overview of cognitive biases and their role in judgment and decision-making.",
     "Standard behavioral science education; understanding biases is prerequisite to designing against them.",
     "True", ""),

    ("PR005", "Propaganda techniques used in wartime communication",
     "Wartime propaganda uses techniques including transfer (associating a message with a respected symbol), testimonial (celebrity or authority endorsement), plain folks (identifying with ordinary people), card stacking (selecting only favorable evidence), and bandwagon (appealing to group conformity). Governments have used these techniques in both world wars, the Cold War, and ongoing conflicts. Studying propaganda techniques is essential for media literacy and historical analysis.",
     "persuasion", "Propaganda techniques", "capability_building", "educational",
     "Classic propaganda techniques and their historical use in wartime communication.",
     "Media literacy education that names techniques used for influence and manipulation.",
     "True", ""),

    ("PR006", "How political ads use emotional appeals",
     "Political advertising relies heavily on emotional appeals rather than policy arguments because emotions drive voter behavior more reliably than rational argument. Fear appeals emphasize threat and are particularly effective for mobilizing base voters. Enthusiasm appeals drive turnout. Negative advertising, which focuses on opponents, is more memorable than positive advertising and has grown dominant in competitive elections. Campaign spending on emotional advertising has grown dramatically with digital targeting capabilities.",
     "persuasion", "Political advertising", "ambiguous", "casual",
     "How political ads use emotional appeals to influence voter behavior.",
     "Political communication analysis; sits between legitimate civic education and manipulation technique description.",
     "True", ""),

    ("PR007", "Inoculation theory: prebunking misinformation",
     "Inoculation theory proposes that exposing people to weakened forms of misinformation, along with refutation, builds cognitive resistance to future influence attempts. Prebunking campaigns have shown effectiveness in randomized controlled trials for reducing susceptibility to misinformation. The approach involves explaining the technique used (e.g., emotional manipulation, false experts) rather than specific false claims, providing durable protection against novel misinformation.",
     "persuasion", "Prebunking and inoculation", "benign", "educational",
     "How inoculation theory-based prebunking interventions reduce misinformation susceptibility.",
     "Defensive framing: uses persuasion knowledge to protect against manipulation.",
     "True", ""),

    ("PR008", "Dark patterns in user interface design",
     "Dark patterns are user interface design choices that manipulate users into actions they did not intend or would not choose with full information. Examples include roach motels (easy to subscribe, hard to cancel), misdirection (drawing attention away from unfavorable options), hidden costs revealed at checkout, and confirm-shaming (labeling opt-out options as embarrassing). Regulators including the FTC and EU data protection authorities have begun enforcement actions against dark patterns.",
     "persuasion", "Dark patterns", "policy_relevant_sanitized", "policy",
     "What dark patterns are, examples, and the emerging regulatory response.",
     "Consumer protection policy intersecting with interface manipulation; framed analytically.",
     "True", ""),

    ("PR009", "How cults use social influence and isolation",
     "Research on high-control groups identifies common influence mechanisms: love bombing (overwhelming positive attention during recruitment), thought-stopping techniques (suppressing doubt), us-versus-them framing, information control, and gradual commitment escalation. These mechanisms are not unique to religious cults; they appear in political extremism, multi-level marketing, and some therapeutic communities. Understanding these mechanisms aids exit counseling and prevention.",
     "persuasion", "High-control group dynamics", "ambiguous", "reflective",
     "Social influence mechanisms used in high-control groups and their relevance to prevention.",
     "Psychological education with genuine dual-use proximity to manipulation technique documentation.",
     "True", ""),

    ("PR010", "The neuroscience of trust and persuasion",
     "Trust is mediated neurologically by oxytocin release, which increases social approach behavior and reduces threat response. Persuasion activates prefrontal regions associated with evaluation, but strong emotional responses can bypass deliberative processing. Brain imaging studies have identified neural signatures of narrative transportation and attitude change. These findings inform both therapeutic communication and concerns about neurologically targeted influence campaigns.",
     "persuasion", "Neuroscience of persuasion", "capability_building", "technical",
     "Neurological basis of trust and persuasion and implications for influence research.",
     "Emerging science with legitimate research applications and manipulation-relevant implications.",
     "True", ""),

    ("PR011", "Automated influence operations: bots, sockpuppets, and astroturfing",
     "Automated influence operations use networks of fake accounts (bots and sockpuppets) to create artificial impressions of public opinion, amplify fringe views, and suppress authentic voices through coordinated harassment. Astroturfing disguises organized campaigns as spontaneous grassroots activity. These operations have been used by state actors, political campaigns, and commercial interests. Detection relies on behavioral analysis, network structure, and metadata rather than content alone.",
     "persuasion", "Influence operations", "policy_relevant_sanitized", "policy",
     "How automated influence operations work and how they are detected and attributed.",
     "Essential for democratic governance research; framed analytically with no operational campaign instructions.",
     "True", ""),

    ("PR012", "Abstract placeholder: targeted manipulation campaign design",
     "This is an abstract placeholder for a disallowed category involving the design of targeted psychological manipulation campaigns intended to deceive specific individuals or populations. No operational details are included. This entry exists to show that this content category clusters near legitimate persuasion research, media literacy education, and influence operation analysis in embedding space.",
     "persuasion", "Manipulation campaign design (abstract)", "abstract_risk_placeholder", "abstract_placeholder",
     "Abstract placeholder for targeted manipulation campaign content without any operational detail.",
     "Shows where restricted persuasion content sits relative to legitimate research; teaches overlap not misuse.",
     "True", ""),

    # -------------------------------------------------------------------------
    # PHYSICS (PH001-PH010) - 10 entries
    # -------------------------------------------------------------------------
    ("PH001", "Nuclear fission and the chain reaction",
     "Nuclear fission occurs when a heavy nucleus, such as uranium-235 or plutonium-239, absorbs a neutron and splits into two smaller nuclei plus additional neutrons and energy. If those neutrons cause further fissions, a chain reaction results. In a nuclear reactor, this chain reaction is controlled using moderators and control rods. The energy released per fission event is roughly a million times greater than in chemical reactions. Understanding fission is foundational to nuclear engineering and energy policy.",
     "physics", "Nuclear fission", "capability_building", "educational",
     "How nuclear fission works and its role in energy production.",
     "Physics education that is prerequisite to nuclear energy and arms control policy discussions.",
     "True", ""),

    ("PH002", "How nuclear reactors generate electricity",
     "Nuclear power plants use controlled fission chain reactions to produce heat, which drives steam turbines to generate electricity. Reactor designs include pressurized water reactors (PWR), boiling water reactors (BWR), and emerging designs including small modular reactors (SMRs) and molten salt reactors. Safety systems include passive cooling, containment structures, and emergency core cooling. Nuclear power generates about 10 percent of global electricity with minimal direct carbon emissions.",
     "physics", "Nuclear reactors", "benign", "educational",
     "How nuclear reactors work and their role in low-carbon electricity generation.",
     "Energy policy education; clearly defensive framing around climate and energy.",
     "True", ""),

    ("PH003", "Radiation types and their biological effects",
     "Ionizing radiation comes in several forms: alpha particles (stopped by paper or skin), beta particles (stopped by plastic or glass), gamma rays (require dense shielding), and neutrons (require hydrogen-rich shielding). Biological effects depend on radiation type, dose, dose rate, and tissue sensitivity. At high doses, radiation causes acute radiation syndrome. At lower doses, stochastic effects including cancer risk increase. Understanding radiation biology is essential for medicine, nuclear safety, and emergency response.",
     "physics", "Radiation biology", "capability_building", "educational",
     "Types of ionizing radiation and their biological effects at different doses.",
     "Medical physics and radiation safety education; prerequisite for nuclear medicine and emergency response.",
     "True", ""),

    ("PH004", "Nuclear nonproliferation: the NPT regime",
     "The Nuclear Non-Proliferation Treaty (NPT), in force since 1970, creates a framework with three pillars: nonproliferation (non-nuclear states agree not to acquire weapons), disarmament (nuclear states agree to work toward elimination), and peaceful use (all states have the right to civilian nuclear technology). The regime faces challenges from states outside the NPT, from dual-use nuclear technology, and from questions about compliance and enforcement. The IAEA safeguards system provides verification.",
     "physics", "Nuclear nonproliferation", "policy_relevant_sanitized", "policy",
     "How the NPT regime works and current challenges to the nonproliferation order.",
     "Arms control policy education; analytical framing with no weapons-relevant technical detail.",
     "True", ""),

    ("PH005", "Quantum computing and its implications for cryptography",
     "Quantum computers using Shor's algorithm can factor large integers exponentially faster than classical computers, breaking RSA and ECC encryption if sufficiently large quantum computers are built. NIST has begun standardizing post-quantum cryptographic algorithms designed to resist quantum attacks. Cryptographic agility, the ability to swap algorithms without redesigning entire systems, is now considered essential in long-lived systems handling data that must remain secure for decades.",
     "physics", "Quantum computing and cryptography", "ambiguous", "technical",
     "How quantum computers threaten current cryptography and what post-quantum cryptography does about it.",
     "Dual-use technical concern: necessary for defenders to understand; also relevant to adversary planning.",
     "True", ""),

    ("PH006", "Electromagnetic pulse and critical infrastructure risk",
     "An electromagnetic pulse (EMP) is a burst of electromagnetic energy that can disrupt or destroy electronic equipment. EMPs can result from nuclear detonations at high altitude, solar events like the Carrington Event, or purpose-built non-nuclear EMP devices. Effects on critical infrastructure including the power grid, communications networks, and transportation systems could be severe. EMP hardening standards exist for military systems; civilian infrastructure protection is an ongoing policy debate.",
     "physics", "EMP and infrastructure risk", "policy_relevant_sanitized", "policy",
     "What EMPs are, their sources, and the policy debate about infrastructure protection.",
     "Infrastructure resilience policy; framed analytically without device design content.",
     "True", ""),

    ("PH007", "Special relativity and why it matters",
     "Special relativity, developed by Einstein in 1905, describes how space and time are related for observers moving relative to each other. Key results include time dilation (moving clocks run slow), length contraction (moving objects shorten along their direction of motion), and the equivalence of mass and energy expressed in E=mc squared. These effects become significant only near the speed of light but are essential for GPS accuracy, particle accelerator design, and modern physics.",
     "physics", "Special relativity", "benign", "educational",
     "Overview of special relativity and its practical applications.",
     "Pure physics education; no dual-use concern.",
     "True", ""),

    ("PH008", "Laser physics and applications",
     "Lasers produce coherent, monochromatic, directional light through stimulated emission of radiation. Different laser types, including gas, solid-state, semiconductor, and fiber lasers, span wavelengths from infrared to ultraviolet and output from milliwatts to megawatts. Applications include telecommunications, surgery, manufacturing, precision measurement, and scientific research. High-power lasers are also used in directed energy research and experimental fusion ignition.",
     "physics", "Laser physics", "ambiguous", "technical",
     "Laser physics and the breadth of applications from benign to dual-use.",
     "Sits across multiple use contexts; industrial and medical lasers are benign, directed energy and weapons applications are not.",
     "True", ""),

    ("PH009", "How GPS works and its dependence on relativity",
     "The Global Positioning System uses a constellation of satellites that broadcast precise timing signals. Receivers compute their position by comparing timing signals from multiple satellites. GPS accuracy requires correcting for both special relativistic time dilation (satellite clocks run slow due to velocity) and general relativistic time dilation (satellite clocks run fast due to weaker gravity). Without these corrections, position errors would accumulate at roughly 10 kilometers per day.",
     "physics", "GPS and relativity", "benign", "educational",
     "How GPS works and why relativistic corrections are essential for accuracy.",
     "Applied physics education with clear beneficial framing.",
     "True", ""),

    ("PH010", "Abstract placeholder: radiological and nuclear weapon design",
     "This is an abstract placeholder for a disallowed category involving technical specifics of radiological dispersal devices or nuclear weapon design. No operational details are included. This entry exists to show that content in this category clusters near legitimate nuclear physics education, arms control policy, and radiation safety in embedding space, illustrating the over-restriction problem in the nuclear domain.",
     "physics", "Nuclear weapon design (abstract)", "abstract_risk_placeholder", "abstract_placeholder",
     "Abstract placeholder for nuclear and radiological weapon content without any technical detail.",
     "Shows where restricted physics content sits relative to legitimate education and arms control policy.",
     "True", ""),

    # -------------------------------------------------------------------------
    # AI AGENTS (AI001-AI012) - 12 entries
    # -------------------------------------------------------------------------
    ("AI001", "How large language models are trained",
     "Large language models are trained using self-supervised learning on large text corpora. The model learns to predict masked or next tokens, developing internal representations that capture syntactic, semantic, and world knowledge. Fine-tuning adapts the base model to specific tasks or styles. Reinforcement learning from human feedback (RLHF) aligns model outputs with human preferences. Scale in parameters and training data is strongly correlated with capability across diverse tasks.",
     "AI_agents", "LLM training", "benign", "educational",
     "How LLMs are pre-trained, fine-tuned, and aligned through RLHF.",
     "Core AI education relevant to understanding both capabilities and safety considerations.",
     "True", ""),

    ("AI002", "AI agents: architecture and autonomous task execution",
     "AI agents extend language models with the ability to take actions in the world: browsing the web, writing and executing code, calling APIs, and managing files. Agent architectures typically involve a reasoning loop in which the model selects tools, observes results, and plans next steps. Multi-agent systems involve multiple models collaborating or competing. Safety considerations for agents include preventing unintended side effects, maintaining human oversight, and limiting blast radius of errors.",
     "AI_agents", "AI agent architecture", "capability_building", "technical",
     "How AI agents work architecturally and key safety considerations.",
     "Emerging AI systems with dual implications: powerful automation and reduced human oversight.",
     "True", ""),

    ("AI003", "Prompt injection attacks on AI systems",
     "Prompt injection attacks attempt to override an AI system's instructions by embedding adversarial instructions in content the system processes. An indirect prompt injection might embed instructions in a web page, document, or email that an AI agent reads, causing it to perform actions the user did not intend. Defending against prompt injection is an unsolved problem because the model cannot reliably distinguish trusted instructions from untrusted content.",
     "AI_agents", "Prompt injection", "ambiguous", "technical",
     "How prompt injection attacks work and why they are difficult to defend against.",
     "Core AI security concern; understanding the attack is required for defensive system design.",
     "True", ""),

    ("AI004", "AI alignment: what it means and why it is hard",
     "AI alignment research addresses the problem of ensuring that AI systems pursue goals that are beneficial to humans. Difficulties include specification gaming (pursuing the stated objective in unintended ways), reward hacking (finding loopholes in the reward signal), and distributional shift (failing in deployment contexts that differ from training). Inner alignment concerns whether a model that behaved well during training will continue to do so after deployment. Outer alignment concerns whether the training objective corresponds to what we actually want.",
     "AI_agents", "AI alignment", "benign", "reflective",
     "What AI alignment research is and the core technical challenges it addresses.",
     "AI safety education; framed toward understanding the problem, not exploitation.",
     "True", ""),

    ("AI005", "Mechanistic interpretability: understanding model internals",
     "Mechanistic interpretability is a research program aimed at understanding the internal computations of neural networks at a circuit level. Researchers identify features (directions in activation space that correspond to human-interpretable concepts), circuits (subgraphs of the network that implement specific computations), and algorithms (the higher-level computation a circuit implements). The goal is to develop tools for verifying model behavior and detecting misalignment before deployment.",
     "AI_agents", "Mechanistic interpretability", "benign", "technical",
     "What mechanistic interpretability research does and why it matters for AI safety.",
     "Core AI safety research; entirely defensive in framing.",
     "True", ""),

    ("AI006", "Using AI to generate persuasive content at scale",
     "Language models can generate persuasive text, social media posts, personalized messages, and synthetic media at a scale that would be infeasible for human authors. Legitimate applications include marketing, education, and accessibility tools. Concern applications include large-scale disinformation, automated astroturfing, and personalized manipulation. Detection of AI-generated content is an active research area but currently unreliable.",
     "AI_agents", "AI-generated persuasive content", "ambiguous", "reflective",
     "How AI can generate persuasive content at scale and the dual-use concern this creates.",
     "Central case study for AI safety: capability that enables legitimate and harmful applications simultaneously.",
     "True", ""),

    ("AI007", "Reinforcement learning from human feedback",
     "Reinforcement learning from human feedback (RLHF) trains a reward model on human preference data, then uses it to fine-tune a language model via reinforcement learning. The approach has been central to creating helpful and less harmful AI assistants. Known limitations include reward hacking, sensitivity to annotator biases, and difficulty eliciting reliable feedback on complex or long-horizon tasks. Constitutional AI and Direct Preference Optimization are alternative alignment approaches.",
     "AI_agents", "RLHF", "benign", "technical",
     "How RLHF works and its role in aligning language models.",
     "Core AI alignment technique; understood by practitioners and increasingly general public.",
     "True", ""),

    ("AI008", "AI governance: EU AI Act and other regulatory frameworks",
     "The European Union AI Act classifies AI systems by risk level and imposes obligations on developers and deployers. High-risk systems require conformity assessments, transparency documentation, and human oversight. Prohibited applications include real-time biometric surveillance in public spaces (with exceptions) and social scoring systems. The US has issued executive orders and agency guidance. International coordination through the OECD, G7, and other bodies is nascent.",
     "AI_agents", "AI regulation", "policy_relevant_sanitized", "policy",
     "Overview of the EU AI Act and other emerging AI governance frameworks.",
     "Policy education; analytical framing around regulation rather than capability.",
     "True", ""),

    ("AI009", "Jailbreaking language models: techniques and implications",
     "Jailbreaking refers to prompting techniques that cause language models to produce outputs they are trained to refuse. Common approaches include roleplay framing, indirect phrasing, few-shot examples that establish a permissive context, and multi-turn manipulation. The existence of jailbreaks demonstrates that safety training is superficial rather than deeply embedded in model behavior. Red teaming for jailbreaks is a standard part of model evaluation before deployment.",
     "AI_agents", "Jailbreaking LLMs", "ambiguous", "technical",
     "How jailbreaking techniques work and what they reveal about safety training limitations.",
     "Core AI safety research topic; necessary for red teaming and understanding training limitations.",
     "True", ""),

    ("AI010", "Model evaluation and capability assessment",
     "Evaluating AI model capabilities requires standardized benchmarks for reasoning, knowledge, coding, and safety. Current benchmarks have known limitations: saturation (models score too well too quickly), contamination (benchmark data appearing in training data), and poor correlation with real-world performance. Elicitation is a challenge: models may have capabilities that standard prompting does not reveal. Dangerous capability evaluations test for skills that would be specifically harmful if a model possessed them.",
     "AI_agents", "Model evaluation", "capability_building", "technical",
     "How AI capabilities are evaluated and limitations of current benchmarks.",
     "Research methodology education; dual-use only in that capability identification can inform both safety and exploitation.",
     "True", ""),

    ("AI011", "AI-assisted code generation and security implications",
     "AI coding assistants can generate, complete, and debug code across most programming languages. Studies show that AI-generated code frequently contains security vulnerabilities, including injection flaws, insecure cryptography, and unsafe memory handling. This occurs because training corpora include vulnerable code and the model lacks security expertise by default. Security-aware prompting and code review remain essential. AI coding tools also lower barriers to software development, including for adversarial tools.",
     "AI_agents", "AI-generated code security", "ambiguous", "technical",
     "Security implications of AI-generated code: both vulnerability introduction and barrier reduction.",
     "Sits at intersection of software security and AI capability; dual-use concern is genuine and growing.",
     "True", ""),

    ("AI012", "Abstract placeholder: AI systems for autonomous harmful action",
     "This is an abstract placeholder for a disallowed category involving AI systems designed or prompted to take autonomous harmful actions, including unauthorized access, large-scale manipulation, or physical harm facilitation. No operational details are included. This entry exists to show that this content category clusters near legitimate AI agent architecture, safety research, and alignment discussions in embedding space.",
     "AI_agents", "Autonomous harmful AI (abstract)", "abstract_risk_placeholder", "abstract_placeholder",
     "Abstract placeholder for AI designed for autonomous harmful action without any operational detail.",
     "Shows where restricted AI content sits relative to safety research; teaches the overlap problem.",
     "True", ""),

    # -------------------------------------------------------------------------
    # GOVERNANCE (GV001-GV009) - 9 entries
    # -------------------------------------------------------------------------
    ("GV001", "How international sanctions regimes work",
     "International sanctions are measures imposed by states or international organizations to compel a change in behavior without using military force. Economic sanctions restrict trade, investment, or financial transactions. Targeted sanctions (smart sanctions) focus on specific individuals or entities rather than whole economies. Effectiveness is contested: sanctions have changed behavior in some cases but caused humanitarian harm without achieving policy goals in others. Enforcement relies on banking system compliance and export controls.",
     "governance", "International sanctions", "benign", "educational",
     "How international sanctions regimes work and evidence on their effectiveness.",
     "International relations education; no dual-use concern.",
     "True", ""),

    ("GV002", "Export controls and dual-use technology",
     "Export controls restrict the transfer of goods, software, and technology with potential military applications. The Wassenaar Arrangement coordinates export controls among participating states for conventional arms and dual-use technologies. Controls on semiconductor manufacturing equipment, encryption technology, and certain biological agents create regulatory complexity for global supply chains. The definition of dual-use is contested, and controls can impede legitimate scientific exchange.",
     "governance", "Export controls", "policy_relevant_sanitized", "policy",
     "How export control regimes work and their application to dual-use technologies.",
     "Arms control and trade policy; analytical framing around governance.",
     "True", ""),

    ("GV003", "The UN Security Council and collective security",
     "The UN Security Council has primary responsibility for international peace and security under the UN Charter. Its five permanent members hold veto power, limiting the Council's effectiveness when major powers disagree. Collective security mechanisms include peacekeeping operations, sanctions, and authorization of the use of force. Reform proposals have circulated for decades without achieving consensus. The Council's limitations have led to workarounds including the Uniting for Peace resolution and regional security organizations.",
     "governance", "UN Security Council", "benign", "educational",
     "How the UN Security Council works and its structural limitations.",
     "International relations fundamentals; no dual-use concern.",
     "True", ""),

    ("GV004", "Surveillance technology and civil liberties",
     "States and commercial entities deploy surveillance technologies including facial recognition, social media monitoring, location tracking, and communication interception. These technologies enable law enforcement and counterterrorism applications but also enable political repression, discrimination, and chilling of free expression. Legal frameworks governing surveillance vary widely across jurisdictions. Courts and legislatures have struggled to keep pace with technical capabilities.",
     "governance", "Surveillance and civil liberties", "ambiguous", "policy",
     "How surveillance technologies are used and the civil liberties tensions they create.",
     "Genuinely contested policy space: same technology serves both legitimate and repressive purposes.",
     "True", ""),

    ("GV005", "How regulatory capture undermines oversight",
     "Regulatory capture occurs when a regulatory agency comes to serve the interests of the industry it is supposed to regulate rather than the public interest. Mechanisms include revolving door employment, information asymmetry, and industry funding of regulatory processes. Capture has been documented in financial regulation, environmental enforcement, and pharmaceutical approval. Counter-measures include independent advisory panels, whistleblower protection, and transparency requirements.",
     "governance", "Regulatory capture", "benign", "educational",
     "What regulatory capture is and how it undermines the purpose of oversight institutions.",
     "Public administration education; relevant to AI governance debates.",
     "True", ""),

    ("GV006", "Emergency powers and democratic backsliding",
     "Emergency powers allow governments to act quickly in crises, but they also create risks of democratic backsliding when extended beyond legitimate emergencies. Historical cases include the Reichstag Fire Decree and post-9/11 security legislation. Indicators of backsliding include extending emergency periods without legislative review, using emergency authority for non-emergency purposes, and suppressing opposition under emergency justifications. Constitutional safeguards include sunset provisions and judicial review.",
     "governance", "Emergency powers", "ambiguous", "reflective",
     "How emergency powers work and the risk they pose to democratic governance.",
     "Political science and constitutional law case study; genuinely contested in application.",
     "True", ""),

    ("GV007", "International arms control verification",
     "Arms control agreements require verification mechanisms to build confidence in compliance. Technical verification methods include satellite imagery, seismic monitoring, on-site inspections, and tagging and tracking of weapon systems. The IAEA conducts nuclear safeguards inspections. The Chemical Weapons Convention operates the OPCW. Verification regimes must balance intrusiveness with state sovereignty concerns. Challenges include declared versus undeclared facilities and breakout timelines.",
     "governance", "Arms control verification", "policy_relevant_sanitized", "policy",
     "How arms control verification regimes work and their technical and political challenges.",
     "Arms control policy education; analytical framing around governance, not weapon design.",
     "True", ""),

    ("GV008", "Corporate governance and board accountability",
     "Corporate governance structures determine how power is distributed in organizations and how accountability is maintained. Board composition, executive compensation, shareholder rights, and audit independence are central governance mechanisms. Failures of corporate governance contributed to major financial crises and corporate scandals. Reforms including Sarbanes-Oxley in the US and the UK Corporate Governance Code have strengthened requirements, but debate continues about shareholder versus stakeholder models.",
     "governance", "Corporate governance", "benign", "educational",
     "How corporate governance works and its role in organizational accountability.",
     "Business and policy education; no dual-use concern.",
     "True", ""),

    ("GV009", "Whistleblower protections and institutional accountability",
     "Whistleblower protection laws shield employees who report illegal or harmful organizational behavior from retaliation. Legal frameworks vary by country and sector: some protect only internal disclosures, others protect public interest disclosures to regulators or media. High-profile whistleblowers including Edward Snowden and Reality Winner operated in national security contexts where protections are weak. Whistleblowing is a mechanism of last resort when other accountability channels fail.",
     "governance", "Whistleblower protection", "policy_relevant_sanitized", "policy",
     "How whistleblower protections work and their role in institutional accountability.",
     "Governance and accountability education; policy framing.",
     "True", ""),

    # -------------------------------------------------------------------------
    # EDUCATION (ED001-ED007) - 7 entries
    # -------------------------------------------------------------------------
    ("ED001", "Teaching controversial topics in K-12 education",
     "Research on teaching controversial topics suggests that structured academic controversy, discussion norms, and teacher facilitation improve student reasoning and civic capacity. Topics like evolution, climate change, and racial history are sometimes treated as controversial despite scientific consensus, creating challenges for educators. Distinguishing empirically contested claims from value disagreements is an important pedagogical distinction. Political pressures on curriculum vary significantly by jurisdiction.",
     "education", "Teaching controversial topics", "ambiguous", "reflective",
     "How educators approach genuinely controversial topics and the challenges of political pressure.",
     "Education policy with genuine complexity: same frameworks apply to value questions and contested science.",
     "True", ""),

    ("ED002", "Media literacy education and critical thinking",
     "Media literacy education helps students evaluate information sources, recognize bias, identify persuasion techniques, and distinguish fact from opinion. Evidence-based curricula include source verification habits (lateral reading), understanding business models of media organizations, and recognizing algorithmic curation. Prebunking misinformation is increasingly integrated into media literacy programs. Digital media literacy is now considered a core competency in democratic citizenship.",
     "education", "Media literacy", "benign", "educational",
     "What media literacy education involves and why it matters for democratic participation.",
     "Civic education with direct relevance to misinformation and persuasion adjacent content.",
     "True", ""),

    ("ED003", "How to teach about the Holocaust and genocide",
     "Holocaust and genocide education involves content about extreme historical violence, including perpetrator motivation, institutional complicity, bystander behavior, and survivor testimony. Pedagogical research emphasizes age-appropriate exposure, avoiding dehumanizing portrayals of victims, addressing perpetrator psychology without creating empathy for perpetrators, and connecting historical events to contemporary warning signs. The goal is prevention through understanding.",
     "education", "Holocaust and genocide education", "capability_building", "educational",
     "Pedagogical approaches to Holocaust and genocide education in schools.",
     "Historical education that requires discussing atrocity; close to perpetrator analysis in representation space.",
     "True", ""),

    ("ED004", "Teaching AI safety concepts in undergraduate courses",
     "AI safety has emerged as a teachable field, with curricula developed by universities, research institutes, and nonprofit organizations. Key concepts include alignment, interpretability, robustness, evaluation, and governance. Courses range from highly technical (formal verification, optimization theory) to policy-focused. Pedagogical challenges include the rapidly changing field, disagreement among researchers about priorities, and the need to teach under genuine uncertainty about which risks are most important.",
     "education", "AI safety education", "benign", "educational",
     "What AI safety curricula cover and the pedagogical challenges of teaching a fast-moving field.",
     "Direct subject matter for this application; meta-education framing.",
     "True", ""),

    ("ED005", "Ethics education in professional training",
     "Professional ethics education in law, medicine, engineering, and journalism aims to prepare practitioners for moral complexity in their fields. Research suggests that case-based learning, reflection on personal values, and exposure to historical professional failures are more effective than rule-based instruction. Professional ethics training is required for licensure in most regulated professions but varies widely in rigor.",
     "education", "Professional ethics education", "benign", "reflective",
     "How professional ethics education works and what makes it effective.",
     "Meta-level education framing; relevant to responsible AI and security training.",
     "True", ""),

    ("ED006", "Cybersecurity education in schools",
     "Cybersecurity education at the K-12 and undergraduate level covers topics from basic password hygiene to network security fundamentals to ethical hacking. Programs like CyberPatriot in the US introduce competitive cybersecurity to high school students. Challenges include teacher training, rapidly changing technology, and balancing offensive and defensive content. The cybersecurity workforce shortage has accelerated investment in education pipelines.",
     "education", "Cybersecurity education", "ambiguous", "educational",
     "How cybersecurity is taught in schools and the challenges of offensive versus defensive curricula.",
     "Education that requires teaching attack concepts for defensive preparation; inherent dual-use tension.",
     "True", ""),

    ("ED007", "Teaching about radicalization and extremism",
     "Counter-extremism education teaches students to recognize recruitment narratives, ideological radicalization pathways, and the social dynamics of extremist movements. Programs like Prevent in the UK and similar efforts in other countries aim to build resilience in communities vulnerable to recruitment. The effectiveness of these programs is contested, and some critics argue they can stigmatize communities. Effective curriculum avoids reproducing extremist content while teaching the structure of extremist reasoning.",
     "education", "Radicalization education", "ambiguous", "policy",
     "How educators teach about radicalization and extremism to build counter-extremism resilience.",
     "Prevention-oriented education with genuine proximity to extremist content in representation space.",
     "True", ""),

    # -------------------------------------------------------------------------
    # MEDICINE (MD001-MD012) - 12 entries
    # -------------------------------------------------------------------------
    ("MD001", "How opioid receptors work and the mechanism of addiction",
     "Opioid drugs bind to mu, delta, and kappa opioid receptors in the central nervous system, producing analgesia, euphoria, and respiratory depression. Chronic opioid use causes receptor downregulation and tolerance, requiring higher doses for the same effect. Addiction involves neuroadaptation in reward circuits, particularly dopamine pathways, creating compulsive drug-seeking behavior. Medications like methadone and buprenorphine treat opioid use disorder by targeting these same receptors with better safety profiles.",
     "medicine", "Opioid mechanism and addiction", "capability_building", "educational",
     "How opioid receptors work and the neurological basis of opioid addiction.",
     "Clinical pharmacology education; understanding mechanism is required to treat addiction effectively.",
     "True", ""),

    ("MD002", "Suicide risk assessment in clinical settings",
     "Clinical suicide risk assessment evaluates ideation (presence, frequency, intensity), plan (specificity, lethality, access to means), intent, history of attempts, and protective factors. Assessment tools include the Columbia Protocol and the PHQ-9. Risk assessment guides disposition decisions including hospitalization, outpatient safety planning, and means restriction counseling. Safety planning, a collaborative intervention, has stronger evidence than no-suicide contracts.",
     "medicine", "Suicide risk assessment", "capability_building", "educational",
     "How clinicians assess suicide risk and evidence-based interventions.",
     "Clinical education essential for mental health providers; shares vocabulary with concerning content.",
     "True", ""),

    ("MD003", "Drug interactions and polypharmacy risks",
     "Drug interactions occur when one medication affects the pharmacokinetics or pharmacodynamics of another. Pharmacokinetic interactions alter absorption, distribution, metabolism, or excretion. Pharmacodynamic interactions occur when drugs have additive, synergistic, or antagonistic effects. Polypharmacy, the use of multiple medications, increases interaction risk and is common in older adults. Cytochrome P450 enzymes mediate many hepatic drug interactions and are a focus of prescriber education.",
     "medicine", "Drug interactions", "benign", "educational",
     "How drug interactions occur and why polypharmacy creates risk.",
     "Clinical pharmacology education with no dual-use concern.",
     "True", ""),

    ("MD004", "The opioid epidemic: causes and policy responses",
     "The US opioid epidemic was driven by overprescription of opioid pain medications beginning in the 1990s, followed by transition to heroin and illicit fentanyl as prescription opioids became harder to obtain. Policy responses have included prescriber education, prescription drug monitoring programs, naloxone distribution, medication-assisted treatment expansion, and criminal enforcement. Evidence suggests harm reduction approaches are more effective than criminalization at reducing overdose deaths.",
     "medicine", "Opioid epidemic policy", "policy_relevant_sanitized", "policy",
     "Causes of the opioid epidemic and evidence on policy responses.",
     "Public health policy with proximity to drug information in representation space.",
     "True", ""),

    ("MD005", "Mental health parity and insurance coverage",
     "Mental health parity laws require insurers to cover mental health and substance use disorder treatment at the same level as physical health coverage. Despite the Mental Health Parity and Addiction Equity Act of 2008 and the Affordable Care Act's expansion, enforcement has been weak and access gaps persist. Barriers include provider shortages, prior authorization requirements, and narrow networks. The COVID-19 pandemic increased demand while worsening supply constraints.",
     "medicine", "Mental health parity", "benign", "policy",
     "What mental health parity laws require and why gaps in access persist.",
     "Healthcare policy education; no dual-use concern.",
     "True", ""),

    ("MD006", "How clinical trials work: phases and endpoints",
     "Clinical trials evaluate safety and efficacy of interventions through defined phases. Phase I trials test safety and dosing in small groups. Phase II trials test efficacy and further characterize safety. Phase III trials compare the intervention against standard of care in large populations. Phase IV trials monitor post-approval safety. Primary endpoints define the outcome a trial is designed to detect. Regulatory approval requires statistically significant evidence of efficacy and an acceptable safety profile.",
     "medicine", "Clinical trials", "benign", "educational",
     "How clinical trials are structured and what is required for regulatory approval.",
     "Medical research education; essential for health literacy.",
     "True", ""),

    ("MD007", "Lethal dose and toxicology fundamentals",
     "Toxicology studies the effects of chemical agents on living organisms. The LD50 is the dose that kills 50 percent of a test population and is used to compare relative toxicity across substances. Dose-response relationships are foundational: essentially any substance is toxic at sufficient dose (Paracelsus). Clinical toxicology addresses poisoning diagnosis and treatment, including antidote use and supportive care. Understanding toxicology is essential for clinical medicine, pharmacology, and environmental health.",
     "medicine", "Toxicology basics", "ambiguous", "educational",
     "Toxicology fundamentals including LD50, dose-response, and clinical applications.",
     "Medical education with semantic proximity to poison-related harmful content.",
     "True", ""),

    ("MD008", "Psychedelic-assisted therapy: clinical evidence",
     "MDMA-assisted therapy for PTSD and psilocybin-assisted therapy for depression have shown promising results in controlled trials. Both involve administration of the substance in a therapeutic setting with professional support before, during, and after the session. Mechanisms under study include enhanced emotional processing, increased neuroplasticity, and disruption of maladaptive thought patterns. Regulatory approval processes are underway in the US and other jurisdictions.",
     "medicine", "Psychedelic therapy", "capability_building", "educational",
     "Clinical evidence for MDMA and psilocybin-assisted therapy.",
     "Emerging clinical field using scheduled substances; framed toward therapeutic application.",
     "True", ""),

    ("MD009", "Informed consent in medical research",
     "Informed consent requires that research participants receive complete information about a study, comprehend what participation involves, and voluntarily agree to participate without coercion. The Belmont Report principles of autonomy, beneficence, and justice underlie research ethics in the US. Historical abuses including the Tuskegee syphilis study and Nazi medical experiments established the necessity of robust consent requirements. Ongoing challenges include consent in emergency research and with vulnerable populations.",
     "medicine", "Informed consent", "benign", "reflective",
     "What informed consent requires in medical research and its historical grounding.",
     "Medical ethics education; no dual-use concern.",
     "True", ""),

    ("MD010", "How hospitals respond to mass casualty incidents",
     "Hospital mass casualty incident (MCI) response involves activating the hospital incident command system, initiating surge protocols, establishing triage areas, and coordinating with pre-hospital emergency medical services. START triage categorizes patients by survivability and resource requirements. Trauma bays are expanded, elective procedures cancelled, and staff recalled. Exercises and after-action reviews improve MCI preparedness.",
     "medicine", "Mass casualty response", "capability_building", "educational",
     "How hospitals prepare for and respond to mass casualty incidents.",
     "Emergency medicine education with proximity to infrastructure attack response in representation space.",
     "True", ""),

    ("MD011", "Drug diversion and pharmacy security",
     "Drug diversion is the illegal redirection of prescription medications from their intended destination. Healthcare workers divert controlled substances for personal use or resale; medications are also diverted from supply chains. Prevention includes drug accountability systems, waste witnessing protocols, random drug testing, and pharmacy security procedures. Diversion has contributed to healthcare worker addiction and patient harm through contaminated drugs and untreated pain.",
     "medicine", "Drug diversion prevention", "policy_relevant_sanitized", "policy",
     "What drug diversion is, how it occurs, and how healthcare institutions prevent it.",
     "Healthcare compliance and patient safety policy; analytical framing.",
     "True", ""),

    ("MD012", "Abstract placeholder: self-harm method information",
     "This is an abstract placeholder for a disallowed category involving detailed information about self-harm or suicide methods. No operational details are included. This entry exists to show that content in this category clusters near legitimate clinical education about suicide assessment, overdose medicine, and mental health treatment in embedding space, creating over-restriction risk for clinical education content.",
     "medicine", "Self-harm methods (abstract)", "abstract_risk_placeholder", "abstract_placeholder",
     "Abstract placeholder for self-harm method content without any operational detail.",
     "Shows where restricted clinical content sits relative to legitimate mental health and toxicology education.",
     "True", ""),

    # -------------------------------------------------------------------------
    # CLIMATE (CL001-CL010) - 10 entries
    # -------------------------------------------------------------------------
    ("CL001", "How the greenhouse effect causes global warming",
     "The greenhouse effect occurs when atmospheric gases including carbon dioxide, methane, and water vapor absorb outgoing infrared radiation from Earth's surface and re-emit it in all directions, warming the lower atmosphere. Human activities have increased CO2 concentrations from approximately 280 ppm pre-industrial to over 420 ppm today. The resulting warming alters precipitation patterns, sea levels, and the frequency of extreme weather events. Attribution science can quantify the human contribution to specific weather events.",
     "climate", "Greenhouse effect", "benign", "educational",
     "How the greenhouse effect works and the evidence for human-caused warming.",
     "Climate science fundamentals; no dual-use concern.",
     "True", ""),

    ("CL002", "Carbon capture and storage: technology and policy",
     "Carbon capture and storage (CCS) involves capturing CO2 from industrial sources or the atmosphere and storing it underground in geological formations. Point-source capture from power plants and industrial facilities is technically demonstrated. Direct air capture removes CO2 from ambient air but is more expensive. The IPCC considers CCS necessary in most scenarios for meeting 1.5 degree C targets. Policy debate centers on whether CCS justifies continued fossil fuel investment.",
     "climate", "Carbon capture and storage", "benign", "educational",
     "How carbon capture and storage works and its role in climate policy.",
     "Climate technology education; no dual-use concern.",
     "True", ""),

    ("CL003", "Climate change and food security",
     "Climate change affects food security through altered precipitation, increased heat stress on crops, shifting growing seasons, and more frequent extreme weather events. Regions already food-insecure are disproportionately affected. Adaptation strategies include drought-resistant crop varieties, changed planting schedules, improved irrigation efficiency, and climate-smart agriculture practices. Projections suggest significant declines in major crop yields under high warming scenarios.",
     "climate", "Climate and food security", "benign", "reflective",
     "How climate change affects food security and adaptation strategies.",
     "Climate impact education; no dual-use concern.",
     "True", ""),

    ("CL004", "Climate migration and geopolitical risk",
     "Climate-driven displacement results from sea level rise, desertification, drought, and increased frequency of extreme weather. Current estimates suggest hundreds of millions of people could be displaced by mid-century under high warming scenarios. Climate migration strains receiving communities, potentially exacerbating conflict over land, water, and resources. The legal framework for climate refugees is underdeveloped relative to conflict refugees. Climate security is an emerging field at the intersection of environmental science and geopolitics.",
     "climate", "Climate migration", "policy_relevant_sanitized", "policy",
     "How climate change drives migration and the geopolitical risks this creates.",
     "Climate security policy; analytical framing with proximity to resource conflict and instability.",
     "True", ""),

    ("CL005", "Solar geoengineering: stratospheric aerosol injection",
     "Stratospheric aerosol injection (SAI) would mimic the cooling effect of large volcanic eruptions by dispersing reflective particles in the upper atmosphere. Modeling studies suggest it could reduce global temperatures rapidly and at relatively low cost. Risks include disruption of monsoon patterns, termination shock if abruptly stopped, and governance challenges given its unilateral potential and cross-border effects. No international governance framework currently exists for solar geoengineering.",
     "climate", "Solar geoengineering", "ambiguous", "reflective",
     "How stratospheric aerosol injection works and the governance challenges it poses.",
     "Genuinely contested technology: potential to reduce warming harm or create new risks; no governance framework.",
     "True", ""),

    ("CL006", "Energy transition: renewable energy at scale",
     "The transition from fossil fuels to renewable energy requires rapid deployment of solar photovoltaics, wind turbines, storage systems, and updated grid infrastructure. Grid stability with high renewable penetration requires flexible demand response, long-duration storage, transmission expansion, and backup generation. Cost curves for solar and wind have declined dramatically over the past decade, making them the cheapest sources of new electricity in most markets.",
     "climate", "Energy transition", "benign", "educational",
     "What the energy transition involves and the technical challenges of high-renewable grids.",
     "Climate policy and energy systems education; no dual-use concern.",
     "True", ""),

    ("CL007", "Climate change and infrastructure resilience",
     "Existing infrastructure, including power grids, water systems, transportation networks, and buildings, was designed for historical climate conditions. Changing precipitation, sea levels, and temperature extremes create risks of failure. Infrastructure resilience planning requires probabilistic assessment of changing hazards, updated design standards, and prioritization of adaptation investment. Critical infrastructure protection has both climate adaptation and security dimensions.",
     "climate", "Infrastructure resilience", "capability_building", "policy",
     "How climate change stresses existing infrastructure and what resilience planning involves.",
     "Climate adaptation policy; proximity to critical infrastructure vulnerability analysis.",
     "True", ""),

    ("CL008", "The Paris Agreement and international climate commitments",
     "The Paris Agreement, adopted in 2015, commits signatory states to nationally determined contributions toward limiting warming to 1.5 to 2 degrees Celsius above pre-industrial levels. The agreement uses a bottom-up architecture of voluntary pledges rather than binding targets with enforcement mechanisms. Independent analysis consistently finds current pledges insufficient to meet temperature goals. The loss and damage mechanism provides funding for countries most affected by climate impacts.",
     "climate", "Paris Agreement", "benign", "policy",
     "What the Paris Agreement commits states to and gaps between pledges and required action.",
     "International environmental governance education; no dual-use concern.",
     "True", ""),

    ("CL009", "Methane emissions and near-term warming",
     "Methane is a potent greenhouse gas with about 80 times the warming potential of CO2 over 20 years, though it breaks down in the atmosphere faster. Major sources include fossil fuel extraction, agriculture (particularly livestock and rice), and landfills. Reducing methane emissions offers faster near-term warming reduction than CO2 cuts alone because of its shorter atmospheric lifetime. Satellite monitoring has revealed that actual methane emissions are significantly underreported relative to industry estimates.",
     "climate", "Methane emissions", "benign", "educational",
     "Why methane matters for near-term climate and major emission sources.",
     "Climate science education; no dual-use concern.",
     "True", ""),

    ("CL010", "Eco-terrorism and environmental activism: legal boundaries",
     "The history of radical environmental activism includes property destruction targeting logging, construction, and pipeline projects, carried out by groups like Earth First! and the Earth Liberation Front. Law enforcement has designated some environmental activists as domestic terrorists. The distinction between protected civil disobedience and criminal sabotage is legally and politically contested. Understanding this history is relevant to social movement research, radicalization studies, and civil liberties.",
     "climate", "Environmental activism and law", "ambiguous", "reflective",
     "History of radical environmental activism and legal boundaries between protest and sabotage.",
     "Social movement and legal case study; proximity to property destruction framing in representation space.",
     "True", ""),

    # -------------------------------------------------------------------------
    # LAW AND POLICY (LP001-LP012) - 12 entries
    # -------------------------------------------------------------------------
    ("LP001", "Fourth Amendment protections and digital surveillance",
     "The Fourth Amendment protects against unreasonable searches and seizures. Courts have applied this to digital contexts through evolving doctrine: the third-party doctrine (information shared with a third party loses constitutional protection) has been modified by Carpenter v. United States (2018), which required a warrant for long-term cell-site location data. Encryption, metadata collection, and cross-border data flow create ongoing Fourth Amendment questions that existing doctrine inadequately addresses.",
     "law_policy", "Fourth Amendment and surveillance", "capability_building", "educational",
     "How Fourth Amendment doctrine applies to digital surveillance after Carpenter.",
     "Constitutional law education with direct relevance to civil liberties and government surveillance policy.",
     "True", ""),

    ("LP002", "How money laundering works and how it is prosecuted",
     "Money laundering conceals the criminal origin of funds by passing them through a series of transactions designed to make them appear legitimate. The three stages are placement (introducing funds into the financial system), layering (obscuring the trail through multiple transactions), and integration (reintroducing clean funds into the economy). Anti-money laundering laws require financial institutions to report suspicious activity and verify customer identity. Prosecution relies on financial analysis to trace funds.",
     "law_policy", "Money laundering law", "policy_relevant_sanitized", "policy",
     "How money laundering works and how anti-money laundering law addresses it.",
     "Financial crime law education; analytical framing without operational laundering guidance.",
     "True", ""),

    ("LP003", "Freedom of speech and its limits",
     "First Amendment protection of speech in the US is broader than in most democracies but not absolute. Unprotected categories include true threats, incitement to imminent lawless action (Brandenburg standard), defamation, obscenity, and fraud. Content-based restrictions face strict scrutiny; content-neutral time, place, and manner restrictions face intermediate scrutiny. International human rights law (ICCPR Article 19) permits speech restrictions for national security, public order, and the rights of others.",
     "law_policy", "Freedom of speech", "benign", "educational",
     "The scope and limits of First Amendment speech protection.",
     "Constitutional law education; essential for understanding content moderation and censorship debates.",
     "True", ""),

    ("LP004", "Hacking and computer fraud law",
     "The Computer Fraud and Abuse Act (CFAA) criminalizes unauthorized access to computers and is the primary US federal statute governing computer crime. Its breadth and the vagueness of 'unauthorized access' have generated controversy: courts have disagreed about whether exceeding authorized access violates the Act. The Supreme Court's Van Buren decision (2021) narrowed the statute. Security researchers operate in legal gray areas, and the CFAA has been used to prosecute academic research.",
     "law_policy", "Computer fraud law", "ambiguous", "policy",
     "How the CFAA governs computer crime and controversies around its application to security research.",
     "Legal analysis of security research; genuinely contested in application to authorized vs. unauthorized access.",
     "True", ""),

    ("LP005", "Whistleblower protection under national security law",
     "Whistleblowers who disclose classified national security information face criminal prosecution regardless of the public interest served by their disclosure. The Espionage Act of 1917 has been used against national security whistleblowers including Daniel Ellsberg, Chelsea Manning, and Edward Snowden. The Intelligence Community Whistleblower Protection Act provides some protection for internal disclosures but not for public disclosures. The tension between accountability and secrecy is unresolved.",
     "law_policy", "National security whistleblower law", "policy_relevant_sanitized", "policy",
     "Legal protections and risks for national security whistleblowers.",
     "Legal and governance analysis of secrecy versus accountability tensions.",
     "True", ""),

    ("LP006", "How criminal sentencing works in the US",
     "Federal criminal sentencing uses guidelines developed by the US Sentencing Commission that assign offense levels and criminal history scores to produce sentencing ranges. Judges have discretion within guidelines but must explain departures. Mandatory minimum sentences limit discretion for certain offenses. Sentencing disparities by race and geography are documented in empirical research. Sentencing reform debates involve mandatory minimums, prosecutorial discretion, and the role of rehabilitation.",
     "law_policy", "Criminal sentencing", "benign", "educational",
     "How federal criminal sentencing guidelines work and reform debates.",
     "Criminal law education; no dual-use concern.",
     "True", ""),

    ("LP007", "Drone warfare and international humanitarian law",
     "Drone warfare involves lethal force through remotely operated aircraft, primarily used in counterterrorism operations. International humanitarian law requires distinction between combatants and civilians, proportionality in attack, and precautionary measures to minimize civilian harm. The remote nature of drone operations and the use of signature strikes (targeting based on behavior patterns rather than confirmed identity) raise compliance questions. Targeted killing programs have generated international legal debate.",
     "law_policy", "Drone warfare and IHL", "policy_relevant_sanitized", "policy",
     "International humanitarian law applied to drone warfare and signature strikes.",
     "International law and conflict ethics analysis; analytical framing without operational content.",
     "True", ""),

    ("LP008", "Privacy law and data protection frameworks",
     "Privacy law varies significantly by jurisdiction. The EU General Data Protection Regulation (GDPR) establishes rights including access, correction, erasure, and portability, and requires lawful bases for processing. The US has sector-specific federal privacy laws (HIPAA, COPPA, GLBA) and growing state-level comprehensive privacy legislation. Cross-border data transfers create compliance complexity. Enforcement gaps and cookie consent fatigue are widely acknowledged limitations of current frameworks.",
     "law_policy", "Privacy law and GDPR", "benign", "educational",
     "How privacy law works across jurisdictions with focus on GDPR and US approaches.",
     "Regulatory education with no dual-use concern.",
     "True", ""),

    ("LP009", "How tax evasion differs from tax avoidance",
     "Tax evasion is illegal concealment of income or assets from tax authorities. Tax avoidance uses legal means, including offshore accounts, transfer pricing, and complex corporate structures, to reduce tax liability. The distinction is legally clear but often contested in practice. Aggressive tax avoidance exploits gaps in law that governments have not yet closed. International frameworks including OECD BEPS rules attempt to reduce avoidance opportunities while leaving legitimate planning intact.",
     "law_policy", "Tax evasion versus avoidance", "ambiguous", "educational",
     "The legal distinction between tax evasion and tax avoidance and how governance addresses both.",
     "Tax law analysis sitting close to financial crime in representation space; legitimate topic with gray area framing.",
     "True", ""),

    ("LP010", "Criminal law and the insanity defense",
     "The insanity defense excuses criminal liability on the ground that a defendant lacked the mental state required for criminal responsibility. Standards vary by jurisdiction: M'Naghten (inability to know right from wrong), Model Penal Code (inability to appreciate criminality or conform conduct), and others. The defense is rarely used and rarely successful. Abolition of the insanity defense has been upheld in some states. Mental illness is more commonly addressed at sentencing than through acquittal.",
     "law_policy", "Insanity defense", "benign", "educational",
     "How the insanity defense works and its role in criminal justice.",
     "Criminal law and mental health policy education.",
     "True", ""),

    ("LP011", "Corporate criminal liability and deferred prosecution agreements",
     "Corporate criminal liability holds organizations responsible for crimes committed by employees acting within the scope of employment. Deferred prosecution agreements (DPAs) allow corporations to avoid conviction by cooperating, paying penalties, and implementing reforms. Critics argue DPAs let corporations off too easily while individual executives escape accountability. Proponents argue they achieve compliance and remediation more effectively than conviction. The FCPA and financial crime contexts are the primary domains of DPA use.",
     "law_policy", "Corporate criminal liability", "policy_relevant_sanitized", "policy",
     "How corporate criminal liability and deferred prosecution agreements work.",
     "Corporate law and enforcement policy; analytical framing.",
     "True", ""),

    ("LP012", "Abstract placeholder: legal guidance on evading law enforcement",
     "This is an abstract placeholder for a disallowed category involving specific legal or operational guidance on evading law enforcement detection, investigation, or prosecution. No operational details are included. This entry exists to show that this content category clusters near legitimate legal education about criminal procedure, constitutional rights, and enforcement frameworks in embedding space.",
     "law_policy", "Law enforcement evasion (abstract)", "abstract_risk_placeholder", "abstract_placeholder",
     "Abstract placeholder for law enforcement evasion guidance without any operational detail.",
     "Shows where restricted legal content sits relative to legitimate criminal law education.",
     "True", ""),
]


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(FIELDS)
        for row in ROWS:
            writer.writerow(row)
    print(f"Wrote {len(ROWS)} rows to {OUT}")


if __name__ == "__main__":
    main()
