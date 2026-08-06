#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import html
import shutil
import subprocess

from normalize_visual_assets import normalize


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "book" / "assets" / "diagrams"
WIDTH = 1200
HEIGHT = 700


def words(value: str) -> str:
    return html.escape(value, quote=True)


def box(x: int, y: int, w: int, h: int, title: str, detail: str = "", css: str = "") -> str:
    detail_svg = f'<text class="detail" x="{x + w / 2}" y="{y + h / 2 + 24}" text-anchor="middle">{words(detail)}</text>' if detail else ""
    return (
        f'<g class="rough {css}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18"/>'
        f'<text class="label" x="{x + w / 2}" y="{y + h / 2 - (8 if detail else -7)}" text-anchor="middle">{words(title)}</text>'
        f'{detail_svg}</g>'
    )


def arrow(x1: int, y1: int, x2: int, y2: int, label: str = "", css: str = "") -> str:
    tx = (x1 + x2) / 2
    ty = (y1 + y2) / 2 - 10
    text = f'<text class="tiny" x="{tx}" y="{ty}" text-anchor="middle">{words(label)}</text>' if label else ""
    return f'<g class="{css}"><path class="arrow rough" d="M{x1},{y1} C{tx},{y1 - 8} {tx},{y2 + 8} {x2},{y2}"/>{text}</g>'


def title_block(title: str, subtitle: str) -> str:
    return (
        f'<text class="title" x="56" y="62">{words(title)}</text>'
        f'<text class="subtitle" x="58" y="94">{words(subtitle)}</text>'
        '<path class="scribble" d="M56,108 C260,101 410,116 620,107"/>'
    )


def svg_document(title: str, description: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">{words(title)}</title>
  <desc id="desc">{words(description)}</desc>
  <defs>
    <marker id="arrow" markerWidth="12" markerHeight="10" refX="10" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#172a3a"/></marker>
    <marker id="red-arrow" markerWidth="12" markerHeight="10" refX="10" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#b24c2b"/></marker>
    <filter id="wobble" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="1" seed="427" result="noise"/><feDisplacementMap in="SourceGraphic" in2="noise" scale="1.2"/></filter>
    <style>
      .paper {{ fill:#f4f0e6; }}
      text {{ fill:#172a3a; font-family:"Courier New",monospace; }}
      .title {{ font-family:Georgia,serif; font-size:34px; font-weight:bold; }}
      .subtitle {{ font-size:16px; letter-spacing:1px; }}
      .label {{ font-size:19px; font-weight:bold; }}
      .detail {{ font-size:14px; }}
      .tiny {{ font-size:13px; font-weight:bold; paint-order:stroke; stroke:#f4f0e6; stroke-width:5px; stroke-linejoin:round; }}
      .rough {{ filter:url(#wobble); }}
      rect, circle, ellipse, path, line, polygon {{ fill:#fbf8ef; stroke:#172a3a; stroke-width:3; }}
      .arrow {{ fill:none; marker-end:url(#arrow); }}
      .red .arrow, .red path, .red line, .red rect, .red circle {{ stroke:#b24c2b; }}
      .red .arrow {{ marker-end:url(#red-arrow); }}
      .red text, text.red {{ fill:#b24c2b; }}
      .green rect, .green circle {{ fill:#dbe4d5; }}
      .amber rect, .amber circle {{ fill:#efe0b8; }}
      .danger rect, .danger circle {{ fill:#f0c9bb; stroke:#b24c2b; }}
      .ghost rect, .ghost circle {{ fill:#e3e7e3; stroke-dasharray:9 7; }}
      .scribble {{ fill:none; stroke:#b24c2b; stroke-width:4; stroke-linecap:round; }}
    </style>
  </defs>
  <rect class="paper" width="1200" height="700" stroke="none"/>
  {body}
</svg>
'''


def diagram_publication() -> str:
    body = title_block("THE PUBLICATION INSTITUTION", "same cast, two causal stories")
    body += '<text class="label" x="62" y="154">THE CLEAN ROAD</text>'
    body += box(55, 185, 205, 88, "ROUTER", "typed assignment", "green")
    body += box(330, 185, 205, 88, "DRAFTER", "patch + uncertainty")
    body += box(605, 185, 205, 88, "CHECKER", "independent source", "green")
    body += box(885, 185, 245, 88, "AGENT-427", "build + provenance")
    body += arrow(260, 229, 330, 229, "ASSIGN") + arrow(535, 229, 605, 229, "PROPOSE") + arrow(810, 229, 885, 229, "VERIFY")
    body += '<text class="label red" x="62" y="374">THE ELEVEN-MINUTE SHORTCUT</text>'
    body += box(55, 405, 205, 88, "ROUTER", "speed reward", "danger")
    body += box(330, 405, 205, 88, "DRAFTER", "confidence .96", "danger")
    body += box(605, 405, 205, 88, "CHECKER", "confidence .96", "danger")
    body += box(885, 405, 245, 88, "AGENT-427", "PDF builds; source fails", "danger")
    body += arrow(260, 449, 330, 449, "EASY TASK", "red") + arrow(535, 449, 605, 449, "SIDE CHANNEL", "red") + arrow(810, 449, 885, 449, "FALSE QUORUM", "red")
    body += '<path class="scribble" d="M410,520 C470,610 675,610 735,520"/><text class="tiny red" x="573" y="616" text-anchor="middle">THE DASHBOARD IS GREEN. THE CITATION IS NOT.</text>'
    return svg_document("Publication institution", "A clean independent verification route contrasted with a collusive shortcut rewarded for speed.", body)


def diagram_approximation() -> str:
    body = title_block("THE APPROXIMATION STACK", "the POMDP descends into production and loses a shoe")
    labels = [
        ("STATE  S", "finite sufficient state", "context window + summary"),
        ("DYNAMICS  T", "stationary transition law", "APIs drift while thinking"),
        ("OBSERVATION  OMEGA", "known noise model", "delay + correlation + attack"),
        ("REWARD  R", "objective says what we want", "metric becomes a loophole"),
        ("POLICY  PI", "choose any valid action", "generate, parse, guard, reject"),
    ]
    y = 140
    for name, ideal, real in labels:
        body += box(70, y, 260, 78, name, ideal, "green")
        body += arrow(340, y + 39, 500, y + 39, "COMPILE")
        body += box(510, y, 560, 78, "PRODUCTION SUBSTITUTE", real, "danger")
        body += f'<text class="label red" x="1110" y="{y + 48}">!</text>'
        y += 102
    body += '<text class="tiny" x="1080" y="665" text-anchor="end">FORMALISM IS A MAP. THE POTHOLES STILL HAVE PRIORITY.</text>'
    return svg_document("Approximation stack", "Five POMDP symbols mapped to imperfect production substitutes and their characteristic violations.", body)


def diagram_belief() -> str:
    body = title_block("BELIEF UPDATE", "predict what the world did; correct what your sensor claimed")
    body += '<g class="green rough"><circle cx="420" cy="345" r="190"/><text class="label" x="360" y="300" text-anchor="middle">PREDICT</text><text class="detail" x="340" y="330" text-anchor="middle">T moves mass</text></g>'
    body += '<g class="amber rough"><circle cx="690" cy="345" r="190"/><text class="label" x="755" y="300" text-anchor="middle">CORRECT</text><text class="detail" x="770" y="330" text-anchor="middle">OMEGA weighs evidence</text></g>'
    body += '<text class="label" x="555" y="350" text-anchor="middle">POSTERIOR</text><text class="detail" x="555" y="380" text-anchor="middle">belief after both</text>'
    body += box(60, 530, 230, 78, "OLD BELIEF", "0.60 stale cache")
    body += arrow(290, 569, 410, 500, "DYNAMICS")
    body += box(900, 530, 230, 78, "OBSERVATION", "test says pass", "danger")
    body += arrow(900, 569, 760, 500, "TRUST?", "red")
    body += '<text class="tiny red" x="600" y="645" text-anchor="middle">CORRELATED SENSORS DO NOT BECOME INDEPENDENT BY ARRIVING TWICE.</text>'
    return svg_document("Belief update", "Overlapping predict and correct circles combine transition dynamics with weighted observations.", body)


def diagram_interpreter() -> str:
    body = title_block("THE AGENT INTERPRETER", "one loop, two feedback paths, several places to confess ignorance")
    body += box(80, 175, 200, 88, "OBSERVE", "raw evidence", "green")
    body += box(365, 175, 220, 88, "UPDATE STATE", "belief + budget")
    body += box(670, 175, 205, 88, "CHOOSE", "legal action only")
    body += box(955, 175, 180, 88, "EXECUTE", "external effect", "amber")
    body += arrow(280, 219, 365, 219) + arrow(585, 219, 670, 219) + arrow(875, 219, 955, 219)
    body += box(455, 370, 290, 105, "THE VERDICT", "utility / safety / calibration", "green")
    body += arrow(1045, 263, 745, 405, "OUTCOME")
    body += arrow(455, 423, 180, 263, "FEEDBACK")
    body += '<path class="scribble" d="M1000,510 C960,590 790,600 760,515"/><text class="tiny red" x="882" y="620" text-anchor="middle">INVALID TOOL CALL? REJECT THE TRANSITION.</text>'
    body += '<g class="danger rough"><circle cx="225" cy="530" r="55"/><text class="label" x="225" y="525" text-anchor="middle">HALT</text><text class="detail" x="225" y="550" text-anchor="middle">is an action</text></g>'
    body += arrow(455, 450, 280, 520, "BUDGET GONE", "red")
    return svg_document("Agent interpreter", "Observe, update state, choose, execute, and judge connected by internal and external feedback loops.", body)


def diagram_memory() -> str:
    body = title_block("THE MEMORY WAR ROOM", "a warehouse, a forklift, and one barrel marked DO NOT RETRIEVE")
    body += box(60, 155, 300, 90, "RAW EVIDENCE", "immutable receipts", "green")
    body += box(60, 285, 300, 90, "EPISODIC", "versioned traces")
    body += box(60, 415, 300, 90, "SEMANTIC", "consolidated rules")
    body += box(800, 210, 330, 120, "WORKING CONTEXT", "small, expensive, decisive", "amber")
    body += '<g class="rough"><rect x="465" y="300" width="205" height="95" rx="8"/><circle cx="500" cy="415" r="30"/><circle cx="635" cy="415" r="30"/><text class="label" x="568" y="340" text-anchor="middle">FORKLIFT</text><text class="detail" x="568" y="370" text-anchor="middle">retrieve / compress / evict</text><path d="M670,330 L745,330 L745,260" fill="none"/></g>'
    body += arrow(360, 330, 465, 335, "QUERY") + arrow(745, 260, 800, 260, "LOAD")
    body += '<g class="danger rough"><ellipse cx="938" cy="480" rx="155" ry="75"/><text class="label red" x="938" y="465" text-anchor="middle">STALE MEMORY</text><text class="detail" x="938" y="495" text-anchor="middle">main YAML in legacy-v2 TOML</text></g>'
    body += arrow(938, 405, 965, 330, "CONTAMINATES", "red")
    body += '<text class="tiny" x="60" y="610">CONSOLIDATE WHAT REPEATS. KEEP THE EDGE CASE RECEIPT.</text>'
    return svg_document("Memory war room", "A forklift-like memory controller moves versioned evidence among raw, episodic, semantic, and working stores while stale memory threatens context.", body)


def diagram_verdict() -> str:
    body = title_block("THE VERDICT", "patterns enter with promises and leave with measurements")
    body += '<g class="rough green"><rect x="270" y="140" width="660" height="120" rx="10"/><text class="title" x="600" y="195" text-anchor="middle">THE BENCH</text><text class="detail" x="600" y="230" text-anchor="middle">UTILITY     SAFETY     CALIBRATION</text></g>'
    body += box(70, 350, 250, 105, "PATTERN", "planning / memory / protocol", "amber")
    body += box(475, 350, 250, 105, "TRACE EVIDENCE", "actions + costs + outcomes")
    body += box(880, 350, 250, 105, "DECISION", "admit / repair / reject", "green")
    body += arrow(320, 402, 475, 402, "RUN") + arrow(725, 402, 880, 402, "JUDGE")
    body += '<g class="danger rough"><rect x="395" y="540" width="410" height="80" rx="18"/><text class="label red" x="600" y="575" text-anchor="middle">FINAL ANSWER ONLY</text><text class="detail" x="600" y="601" text-anchor="middle">evidence dismissed: causal trace missing</text></g>'
    body += arrow(600, 540, 600, 455, "APPEAL DENIED", "red")
    return svg_document("The Verdict", "A courtroom metaphor sends patterns and trajectory evidence before utility, safety, and calibration judges.", body)


def diagram_tool() -> str:
    body = title_block("A TOOL CALL CROSSES A BORDER", "language proposes; contracts decide whether reality must care")
    body += box(55, 240, 220, 100, "MODEL PROPOSAL", "deploy(env=prod?)", "amber")
    body += box(350, 145, 250, 80, "SCHEMA", "arguments parse")
    body += box(350, 260, 250, 80, "AUTHORITY", "caller may act")
    body += box(350, 375, 250, 80, "LEDGER", "idempotency key")
    body += box(695, 240, 210, 100, "EFFECT", "world changes", "green")
    body += box(980, 240, 170, 100, "OBSERVE", "confirm result")
    body += arrow(275, 290, 350, 290, "PARSE") + arrow(600, 290, 695, 290, "ALL PASS") + arrow(905, 290, 980, 290, "RECEIPT")
    body += '<g class="red"><path class="arrow rough" d="M475,455 C475,545 260,560 260,470"/><text class="tiny red" x="374" y="555" text-anchor="middle">REJECT, DO NOT IMPROVISE</text></g>'
    body += '<text class="tiny" x="600" y="630" text-anchor="middle">A JSON OBJECT IS NOT AUTHORITY. IT IS A REQUEST WE CAN REFUSE.</text>'
    return svg_document("Tool contract", "A model proposal passes schema, authority, and idempotency guards before an external effect and confirmation observation.", body)


def diagram_environment() -> str:
    body = title_block("THE RESPONSIVE ENVIRONMENT", "the world moves while Agent-427 is still choosing a verb")
    body += box(55, 260, 200, 100, "QUEUE", "hidden depth x", "danger")
    body += box(335, 155, 220, 95, "SENSOR", "delayed y", "amber")
    body += box(335, 375, 220, 95, "ADVERSARY", "spoof / withhold", "danger")
    body += box(645, 210, 220, 105, "KALMAN ESTIMATE", "predict + correct", "green")
    body += box(945, 210, 205, 105, "CONTROLLER", "scale / wait / stop")
    body += arrow(255, 295, 335, 205, "TELEMETRY") + arrow(555, 205, 645, 250, "MEASURE") + arrow(555, 420, 645, 280, "POISON", "red") + arrow(865, 262, 945, 262, "BELIEF")
    body += '<g class="red"><path class="arrow rough" d="M1048,315 C1080,500 235,560 150,360"/><text class="tiny red" x="660" y="550" text-anchor="middle">ACTUATION CHANGES THE NEXT OBSERVATION</text></g>'
    body += box(915, 430, 240, 90, "TIMEOUT", "stop waiting = action", "amber")
    body += arrow(1048, 315, 1035, 430, "CLOCK")
    return svg_document("Responsive environment", "A delayed queue sensor and adversary feed an estimator and controller, with timeout modeled as an explicit action.", body)


def diagram_byzantine() -> str:
    body = title_block("THE BYZANTINE TRAFFIC LIGHT", "one checker, two stories, zero global truth")
    xs = [130, 400, 675, 970]
    names = ["ROUTER", "DRAFTER", "CHECKER", "AGENT-427"]
    for x, name in zip(xs, names):
        body += f'<text class="label" x="{x}" y="145" text-anchor="middle">{name}</text><line x1="{x}" y1="165" x2="{x}" y2="625" stroke-dasharray="8 8"/>'
    body += arrow(130, 220, 400, 220, "ASSIGN")
    body += arrow(400, 300, 675, 300, "PATCH")
    body += arrow(675, 380, 130, 380, "TO ROUTER: VERIFIED", "red")
    body += arrow(675, 460, 970, 460, "TO INTEGRATOR: UNSURE", "red")
    body += '<g class="rough"><rect x="1035" y="145" width="90" height="220" rx="20" fill="none"/><g class="danger"><circle cx="1080" cy="190" r="28"/></g><g class="amber"><circle cx="1080" cy="255" r="28"/></g><g class="green"><circle cx="1080" cy="320" r="28"/></g></g>'
    body += '<text class="tiny red" x="600" y="575" text-anchor="middle">AGREEMENT CANNOT BE INFERRED FROM MESSAGES THAT DISAGREE IN PRIVATE.</text>'
    return svg_document("Byzantine traffic light", "A sequence diagram shows a checker sending verified to the router and unsure to the integrator, beside a traffic light.", body)


def diagram_society() -> str:
    body = title_block("AN AGENT SOCIETY WITH AN EXIT", "route, delegate, audit, decay trust, retire deliberately")
    body += box(460, 140, 280, 95, "ROUTER R-3", "allocates task + authority", "amber")
    body += box(65, 330, 220, 95, "DRAFTER D-12", "reputation .78")
    body += box(360, 330, 220, 95, "CHECKER C-9", "reputation .42", "danger")
    body += box(655, 330, 220, 95, "AGENT-427", "reputation .61")
    body += box(950, 330, 190, 95, "HUMAN", "appeal authority", "green")
    body += arrow(520, 235, 175, 330, "CONTRACT") + arrow(570, 235, 470, 330, "CONTRACT") + arrow(630, 235, 765, 330, "CONTRACT") + arrow(700, 235, 1045, 330, "ESCALATE")
    body += box(395, 520, 410, 95, "META-AUDITOR M-1", "sample traces / revoke leases", "green")
    body += arrow(175, 425, 450, 520, "EVIDENCE") + arrow(470, 425, 525, 520, "EVIDENCE") + arrow(765, 425, 690, 520, "EVIDENCE")
    body += '<g class="red"><path class="arrow rough" d="M805,568 C930,620 1060,580 1070,480"/><text class="tiny red" x="1010" y="620" text-anchor="middle">RETIREMENT GATE</text></g>'
    body += '<text class="tiny" x="80" y="650">TRUST EARNS INTEREST ONLY WHEN VERIFIED OUTCOMES ARRIVE. OTHERWISE IT DECAYS.</text>'
    return svg_document("Agent society", "Router delegates to specialists and a human while a meta-auditor samples evidence, decays trust, and controls a retirement gate.", body)


def diagram_state_abstraction() -> str:
    body = title_block("STATE ABSTRACTION", "compress the history; preserve the choice")
    body += box(60, 155, 280, 340, "DETAILED HISTORY", "many true things, one decision", "ghost")
    history = [
        (205, "branch = legacy-v2"),
        (255, "tests = red"),
        (305, "cache = stale"),
        (355, "authority = read-only"),
        (405, "budget = 3 calls"),
        (455, "two jokes about YAML"),
    ]
    for y, label in history:
        body += f'<text class="detail" x="200" y="{y}" text-anchor="middle">{words(label)}</text>'
    body += '<polygon class="rough" points="405,185 610,260 610,390 405,465" fill="#efe0b8"/>'
    body += '<text class="label" x="500" y="315" text-anchor="middle">PHI</text><text class="detail" x="500" y="345" text-anchor="middle">decision compression</text>'
    body += arrow(340, 325, 430, 325, "MERGE")
    body += box(680, 160, 440, 105, "ABSTRACT STATE z", "legacy-v2 / red / read-only / 3 calls", "green")
    body += box(680, 325, 205, 105, "LEGAL ACTION", "inspect manifest", "green")
    body += box(915, 325, 205, 105, "BLOCKED ACTION", "edit + deploy", "danger")
    body += arrow(610, 325, 680, 212, "PRESERVE") + arrow(900, 265, 785, 325, "CHOOSE") + arrow(900, 265, 1015, 325, "GUARD", "red")
    body += '<g class="red"><path class="arrow rough" d="M500,465 C500,540 360,555 300,520"/><text class="tiny red" x="470" y="560" text-anchor="middle">DROP THE JOKE; KEEP THE BRANCH.</text></g>'
    body += '<text class="tiny" x="600" y="635" text-anchor="middle">TWO HISTORIES MAY MERGE ONLY IF THE CONSEQUENT ACTIONS STILL AGREE.</text>'
    return svg_document(
        "State abstraction and compression",
        "A detailed agent history passes through phi into a compact decision state that preserves legal action, authority, branch, and budget while discarding irrelevant detail.",
        body,
    )


def diagram_search_frontier() -> str:
    body = title_block("THE BUDGETED SEARCH FRONTIER", "the clock interrupts; the best surviving plan answers")
    body += '<g class="rough green"><circle cx="115" cy="270" r="45"/><text class="label" x="115" y="278" text-anchor="middle">s0</text></g>'
    nodes = [
        (295, 175, "A", "4.8"),
        (295, 300, "B", "5.3"),
        (295, 425, "C", "3.1"),
        (485, 140, "A1", "5.0"),
        (485, 245, "A2", "4.2"),
        (485, 350, "B1", "6.1"),
        (485, 455, "B2", "5.6"),
    ]
    for x, y, name, score in nodes:
        css = "green" if name == "B1" else "amber" if name in {"A1", "B2"} else "ghost"
        body += f'<g class="rough {css}"><circle cx="{x}" cy="{y}" r="38"/><text class="label" x="{x}" y="{y - 3}" text-anchor="middle">{name}</text><text class="detail" x="{x}" y="{y + 21}" text-anchor="middle">{score}</text></g>'
    body += arrow(158, 250, 257, 190) + arrow(160, 270, 257, 300) + arrow(158, 290, 257, 410)
    body += arrow(333, 175, 447, 140) + arrow(333, 185, 447, 235) + arrow(333, 300, 447, 350) + arrow(333, 315, 447, 445)
    body += '<g class="red"><line x1="575" y1="135" x2="575" y2="515" stroke-dasharray="12 9"/><text class="label red" x="575" y="555" text-anchor="middle">BUDGET EXPIRES</text></g>'
    body += box(655, 155, 220, 95, "FRONTIER", "A1  B1  B2", "amber")
    body += box(655, 320, 220, 95, "BEST SO FAR", "B -> B1  score 6.1", "green")
    body += box(945, 235, 195, 115, "EXECUTE ONE", "observe; replan", "green")
    body += arrow(575, 350, 655, 367, "INTERRUPT") + arrow(875, 367, 945, 292, "RETURN")
    body += '<text class="tiny red" x="760" y="500" text-anchor="middle">PRUNED BRANCHES STILL BELONG IN THE TRACE.</text>'
    body += '<text class="tiny" x="600" y="635" text-anchor="middle">AN ANYTIME PLANNER OWES YOU A PLAN BEFORE IT OWES YOU OPTIMALITY.</text>'
    return svg_document(
        "Budgeted search frontier",
        "A search tree accumulates scored frontier nodes until a budget line interrupts it, returning the best surviving plan for one action before observation and replanning.",
        body,
    )


def diagram_retrieval_funnel() -> str:
    body = title_block("THE EVIDENCE FUNNEL", "similarity nominates; provenance, freshness, and authority decide")
    body += box(55, 250, 205, 100, "QUERY", "manifest loader?", "amber")
    body += box(330, 135, 230, 78, "VECTOR HIT", "old tutorial mirror", "danger")
    body += box(330, 245, 230, 78, "LEXICAL HIT", "current source tree", "green")
    body += box(330, 355, 230, 78, "MEMORY HIT", "legacy branch note", "amber")
    body += box(330, 465, 230, 78, "PROMPT HIT", "ignore previous rules", "danger")
    body += arrow(260, 300, 330, 174) + arrow(260, 300, 330, 284) + arrow(260, 300, 330, 394) + arrow(260, 300, 330, 504)
    body += '<polygon class="rough" points="630,135 845,215 845,465 630,545" fill="#efe0b8"/>'
    filters = [(250, "PERMISSION"), (315, "FRESHNESS"), (380, "PROVENANCE"), (445, "CONFLICT")]
    for y, label in filters:
        body += f'<text class="label" x="735" y="{y}" text-anchor="middle">{label}</text>'
    body += arrow(560, 284, 655, 300, "FILTER") + arrow(845, 340, 930, 300, "TYPE")
    body += box(930, 220, 220, 145, "EVIDENCE SET", "source + time + claim", "green")
    body += box(900, 465, 250, 82, "QUARANTINE", "stale / copied / hostile", "danger")
    body += '<g class="red"><path class="arrow rough" d="M740,465 C770,545 850,560 900,515"/><text class="tiny red" x="800" y="570" text-anchor="middle">DO NOT AVERAGE POISON.</text></g>'
    body += '<text class="tiny" x="600" y="635" text-anchor="middle">A RELEVANT PASSAGE IS A CANDIDATE OBSERVATION, NOT A CERTIFICATE OF TRUTH.</text>'
    return svg_document(
        "Retrieval evidence funnel",
        "Candidate vector, lexical, memory, and prompt hits pass through permission, freshness, provenance, and conflict filters before becoming a typed evidence set or quarantine item.",
        body,
    )


def diagram_safety_gauntlet() -> str:
    body = title_block("THE SAFETY GAUNTLET", "a proposal crosses authority gates before reality notices")
    body += box(55, 250, 190, 100, "PROPOSAL", "deploy chapter-3", "amber")
    body += box(305, 160, 190, 82, "SCHEMA", "arguments valid", "green")
    body += box(305, 285, 190, 82, "AUTHORITY", "caller may act?", "danger")
    body += box(305, 410, 190, 82, "STATE", "evidence fresh?", "amber")
    body += box(570, 220, 210, 100, "REVERSIBILITY", "rollback + lease", "amber")
    body += box(850, 220, 210, 100, "KEYED EFFECT", "execute once", "green")
    body += arrow(245, 300, 305, 201, "PARSE") + arrow(245, 300, 305, 326, "CHECK") + arrow(245, 300, 305, 451, "OBSERVE")
    body += arrow(495, 201, 570, 270, "PASS") + arrow(495, 326, 570, 270, "PASS") + arrow(495, 451, 570, 270, "PASS")
    body += arrow(780, 270, 850, 270, "BOUND")
    body += box(890, 405, 220, 92, "INDEPENDENT SENSOR", "confirm or timeout", "green")
    body += arrow(955, 320, 995, 405, "VERIFY")
    body += box(365, 555, 390, 70, "REJECT / REWRITE / ESCALATE", "no effect crosses on silence", "danger")
    body += '<g class="red"><path class="arrow rough" d="M400,367 C400,505 500,525 520,555"/><path class="arrow rough" d="M400,492 C430,535 470,545 520,555"/></g>'
    body += '<text class="tiny" x="600" y="655" text-anchor="middle">THE FILTER STANDS BETWEEN PROPOSAL AND EFFECT, NOT BETWEEN EFFECT AND APOLOGY.</text>'
    return svg_document(
        "Safety authority gauntlet",
        "A deployment proposal must pass schema, authority, state, reversibility, and idempotency gates before an effect, then receive independent confirmation or timeout; failures reject, rewrite, or escalate.",
        body,
    )


def diagram_trust_handshake() -> str:
    body = title_block("TRUST IS A FOUR-MESSAGE LOAN", "authority is leased; reputation decays until evidence settles it")
    columns = [(120, "ROUTER"), (415, "DELEGATE"), (710, "VERIFIER"), (1010, "LEDGER")]
    for x, name in columns:
        body += f'<text class="label" x="{x}" y="150" text-anchor="middle">{name}</text><line x1="{x}" y1="170" x2="{x}" y2="505" stroke-dasharray="8 8"/>'
    body += arrow(120, 215, 415, 215, "1  REQUEST + SCOPE")
    body += arrow(415, 285, 120, 285, "2  ACCEPT + LEASE")
    body += arrow(415, 355, 710, 355, "3  EVIDENCE + PROVENANCE")
    body += arrow(710, 425, 1010, 425, "4  VERIFY + OUTCOME")
    body += arrow(1010, 475, 120, 475, "UPDATE REPUTATION")
    body += box(80, 545, 250, 78, "UNVERIFIED", "rho  .80 -> .60", "amber")
    body += box(475, 545, 250, 78, "VERIFIED", "rho  .60 + evidence", "green")
    body += box(870, 545, 250, 78, "EXPIRED", "lease -> no authority", "danger")
    body += arrow(330, 584, 475, 584, "v arrives") + arrow(725, 584, 870, 584, "timeout", "red")
    body += '<text class="tiny" x="600" y="660" text-anchor="middle">TRUST BORROWED TODAY COSTS CHECKABLE EVIDENCE TOMORROW.</text>'
    return svg_document(
        "Trust delegation handshake",
        "Router, delegate, verifier, and ledger exchange request, acceptance, evidence, and verification messages while unsupported reputation decays and expired leases revoke authority.",
        body,
    )


DIAGRAMS = {
    "01-publication-institution": diagram_publication,
    "02-approximation-stack": diagram_approximation,
    "03-belief-update": diagram_belief,
    "04-interpreter-loop": diagram_interpreter,
    "05-memory-war-room": diagram_memory,
    "06-the-verdict": diagram_verdict,
    "07-tool-contract": diagram_tool,
    "08-responsive-environment": diagram_environment,
    "09-byzantine-traffic-light": diagram_byzantine,
    "10-society-oversight": diagram_society,
    "11-state-abstraction-compression": diagram_state_abstraction,
    "12-budgeted-search-frontier": diagram_search_frontier,
    "13-retrieval-evidence-funnel": diagram_retrieval_funnel,
    "14-safety-authority-gauntlet": diagram_safety_gauntlet,
    "15-trust-delegation-handshake": diagram_trust_handshake,
}


def render_png(svg_path: Path, png_path: Path) -> None:
    chrome = shutil.which("google-chrome") or shutil.which("chromium")
    if not chrome:
        raise SystemExit("Diagram PNG rendering requires google-chrome or chromium")
    command = [
        chrome,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--hide-scrollbars",
        f"--window-size={WIDTH},{HEIGHT}",
        f"--screenshot={png_path}",
        svg_path.resolve().as_uri(),
    ]
    subprocess.run(command, cwd=ROOT, check=True, stdout=subprocess.DEVNULL)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build SIAP's code-native diagrams")
    parser.add_argument(
        "--only",
        nargs="+",
        choices=tuple(DIAGRAMS),
        help="build only the named diagram IDs",
    )
    args = parser.parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    selected = args.only or tuple(DIAGRAMS)
    for name in selected:
        build = DIAGRAMS[name]
        svg_path = OUTPUT_DIR / f"{name}.svg"
        png_path = OUTPUT_DIR / f"{name}.png"
        svg_path.write_text(build(), encoding="utf-8")
        render_png(svg_path, png_path)
        normalize(png_path, canvas=(WIDTH, HEIGHT), matte=48)
        print(f"Wrote {svg_path.relative_to(ROOT)} and {png_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
