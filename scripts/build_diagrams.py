#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import shutil
import subprocess


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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, build in DIAGRAMS.items():
        svg_path = OUTPUT_DIR / f"{name}.svg"
        png_path = OUTPUT_DIR / f"{name}.png"
        svg_path.write_text(build(), encoding="utf-8")
        render_png(svg_path, png_path)
        print(f"Wrote {svg_path.relative_to(ROOT)} and {png_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
