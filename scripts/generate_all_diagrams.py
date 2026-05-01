"""
Generate all engineering diagrams for AI Support Copilot.
1. System Architecture Diagram (updated with final tech stack)
2. Pipeline Sequence Diagram
3. Decision Flowchart
4. Data Flow Diagram
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "client-docs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SIM_DIR = "/Users/amit/Work/Gyde/Gyde Pivot/Gyde AI POD Framework/Simulation Docs"

# Color palette
DARK_BLUE = '#1B2A4A'
MEDIUM_BLUE = '#2C5F8A'
LIGHT_BLUE = '#E8F0F8'
ACCENT_ORANGE = '#E86C00'
ACCENT_GREEN = '#2D7D46'
ACCENT_RED = '#CC3333'
ACCENT_PURPLE = '#7B1FA2'
WHITE = '#FFFFFF'
LIGHT_GRAY = '#F5F5F5'
MEDIUM_GRAY = '#999999'
DARK_GRAY = '#333333'
BORDER_GRAY = '#CCCCCC'

# Step colors
CLASSIFY_BG = '#E3F2FD'
CLASSIFY_BORDER = '#1976D2'
RETRIEVE_BG = '#E8F5E9'
RETRIEVE_BORDER = '#388E3C'
REASON_BG = '#FFF3E0'
REASON_BORDER = '#F57C00'
DRAFT_BG = '#F3E5F5'
DRAFT_BORDER = '#7B1FA2'
GUARD_BG = '#FFEBEE'
GUARD_BORDER = '#C62828'
PRESENT_BG = '#E0F2F1'
PRESENT_BORDER = '#00796B'


def draw_box(ax, x, y, w, h, color, border_color=None, radius=0.02, alpha=1.0, lw=1.5):
    rect = FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad={radius}",
        facecolor=color, edgecolor=border_color or color,
        linewidth=lw, alpha=alpha, zorder=2)
    ax.add_patch(rect)
    return rect


def arrow(ax, x1, y1, x2, y2, color=MEDIUM_BLUE, lw=2, style='->'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw), zorder=3)


# =====================================================================
# 1. SYSTEM ARCHITECTURE DIAGRAM (Updated)
# =====================================================================
def generate_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    # Title
    ax.text(0.50, 0.97, 'AI Support Copilot -- System Architecture',
            fontsize=18, fontweight='bold', color=DARK_BLUE,
            va='center', ha='center', family='sans-serif')
    ax.text(0.50, 0.945, 'RAG Pipeline with Human-in-the-Loop',
            fontsize=11, color=MEDIUM_GRAY, va='center', ha='center', family='sans-serif')

    # === FRONTEND (Top) ===
    draw_box(ax, 0.25, 0.84, 0.50, 0.08, LIGHT_BLUE, MEDIUM_BLUE, radius=0.01, lw=2)
    ax.text(0.50, 0.895, 'FRONTEND -- React', fontsize=12, fontweight='bold',
            color=MEDIUM_BLUE, va='center', ha='center', zorder=3)
    ax.text(0.50, 0.865, 'Three-Panel Dashboard: Ticket Queue | Ticket Detail | Copilot Sidebar',
            fontsize=9, color=DARK_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.50, 0.845, 'State: Zustand  |  API: Axios  |  Feedback Widget',
            fontsize=8, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    # Arrow: Frontend -> Backend
    arrow(ax, 0.50, 0.84, 0.50, 0.80, MEDIUM_BLUE, 2, '<->')
    ax.text(0.52, 0.82, 'REST API (HTTPS)', fontsize=7, color=MEDIUM_GRAY, va='center', zorder=3)

    # === BACKEND (Center) ===
    draw_box(ax, 0.15, 0.30, 0.70, 0.50, '#F8FAFC', DARK_BLUE, radius=0.01, lw=2)
    ax.text(0.50, 0.785, 'BACKEND -- Express (Node.js)', fontsize=12, fontweight='bold',
            color=DARK_BLUE, va='center', ha='center', zorder=3)

    # API Router
    draw_box(ax, 0.17, 0.72, 0.28, 0.05, WHITE, BORDER_GRAY, radius=0.008, lw=1)
    ax.text(0.31, 0.745, 'API Router', fontsize=9, fontweight='bold',
            color=DARK_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.31, 0.725, '/api/copilot/process  |  /api/tickets  |  /api/feedback',
            fontsize=6.5, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    # LLM Gateway
    draw_box(ax, 0.55, 0.72, 0.28, 0.05, '#FFF8E8', ACCENT_ORANGE, radius=0.008, lw=1)
    ax.text(0.69, 0.745, 'LLM Gateway', fontsize=9, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)
    ax.text(0.69, 0.725, 'Provider-agnostic  |  Swap via env var',
            fontsize=6.5, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    # Pipeline steps
    steps = [
        ('1. CLASSIFY', 'Gemini (Vertex AI)', CLASSIFY_BG, CLASSIFY_BORDER),
        ('2. RETRIEVE', 'Elasticsearch hybrid', RETRIEVE_BG, RETRIEVE_BORDER),
        ('3. REASON', 'Gemini (Vertex AI)', REASON_BG, REASON_BORDER),
        ('4. DRAFT', 'Gemini (Vertex AI)', DRAFT_BG, DRAFT_BORDER),
        ('5. GUARDRAILS', 'Post-processing', GUARD_BG, GUARD_BORDER),
    ]

    # LangChain.js Pipeline box
    draw_box(ax, 0.17, 0.33, 0.66, 0.36, '#FAFBFC', MEDIUM_BLUE, radius=0.01, lw=1.5)
    ax.text(0.50, 0.675, 'LangChain.js Pipeline Orchestrator', fontsize=10, fontweight='bold',
            color=MEDIUM_BLUE, va='center', ha='center', zorder=3)

    step_w = 0.115
    step_h = 0.28
    start_x = 0.19
    gap = 0.013

    for i, (name, tech, bg, border) in enumerate(steps):
        x = start_x + i * (step_w + gap)
        draw_box(ax, x, 0.35, step_w, step_h, bg, border, radius=0.008, lw=1.5)
        ax.text(x + step_w/2, 0.60, name, fontsize=8, fontweight='bold',
                color=border, va='center', ha='center', rotation=0, zorder=3)
        ax.text(x + step_w/2, 0.57, tech, fontsize=6.5,
                color=DARK_GRAY, va='center', ha='center', zorder=3)

        # Arrows between steps
        if i < len(steps) - 1:
            arrow(ax, x + step_w, 0.49, x + step_w + gap, 0.49, border, 1.5)

    # Step details inside each box
    details = [
        ['Ticket text', 'Category', 'Priority', 'Sentiment', 'Confidence'],
        ['Ticket embed', 'kNN + BM25', 'RRF fusion', 'Top-K KB', 'articles'],
        ['Ticket + KB', '+ Esc. rules', 'Reply/Ask/', 'Escalate', 'CoT reasoning'],
        ['Ticket + KB', '+ Action', 'Grounded', 'response', 'w/ citations'],
        ['Profanity', 'PII check', 'Injection', 'Confidence', 'gate'],
    ]
    for i, items in enumerate(details):
        x = start_x + i * (step_w + gap)
        for j, item in enumerate(items):
            ax.text(x + step_w/2, 0.53 - j * 0.03, item, fontsize=6,
                    color=DARK_GRAY, va='center', ha='center', zorder=3)

    # Audit Logger
    draw_box(ax, 0.17, 0.305, 0.20, 0.03, '#FAFAFA', BORDER_GRAY, radius=0.005, lw=0.5)
    ax.text(0.27, 0.32, 'Audit Logger -- logs every decision to MongoDB',
            fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    # === DATA LAYER (Left side) ===
    draw_box(ax, 0.01, 0.08, 0.22, 0.20, '#F0F8F0', ACCENT_GREEN, radius=0.01, lw=1.5)
    ax.text(0.12, 0.265, 'DATA LAYER', fontsize=10, fontweight='bold',
            color=ACCENT_GREEN, va='center', ha='center', zorder=3)

    # MongoDB
    draw_box(ax, 0.02, 0.17, 0.10, 0.08, WHITE, BORDER_GRAY, radius=0.005, lw=0.5)
    ax.text(0.07, 0.24, 'MongoDB', fontsize=8, fontweight='bold',
            color=DARK_BLUE, va='center', ha='center', zorder=3)
    ax.text(0.07, 0.22, 'tickets', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.07, 0.205, 'feedback', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.07, 0.19, 'audit_log', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    # Elasticsearch
    draw_box(ax, 0.13, 0.17, 0.09, 0.08, WHITE, BORDER_GRAY, radius=0.005, lw=0.5)
    ax.text(0.175, 0.24, 'Elasticsearch', fontsize=8, fontweight='bold',
            color=DARK_BLUE, va='center', ha='center', zorder=3)
    ax.text(0.175, 0.22, 'kb_articles', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.175, 0.205, 'kb_vectors', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.175, 0.19, '768d HNSW', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    # Data source
    draw_box(ax, 0.02, 0.09, 0.20, 0.06, '#FFF8E8', ACCENT_ORANGE, radius=0.005, lw=0.5)
    ax.text(0.12, 0.125, 'Data Source', fontsize=8, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)
    ax.text(0.12, 0.10, 'Pilot: Excel  |  Prod: Freshworks API',
            fontsize=6.5, color=DARK_GRAY, va='center', ha='center', zorder=3)

    # Arrow: Data -> Backend
    arrow(ax, 0.23, 0.22, 0.30, 0.40, ACCENT_GREEN, 1.5, '<->')

    # === VERTEX AI (Right side) ===
    draw_box(ax, 0.78, 0.08, 0.21, 0.20, '#FFF3E0', ACCENT_ORANGE, radius=0.01, lw=1.5)
    ax.text(0.885, 0.265, 'GOOGLE VERTEX AI', fontsize=10, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)

    draw_box(ax, 0.79, 0.17, 0.09, 0.07, WHITE, BORDER_GRAY, radius=0.005, lw=0.5)
    ax.text(0.835, 0.225, 'Gemini', fontsize=8, fontweight='bold',
            color=DARK_BLUE, va='center', ha='center', zorder=3)
    ax.text(0.835, 0.205, 'LLM calls', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.835, 0.19, '(classify,', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.835, 0.178, 'reason, draft)', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    draw_box(ax, 0.89, 0.17, 0.09, 0.07, WHITE, BORDER_GRAY, radius=0.005, lw=0.5)
    ax.text(0.935, 0.225, 'Embeddings', fontsize=8, fontweight='bold',
            color=DARK_BLUE, va='center', ha='center', zorder=3)
    ax.text(0.935, 0.205, 'text-embed', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.935, 0.19, '-005', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.935, 0.178, '768 dims', fontsize=6, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    draw_box(ax, 0.79, 0.09, 0.19, 0.06, '#FFF8E8', BORDER_GRAY, radius=0.005, lw=0.5)
    ax.text(0.885, 0.125, 'Auth: GCP Service Account', fontsize=7, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)
    ax.text(0.885, 0.10, 'roles/aiplatform.user', fontsize=6.5,
            color=DARK_GRAY, va='center', ha='center', zorder=3)

    # Arrow: Backend -> Vertex AI
    arrow(ax, 0.70, 0.40, 0.78, 0.22, ACCENT_ORANGE, 1.5, '<->')

    # === EVALUATION (Bottom center) ===
    draw_box(ax, 0.28, 0.01, 0.44, 0.06, '#E8F0F8', MEDIUM_BLUE, radius=0.008, lw=1)
    ax.text(0.50, 0.055, 'EVALUATION HARNESS', fontsize=9, fontweight='bold',
            color=MEDIUM_BLUE, va='center', ha='center', zorder=3)
    ax.text(0.50, 0.03, 'Golden set (40 cases) + Adversarial (20) + Synthetic (1000)  |  CI: every PR + nightly  |  Target: >=85%',
            fontsize=7, color=DARK_GRAY, va='center', ha='center', zorder=3)

    plt.tight_layout(pad=0.5)
    path = os.path.join(OUTPUT_DIR, "architecture_diagram.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print(f"Saved: {path}")

    # Copy to Simulation Docs
    sim_path = os.path.join(SIM_DIR, "architecture_diagram.png")
    fig2, ax2 = plt.subplots(1, 1, figsize=(16, 10))
    plt.close(fig2)
    import shutil
    shutil.copy2(path, sim_path)
    print(f"Copied: {sim_path}")


# =====================================================================
# 2. PIPELINE SEQUENCE DIAGRAM
# =====================================================================
def generate_sequence_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(16, 11))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    # Title
    ax.text(0.50, 0.97, 'AI Support Copilot -- Pipeline Sequence Diagram',
            fontsize=16, fontweight='bold', color=DARK_BLUE,
            va='center', ha='center', family='sans-serif')
    ax.text(0.50, 0.945, 'Message flow from ticket selection to agent response',
            fontsize=10, color=MEDIUM_GRAY, va='center', ha='center')

    # Actors / Lifelines
    actors = [
        ('Agent\n(Browser)', 0.08, MEDIUM_BLUE),
        ('Express\nAPI', 0.22, DARK_BLUE),
        ('Classify\n(Gemini)', 0.36, CLASSIFY_BORDER),
        ('Retrieve\n(ES)', 0.50, RETRIEVE_BORDER),
        ('Reason\n(Gemini)', 0.64, REASON_BORDER),
        ('Draft\n(Gemini)', 0.78, DRAFT_BORDER),
        ('Guard-\nrails', 0.92, GUARD_BORDER),
    ]

    # Draw actor boxes at top
    for name, x, color in actors:
        draw_box(ax, x - 0.05, 0.88, 0.10, 0.05, color, color, radius=0.008)
        ax.text(x, 0.905, name, fontsize=7.5, fontweight='bold',
                color=WHITE, va='center', ha='center', zorder=3)

    # Draw lifelines
    for name, x, color in actors:
        ax.plot([x, x], [0.88, 0.06], '--', color=BORDER_GRAY, lw=1, zorder=1)

    # Messages (sequence of interactions)
    messages = [
        # (from_x, to_x, y, label, color, style)
        (0.08, 0.22, 0.85, '1. POST /api/copilot/process (ticket_id)', MEDIUM_BLUE, 'solid'),
        (0.22, 0.22, 0.82, '   Fetch ticket from MongoDB', MEDIUM_GRAY, 'dashed'),
        (0.22, 0.36, 0.78, '2. classify(ticket_text)', CLASSIFY_BORDER, 'solid'),
        (0.36, 0.36, 0.75, '   Gemini: structured output prompt', MEDIUM_GRAY, 'dashed'),
        (0.36, 0.22, 0.72, '   {category, priority, sentiment, confidence}', CLASSIFY_BORDER, 'solid'),
        (0.22, 0.50, 0.67, '3. retrieve(ticket_text)', RETRIEVE_BORDER, 'solid'),
        (0.50, 0.50, 0.64, '   Embed ticket (text-embedding-005)', MEDIUM_GRAY, 'dashed'),
        (0.50, 0.50, 0.61, '   kNN + BM25 + RRF fusion', MEDIUM_GRAY, 'dashed'),
        (0.50, 0.22, 0.58, '   top-K KB articles with scores', RETRIEVE_BORDER, 'solid'),
        (0.22, 0.64, 0.53, '4. reason(ticket + KB + rules)', REASON_BORDER, 'solid'),
        (0.64, 0.64, 0.50, '   Gemini: chain-of-thought prompt', MEDIUM_GRAY, 'dashed'),
        (0.64, 0.22, 0.47, '   {action, reasoning, confidence}', REASON_BORDER, 'solid'),
        (0.22, 0.78, 0.42, '5. draft(ticket + KB + action + reasoning)', DRAFT_BORDER, 'solid'),
        (0.78, 0.78, 0.39, '   Gemini: RAG prompt with citation tracking', MEDIUM_GRAY, 'dashed'),
        (0.78, 0.22, 0.36, '   {draft_response, cited_kb_ids, tone}', DRAFT_BORDER, 'solid'),
        (0.22, 0.92, 0.31, '6. guardrails(all_outputs)', GUARD_BORDER, 'solid'),
        (0.92, 0.92, 0.28, '   Profanity + PII + injection + confidence', MEDIUM_GRAY, 'dashed'),
        (0.92, 0.22, 0.25, '   {passed, warnings[]}', GUARD_BORDER, 'solid'),
        (0.22, 0.22, 0.21, '   Log to audit_log (MongoDB)', MEDIUM_GRAY, 'dashed'),
        (0.22, 0.08, 0.17, '7. Full pipeline response (JSON)', MEDIUM_BLUE, 'solid'),
        (0.08, 0.08, 0.13, '   Agent reviews, edits, accepts', MEDIUM_GRAY, 'dashed'),
        (0.08, 0.22, 0.09, '8. POST /api/feedback (helpful, edited_draft)', ACCENT_GREEN, 'solid'),
    ]

    for from_x, to_x, y, label, color, style in messages:
        if from_x == to_x:
            # Self-call or note
            ax.text(from_x + 0.02, y, label, fontsize=7,
                    color=color, va='center', style='italic', zorder=3)
        else:
            # Arrow
            ls = '--' if style == 'dashed' else '-'
            arrow(ax, from_x, y, to_x, y, color, 1.5)
            # Label above arrow
            mid_x = (from_x + to_x) / 2
            offset = 0.01 if from_x < to_x else -0.01
            ax.text(mid_x, y + 0.012, label, fontsize=7, fontweight='bold',
                    color=color, va='center', ha='center', zorder=3)

    # Timing annotations on the right
    ax.text(0.98, 0.78, 'Steps 2-3', fontsize=7, color=CLASSIFY_BORDER,
            va='center', ha='right', fontweight='bold', zorder=3)
    ax.text(0.98, 0.75, 'can run in', fontsize=6, color=MEDIUM_GRAY,
            va='center', ha='right', zorder=3)
    ax.text(0.98, 0.72, 'parallel', fontsize=6, color=MEDIUM_GRAY,
            va='center', ha='right', zorder=3)

    # Latency note
    draw_box(ax, 0.01, 0.01, 0.40, 0.04, '#FFF8E8', ACCENT_ORANGE, radius=0.005, lw=0.5)
    ax.text(0.21, 0.03, 'Target: < 10s end-to-end (p95)  |  Hard limit: < 15s',
            fontsize=8, color=ACCENT_ORANGE, va='center', ha='center', zorder=3)

    draw_box(ax, 0.45, 0.01, 0.54, 0.04, '#F0FFF0', ACCENT_GREEN, radius=0.005, lw=0.5)
    ax.text(0.72, 0.03, 'Classify + Retrieve can run in parallel (saves ~2-3s)  |  All via LLM Gateway',
            fontsize=8, color=ACCENT_GREEN, va='center', ha='center', zorder=3)

    plt.tight_layout(pad=0.5)
    path = os.path.join(OUTPUT_DIR, "sequence_diagram.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print(f"Saved: {path}")

    import shutil
    shutil.copy2(path, os.path.join(SIM_DIR, "sequence_diagram.png"))


# =====================================================================
# 3. DECISION FLOWCHART
# =====================================================================
def generate_flowchart():
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    # Title
    ax.text(0.50, 0.97, 'AI Support Copilot -- Decision Flowchart',
            fontsize=16, fontweight='bold', color=DARK_BLUE,
            va='center', ha='center')
    ax.text(0.50, 0.945, 'From ticket input to agent action',
            fontsize=10, color=MEDIUM_GRAY, va='center', ha='center')

    # Helper for diamond (decision node)
    def draw_diamond(ax, cx, cy, w, h, color, border):
        diamond = plt.Polygon([
            [cx, cy + h/2],     # top
            [cx + w/2, cy],     # right
            [cx, cy - h/2],     # bottom
            [cx - w/2, cy],     # left
        ], closed=True, facecolor=color, edgecolor=border, lw=1.5, zorder=2)
        ax.add_patch(diamond)

    # --- START ---
    draw_box(ax, 0.40, 0.89, 0.20, 0.04, DARK_BLUE, DARK_BLUE, radius=0.008)
    ax.text(0.50, 0.91, 'TICKET RECEIVED', fontsize=10, fontweight='bold',
            color=WHITE, va='center', ha='center', zorder=3)

    arrow(ax, 0.50, 0.89, 0.50, 0.86)

    # Step 1: Classify
    draw_box(ax, 0.30, 0.81, 0.40, 0.05, CLASSIFY_BG, CLASSIFY_BORDER, radius=0.008, lw=1.5)
    ax.text(0.50, 0.84, 'Step 1: CLASSIFY', fontsize=10, fontweight='bold',
            color=CLASSIFY_BORDER, va='center', ha='center', zorder=3)
    ax.text(0.50, 0.82, 'LLM extracts: category, priority, sentiment, confidence',
            fontsize=8, color=DARK_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.50, 0.81, 0.50, 0.78)

    # Decision: Confidence > threshold?
    draw_diamond(ax, 0.50, 0.75, 0.22, 0.05, '#FFF8E8', ACCENT_ORANGE)
    ax.text(0.50, 0.75, 'Confidence >= 0.5?', fontsize=8, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)

    # No -> Flag low confidence
    arrow(ax, 0.61, 0.75, 0.78, 0.75, ACCENT_RED, 1.5)
    ax.text(0.68, 0.76, 'No', fontsize=8, fontweight='bold', color=ACCENT_RED,
            va='center', ha='center', zorder=3)
    draw_box(ax, 0.78, 0.73, 0.18, 0.04, '#FFEBEE', ACCENT_RED, radius=0.005)
    ax.text(0.87, 0.75, 'Flag: low confidence\nContinue with warning', fontsize=7,
            color=ACCENT_RED, va='center', ha='center', zorder=3)

    # Yes -> Continue
    arrow(ax, 0.50, 0.725, 0.50, 0.69, ACCENT_GREEN, 1.5)
    ax.text(0.47, 0.71, 'Yes', fontsize=8, fontweight='bold', color=ACCENT_GREEN,
            va='center', zorder=3)

    # Step 2: Retrieve
    draw_box(ax, 0.30, 0.64, 0.40, 0.05, RETRIEVE_BG, RETRIEVE_BORDER, radius=0.008, lw=1.5)
    ax.text(0.50, 0.67, 'Step 2: RETRIEVE', fontsize=10, fontweight='bold',
            color=RETRIEVE_BORDER, va='center', ha='center', zorder=3)
    ax.text(0.50, 0.65, 'Hybrid search: vector (kNN) + keyword (BM25) via RRF',
            fontsize=8, color=DARK_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.50, 0.64, 0.50, 0.61)

    # Decision: KB match found?
    draw_diamond(ax, 0.50, 0.58, 0.22, 0.05, '#FFF8E8', ACCENT_ORANGE)
    ax.text(0.50, 0.58, 'Relevant KB found?', fontsize=8, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)

    # No -> Unknown category path
    arrow(ax, 0.39, 0.58, 0.10, 0.58, ACCENT_RED, 1.5)
    ax.text(0.25, 0.59, 'No match', fontsize=8, fontweight='bold', color=ACCENT_RED,
            va='center', ha='center', zorder=3)
    draw_box(ax, 0.02, 0.55, 0.16, 0.05, '#FFEBEE', ACCENT_RED, radius=0.005)
    ax.text(0.10, 0.58, 'Flag: "No KB match"\nAction = Ask', fontsize=7.5,
            color=ACCENT_RED, va='center', ha='center', zorder=3)

    # Yes -> Continue
    arrow(ax, 0.50, 0.555, 0.50, 0.52, ACCENT_GREEN, 1.5)
    ax.text(0.47, 0.54, 'Yes', fontsize=8, fontweight='bold', color=ACCENT_GREEN,
            va='center', zorder=3)

    # Step 3: Reason
    draw_box(ax, 0.30, 0.47, 0.40, 0.05, REASON_BG, REASON_BORDER, radius=0.008, lw=1.5)
    ax.text(0.50, 0.50, 'Step 3: REASON', fontsize=10, fontweight='bold',
            color=REASON_BORDER, va='center', ha='center', zorder=3)
    ax.text(0.50, 0.48, 'LLM analyzes: ticket + KB + escalation rules',
            fontsize=8, color=DARK_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.50, 0.47, 0.50, 0.44)

    # Decision: What action?
    draw_diamond(ax, 0.50, 0.41, 0.26, 0.05, '#FFF8E8', ACCENT_ORANGE)
    ax.text(0.50, 0.41, 'Recommended action?', fontsize=8, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)

    # Three paths
    # ESCALATE (left)
    arrow(ax, 0.37, 0.41, 0.10, 0.41, ACCENT_RED, 1.5)
    ax.text(0.24, 0.42, 'ESCALATE', fontsize=8, fontweight='bold', color=ACCENT_RED,
            va='center', ha='center', zorder=3)
    draw_box(ax, 0.02, 0.37, 0.16, 0.06, '#FFEBEE', ACCENT_RED, radius=0.005)
    ax.text(0.10, 0.405, 'Escalation triggered', fontsize=8, fontweight='bold',
            color=ACCENT_RED, va='center', ha='center', zorder=3)
    ax.text(0.10, 0.385, 'Team + context\nidentified by rules', fontsize=7,
            color=DARK_GRAY, va='center', ha='center', zorder=3)

    # ASK (right)
    arrow(ax, 0.63, 0.41, 0.82, 0.41, ACCENT_ORANGE, 1.5)
    ax.text(0.73, 0.42, 'ASK', fontsize=8, fontweight='bold', color=ACCENT_ORANGE,
            va='center', ha='center', zorder=3)
    draw_box(ax, 0.82, 0.37, 0.16, 0.06, '#FFF8E8', ACCENT_ORANGE, radius=0.005)
    ax.text(0.90, 0.405, 'Need more info', fontsize=8, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)
    ax.text(0.90, 0.385, 'Insufficient context\nto resolve', fontsize=7,
            color=DARK_GRAY, va='center', ha='center', zorder=3)

    # REPLY (down)
    arrow(ax, 0.50, 0.385, 0.50, 0.35, ACCENT_GREEN, 1.5)
    ax.text(0.53, 0.37, 'REPLY', fontsize=8, fontweight='bold', color=ACCENT_GREEN,
            va='center', zorder=3)

    # Step 4: Draft
    draw_box(ax, 0.30, 0.30, 0.40, 0.05, DRAFT_BG, DRAFT_BORDER, radius=0.008, lw=1.5)
    ax.text(0.50, 0.33, 'Step 4: DRAFT', fontsize=10, fontweight='bold',
            color=DRAFT_BORDER, va='center', ha='center', zorder=3)
    ax.text(0.50, 0.31, 'Generate grounded response with KB citations',
            fontsize=8, color=DARK_GRAY, va='center', ha='center', zorder=3)

    # All three paths converge to guardrails
    arrow(ax, 0.10, 0.37, 0.10, 0.24, MEDIUM_GRAY, 1)
    arrow(ax, 0.10, 0.24, 0.30, 0.24, MEDIUM_GRAY, 1)
    arrow(ax, 0.90, 0.37, 0.90, 0.24, MEDIUM_GRAY, 1)
    arrow(ax, 0.90, 0.24, 0.70, 0.24, MEDIUM_GRAY, 1)
    arrow(ax, 0.50, 0.30, 0.50, 0.27)

    # Step 5: Guardrails
    draw_box(ax, 0.30, 0.20, 0.40, 0.05, GUARD_BG, GUARD_BORDER, radius=0.008, lw=1.5)
    ax.text(0.50, 0.23, 'Step 5: GUARDRAILS', fontsize=10, fontweight='bold',
            color=GUARD_BORDER, va='center', ha='center', zorder=3)
    ax.text(0.50, 0.21, 'Profanity + PII + injection + hallucination + confidence',
            fontsize=8, color=DARK_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.50, 0.20, 0.50, 0.17)

    # Decision: Guardrails pass?
    draw_diamond(ax, 0.50, 0.14, 0.22, 0.05, '#FFF8E8', ACCENT_ORANGE)
    ax.text(0.50, 0.14, 'Guardrails pass?', fontsize=8, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)

    # No -> Show with warning
    arrow(ax, 0.61, 0.14, 0.78, 0.14, ACCENT_RED, 1.5)
    ax.text(0.68, 0.15, 'Fail', fontsize=8, fontweight='bold', color=ACCENT_RED,
            va='center', ha='center', zorder=3)
    draw_box(ax, 0.78, 0.12, 0.18, 0.04, '#FFEBEE', ACCENT_RED, radius=0.005)
    ax.text(0.87, 0.14, 'Show with warning\nbanner to agent', fontsize=7,
            color=ACCENT_RED, va='center', ha='center', zorder=3)
    arrow(ax, 0.87, 0.12, 0.87, 0.07, ACCENT_RED, 1)
    arrow(ax, 0.87, 0.07, 0.62, 0.07, ACCENT_RED, 1)

    # Yes -> Present
    arrow(ax, 0.50, 0.115, 0.50, 0.08, ACCENT_GREEN, 1.5)
    ax.text(0.47, 0.10, 'Pass', fontsize=8, fontweight='bold', color=ACCENT_GREEN,
            va='center', zorder=3)

    # PRESENT to Agent
    draw_box(ax, 0.30, 0.03, 0.40, 0.05, PRESENT_BG, PRESENT_BORDER, radius=0.008, lw=2)
    ax.text(0.50, 0.06, 'PRESENT TO AGENT', fontsize=10, fontweight='bold',
            color=PRESENT_BORDER, va='center', ha='center', zorder=3)
    ax.text(0.50, 0.04, 'Classification + KB matches + Action + Draft + Confidence',
            fontsize=8, color=DARK_GRAY, va='center', ha='center', zorder=3)

    # Legend
    draw_box(ax, 0.02, 0.02, 0.16, 0.10, '#FAFAFA', BORDER_GRAY, radius=0.005, lw=0.5)
    ax.text(0.10, 0.11, 'LEGEND', fontsize=8, fontweight='bold',
            color=DARK_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.04, 0.09, 'Rectangle = Process step', fontsize=6.5,
            color=DARK_GRAY, va='center', zorder=3)
    ax.text(0.04, 0.07, 'Diamond = Decision', fontsize=6.5,
            color=DARK_GRAY, va='center', zorder=3)
    ax.text(0.04, 0.05, 'Green = Yes/Pass', fontsize=6.5,
            color=ACCENT_GREEN, va='center', zorder=3)
    ax.text(0.04, 0.03, 'Red = No/Fail/Escalate', fontsize=6.5,
            color=ACCENT_RED, va='center', zorder=3)

    plt.tight_layout(pad=0.5)
    path = os.path.join(OUTPUT_DIR, "decision_flowchart.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print(f"Saved: {path}")

    import shutil
    shutil.copy2(path, os.path.join(SIM_DIR, "decision_flowchart.png"))


# =====================================================================
# 4. DATA FLOW DIAGRAM
# =====================================================================
def generate_data_flow():
    fig, ax = plt.subplots(1, 1, figsize=(16, 9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    # Title
    ax.text(0.50, 0.97, 'AI Support Copilot -- Data Flow & Integration Points',
            fontsize=16, fontweight='bold', color=DARK_BLUE,
            va='center', ha='center')
    ax.text(0.50, 0.945, 'Pilot (Excel) vs Production (Freshworks API) data paths',
            fontsize=10, color=MEDIUM_GRAY, va='center', ha='center')

    # === PILOT PATH (Top) ===
    draw_box(ax, 0.02, 0.72, 0.96, 0.20, '#F0FFF0', ACCENT_GREEN, radius=0.01, lw=2)
    ax.text(0.50, 0.905, 'PILOT DATA PATH (Current)', fontsize=12, fontweight='bold',
            color=ACCENT_GREEN, va='center', ha='center', zorder=3)

    # Excel
    draw_box(ax, 0.04, 0.74, 0.13, 0.08, WHITE, ACCENT_GREEN, radius=0.008, lw=1.5)
    ax.text(0.105, 0.80, 'Excel Dataset', fontsize=9, fontweight='bold',
            color=DARK_BLUE, va='center', ha='center', zorder=3)
    ax.text(0.105, 0.775, '36 tickets', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.105, 0.755, '12 KB articles', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    # Ingestion Script
    draw_box(ax, 0.22, 0.74, 0.13, 0.08, '#E8F5E9', ACCENT_GREEN, radius=0.008, lw=1)
    ax.text(0.285, 0.80, 'Ingestion', fontsize=9, fontweight='bold',
            color=ACCENT_GREEN, va='center', ha='center', zorder=3)
    ax.text(0.285, 0.775, 'Script', fontsize=9, fontweight='bold',
            color=ACCENT_GREEN, va='center', ha='center', zorder=3)
    ax.text(0.285, 0.755, '(one-time run)', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.17, 0.78, 0.22, 0.78, ACCENT_GREEN, 1.5)

    # MongoDB
    draw_box(ax, 0.40, 0.74, 0.13, 0.08, WHITE, DARK_BLUE, radius=0.008, lw=1.5)
    ax.text(0.465, 0.80, 'MongoDB', fontsize=9, fontweight='bold',
            color=DARK_BLUE, va='center', ha='center', zorder=3)
    ax.text(0.465, 0.775, 'tickets collection', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.465, 0.755, 'feedback + audit', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.35, 0.78, 0.40, 0.78, ACCENT_GREEN, 1.5)

    # Embedding
    draw_box(ax, 0.58, 0.74, 0.13, 0.08, '#FFF3E0', ACCENT_ORANGE, radius=0.008, lw=1)
    ax.text(0.645, 0.80, 'Vertex AI', fontsize=9, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)
    ax.text(0.645, 0.775, 'text-embedding', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.645, 0.755, '-005 (768d)', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.35, 0.76, 0.58, 0.76, ACCENT_ORANGE, 1, '->')
    ax.text(0.465, 0.745, 'KB text', fontsize=7, color=ACCENT_ORANGE, va='center', ha='center', zorder=3)

    # Elasticsearch
    draw_box(ax, 0.76, 0.74, 0.13, 0.08, WHITE, RETRIEVE_BORDER, radius=0.008, lw=1.5)
    ax.text(0.825, 0.80, 'Elasticsearch', fontsize=9, fontweight='bold',
            color=RETRIEVE_BORDER, va='center', ha='center', zorder=3)
    ax.text(0.825, 0.775, 'kb_articles (BM25)', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.825, 0.755, 'kb_vectors (kNN)', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.71, 0.78, 0.76, 0.78, RETRIEVE_BORDER, 1.5)
    arrow(ax, 0.35, 0.80, 0.76, 0.86, ACCENT_GREEN, 1, '->')
    ax.text(0.56, 0.845, 'KB articles (text)', fontsize=7, color=ACCENT_GREEN, va='center', ha='center', zorder=3)

    # === PRODUCTION PATH (Bottom of top section) ===
    draw_box(ax, 0.02, 0.50, 0.96, 0.18, '#FFF8E8', ACCENT_ORANGE, radius=0.01, lw=2)
    ax.text(0.50, 0.665, 'PRODUCTION DATA PATH (Future)', fontsize=12, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)

    # Freshworks
    draw_box(ax, 0.04, 0.52, 0.13, 0.08, WHITE, ACCENT_ORANGE, radius=0.008, lw=1.5)
    ax.text(0.105, 0.58, 'Freshworks', fontsize=9, fontweight='bold',
            color=DARK_BLUE, va='center', ha='center', zorder=3)
    ax.text(0.105, 0.555, 'Freshdesk tickets', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.105, 0.535, 'Freshworks KB', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    # Webhook/Polling
    draw_box(ax, 0.22, 0.52, 0.13, 0.08, '#FFF3E0', ACCENT_ORANGE, radius=0.008, lw=1)
    ax.text(0.285, 0.58, 'Webhook /', fontsize=9, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)
    ax.text(0.285, 0.555, 'Polling', fontsize=9, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', zorder=3)
    ax.text(0.285, 0.535, '(scheduled)', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.17, 0.56, 0.22, 0.56, ACCENT_ORANGE, 1.5)

    # Same MongoDB + ES (arrows pointing to same stores)
    draw_box(ax, 0.40, 0.52, 0.13, 0.08, WHITE, DARK_BLUE, radius=0.008, lw=1.5)
    ax.text(0.465, 0.58, 'MongoDB', fontsize=9, fontweight='bold',
            color=DARK_BLUE, va='center', ha='center', zorder=3)
    ax.text(0.465, 0.555, '(same schema)', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.35, 0.56, 0.40, 0.56, ACCENT_ORANGE, 1.5)

    draw_box(ax, 0.58, 0.52, 0.13, 0.08, WHITE, RETRIEVE_BORDER, radius=0.008, lw=1.5)
    ax.text(0.645, 0.58, 'Elasticsearch', fontsize=9, fontweight='bold',
            color=RETRIEVE_BORDER, va='center', ha='center', zorder=3)
    ax.text(0.645, 0.555, '(same index)', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.53, 0.56, 0.58, 0.56, ACCENT_ORANGE, 1.5)
    ax.text(0.555, 0.545, 'KB re-index', fontsize=6, color=ACCENT_ORANGE, va='center', ha='center', zorder=3)

    # Chrome Extension
    draw_box(ax, 0.76, 0.52, 0.13, 0.08, '#E0F2F1', PRESENT_BORDER, radius=0.008, lw=1.5)
    ax.text(0.825, 0.58, 'Chrome Ext', fontsize=9, fontweight='bold',
            color=PRESENT_BORDER, va='center', ha='center', zorder=3)
    ax.text(0.825, 0.555, 'Sidebar on', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)
    ax.text(0.825, 0.535, 'Freshdesk', fontsize=7, color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    ax.text(0.91, 0.56, 'Same\nbackend\nAPI', fontsize=7, fontweight='bold',
            color=PRESENT_BORDER, va='center', ha='center', zorder=3)

    # === PIPELINE (center) ===
    draw_box(ax, 0.15, 0.25, 0.70, 0.20, '#F8FAFC', MEDIUM_BLUE, radius=0.01, lw=2)
    ax.text(0.50, 0.44, 'AI PIPELINE (Same for both paths)', fontsize=11, fontweight='bold',
            color=MEDIUM_BLUE, va='center', ha='center', zorder=3)

    pipe_steps = [
        ('CLASSIFY', CLASSIFY_BG, CLASSIFY_BORDER),
        ('RETRIEVE', RETRIEVE_BG, RETRIEVE_BORDER),
        ('REASON', REASON_BG, REASON_BORDER),
        ('DRAFT', DRAFT_BG, DRAFT_BORDER),
        ('GUARD', GUARD_BG, GUARD_BORDER),
    ]
    for i, (name, bg, border) in enumerate(pipe_steps):
        x = 0.17 + i * 0.135
        draw_box(ax, x, 0.27, 0.11, 0.12, bg, border, radius=0.008, lw=1.5)
        ax.text(x + 0.055, 0.34, name, fontsize=9, fontweight='bold',
                color=border, va='center', ha='center', zorder=3)
        if i < len(pipe_steps) - 1:
            arrow(ax, x + 0.11, 0.33, x + 0.135, 0.33, border, 1.5)

    # Arrows from data stores to pipeline
    arrow(ax, 0.465, 0.74, 0.35, 0.45, DARK_BLUE, 1.5)
    arrow(ax, 0.825, 0.74, 0.60, 0.45, RETRIEVE_BORDER, 1.5)

    # === OUTPUTS (Bottom) ===
    draw_box(ax, 0.15, 0.05, 0.70, 0.15, LIGHT_BLUE, MEDIUM_BLUE, radius=0.01, lw=1.5)
    ax.text(0.50, 0.185, 'OUTPUT STORES', fontsize=10, fontweight='bold',
            color=MEDIUM_BLUE, va='center', ha='center', zorder=3)

    outputs = [
        ('Audit Log\n(MongoDB)', 'Every decision\nlogged'),
        ('Feedback\n(MongoDB)', 'Agent ratings\n+ edits'),
        ('Eval Reports\n(Git)', 'Metrics per\neval run'),
        ('Pipeline\nResponse', 'JSON to\nfrontend'),
    ]
    for i, (name, detail) in enumerate(outputs):
        x = 0.18 + i * 0.165
        draw_box(ax, x, 0.06, 0.13, 0.09, WHITE, BORDER_GRAY, radius=0.005, lw=0.5)
        ax.text(x + 0.065, 0.13, name, fontsize=8, fontweight='bold',
                color=DARK_BLUE, va='center', ha='center', zorder=3)
        ax.text(x + 0.065, 0.085, detail, fontsize=7,
                color=MEDIUM_GRAY, va='center', ha='center', zorder=3)

    arrow(ax, 0.50, 0.25, 0.50, 0.20, MEDIUM_BLUE, 1.5)

    plt.tight_layout(pad=0.5)
    path = os.path.join(OUTPUT_DIR, "data_flow_diagram.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print(f"Saved: {path}")

    import shutil
    shutil.copy2(path, os.path.join(SIM_DIR, "data_flow_diagram.png"))


if __name__ == "__main__":
    generate_architecture()
    generate_sequence_diagram()
    generate_flowchart()
    generate_data_flow()
    print("\nAll diagrams generated successfully.")
