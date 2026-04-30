"""
Generate diagrams for Team Briefing document.
1. UI Wireframe Mockup (three-panel dashboard)
2. System Architecture Diagram (AI pipeline flow)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "client-docs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color palette
DARK_BLUE = '#1B2A4A'
MEDIUM_BLUE = '#2C5F8A'
LIGHT_BLUE = '#E8F0F8'
ACCENT_ORANGE = '#E86C00'
ACCENT_GREEN = '#2D7D46'
ACCENT_RED = '#CC3333'
WHITE = '#FFFFFF'
LIGHT_GRAY = '#F5F5F5'
MEDIUM_GRAY = '#999999'
DARK_GRAY = '#333333'
BORDER_GRAY = '#CCCCCC'


def draw_rounded_rect(ax, x, y, w, h, color, border_color=None, radius=0.02, alpha=1.0, lw=1.5):
    """Draw a rounded rectangle."""
    rect = FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad={radius}",
        facecolor=color, edgecolor=border_color or color,
        linewidth=lw, alpha=alpha, zorder=2)
    ax.add_patch(rect)
    return rect


def generate_ui_wireframe():
    """Generate UI wireframe mockup of the three-panel dashboard."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    # Title bar
    draw_rounded_rect(ax, 0.02, 0.92, 0.96, 0.06, DARK_BLUE, radius=0.01)
    ax.text(0.05, 0.95, 'AI Support Copilot', fontsize=14, fontweight='bold',
            color=WHITE, va='center', family='sans-serif')
    ax.text(0.85, 0.95, 'Agent: Asha  |  Pilot v1.0', fontsize=9,
            color='#BBCCDD', va='center', family='sans-serif')

    # === LEFT PANEL: Ticket Queue ===
    draw_rounded_rect(ax, 0.02, 0.08, 0.22, 0.82, LIGHT_GRAY, BORDER_GRAY, radius=0.01)

    # Panel header
    draw_rounded_rect(ax, 0.02, 0.83, 0.22, 0.07, MEDIUM_BLUE, radius=0.01)
    ax.text(0.13, 0.865, 'TICKET QUEUE', fontsize=10, fontweight='bold',
            color=WHITE, va='center', ha='center', family='sans-serif')

    # Ticket items
    tickets = [
        ('TKT-1001', 'SSO login fails after...', 'High', True),
        ('TKT-1002', 'Invoice shows wrong...', 'Med', False),
        ('TKT-1003', 'CSV import stuck at...', 'Med', False),
        ('TKT-1004', 'Slack integration...', 'Med', False),
        ('TKT-1005', 'Admin can\'t revoke...', 'Low', False),
        ('TKT-1006', 'Billing cycle date...', 'Med', False),
        ('TKT-1007', 'GDPR export request...', 'Crit', False),
        ('TKT-1008', 'OTP not arriving...', 'High', False),
    ]

    for i, (tid, subj, pri, selected) in enumerate(tickets):
        ypos = 0.78 - i * 0.085
        bg = '#D4E4F7' if selected else WHITE
        border = MEDIUM_BLUE if selected else BORDER_GRAY
        lw = 2 if selected else 1
        draw_rounded_rect(ax, 0.03, ypos, 0.20, 0.07, bg, border, radius=0.008, lw=lw)

        # Priority dot
        pri_colors = {'Crit': ACCENT_RED, 'High': ACCENT_ORANGE, 'Med': '#DAA520', 'Low': ACCENT_GREEN}
        ax.plot(0.045, ypos + 0.05, 'o', color=pri_colors.get(pri, MEDIUM_GRAY), markersize=6, zorder=3)

        ax.text(0.065, ypos + 0.05, tid, fontsize=7, fontweight='bold',
                color=DARK_GRAY, va='center', family='sans-serif', zorder=3)
        ax.text(0.065, ypos + 0.02, subj[:22], fontsize=6.5,
                color=MEDIUM_GRAY, va='center', family='sans-serif', zorder=3)

    ax.text(0.13, 0.11, '36 tickets  |  Filter \u25bc', fontsize=7,
            color=MEDIUM_GRAY, va='center', ha='center', family='sans-serif')

    # === CENTER PANEL: Ticket Detail ===
    draw_rounded_rect(ax, 0.25, 0.08, 0.38, 0.82, WHITE, BORDER_GRAY, radius=0.01)

    # Panel header
    draw_rounded_rect(ax, 0.25, 0.83, 0.38, 0.07, MEDIUM_BLUE, radius=0.01)
    ax.text(0.44, 0.865, 'TICKET DETAIL', fontsize=10, fontweight='bold',
            color=WHITE, va='center', ha='center', family='sans-serif')

    # Ticket info
    ax.text(0.27, 0.79, 'TKT-1001', fontsize=12, fontweight='bold',
            color=DARK_BLUE, va='center', family='sans-serif')
    ax.text(0.27, 0.76, 'SSO login fails after password reset', fontsize=10,
            color=DARK_GRAY, va='center', family='sans-serif')

    # Metadata chips
    chips = [('Customer:', 'Acme Corp'), ('Channel:', 'Email'), ('Created:', '2025-01-15')]
    for i, (label, val) in enumerate(chips):
        xpos = 0.27 + i * 0.125
        draw_rounded_rect(ax, xpos, 0.715, 0.11, 0.03, LIGHT_BLUE, MEDIUM_BLUE, radius=0.005, lw=0.5)
        ax.text(xpos + 0.005, 0.73, label, fontsize=6, fontweight='bold',
                color=MEDIUM_BLUE, va='center', family='sans-serif', zorder=3)
        ax.text(xpos + 0.055, 0.73, val, fontsize=6,
                color=DARK_GRAY, va='center', family='sans-serif', zorder=3)

    # Description box
    draw_rounded_rect(ax, 0.27, 0.45, 0.34, 0.24, '#FAFAFA', BORDER_GRAY, radius=0.008, lw=0.5)
    ax.text(0.28, 0.67, 'Description', fontsize=8, fontweight='bold',
            color=DARK_GRAY, va='center', family='sans-serif', zorder=3)

    desc_lines = [
        'User changed their password yesterday through',
        'the admin portal. Today when attempting SSO',
        'login, the system throws a 403 Forbidden error.',
        '',
        'Steps attempted by customer:',
        '  - Cleared browser cache and cookies',
        '  - Tried incognito mode',
        '  - Tried different browser',
        '',
        'Issue persists across all browsers. Customer',
        'reports that other team members with SSO are',
        'not affected. Urgent \u2014 blocking their workflow.',
    ]
    for i, line in enumerate(desc_lines):
        ax.text(0.28, 0.645 - i * 0.016, line, fontsize=6.5,
                color=DARK_GRAY if line.strip() else MEDIUM_GRAY,
                va='center', family='monospace', zorder=3)

    # SLA bar
    draw_rounded_rect(ax, 0.27, 0.39, 0.34, 0.04, '#FFF8E8', '#DAA520', radius=0.005, lw=0.5)
    ax.text(0.28, 0.41, 'SLA:', fontsize=7, fontweight='bold',
            color=ACCENT_ORANGE, va='center', family='sans-serif', zorder=3)
    ax.text(0.31, 0.41, '12 hours  |  8h 23m remaining', fontsize=7,
            color=DARK_GRAY, va='center', family='sans-serif', zorder=3)

    # Resolution area
    draw_rounded_rect(ax, 0.27, 0.12, 0.34, 0.25, WHITE, BORDER_GRAY, radius=0.008, lw=0.5)
    ax.text(0.28, 0.35, 'Agent Response', fontsize=8, fontweight='bold',
            color=DARK_GRAY, va='center', family='sans-serif', zorder=3)
    ax.text(0.28, 0.325, 'Draft will be inserted here from copilot \u2192', fontsize=7,
            color=MEDIUM_GRAY, va='center', family='sans-serif', style='italic', zorder=3)

    # Send button
    draw_rounded_rect(ax, 0.50, 0.13, 0.10, 0.035, ACCENT_GREEN, radius=0.005)
    ax.text(0.55, 0.148, 'Send Reply', fontsize=8, fontweight='bold',
            color=WHITE, va='center', ha='center', family='sans-serif', zorder=3)

    # === RIGHT PANEL: Copilot Sidebar ===
    draw_rounded_rect(ax, 0.64, 0.08, 0.34, 0.82, LIGHT_BLUE, MEDIUM_BLUE, radius=0.01, lw=2)

    # Panel header
    draw_rounded_rect(ax, 0.64, 0.83, 0.34, 0.07, DARK_BLUE, radius=0.01)
    ax.text(0.68, 0.865, '\u25C6', fontsize=10, color='#88AACC', va='center', ha='center', zorder=3)
    ax.text(0.72, 0.865, 'COPILOT', fontsize=10, fontweight='bold',
            color=WHITE, va='center', family='sans-serif')
    ax.text(0.90, 0.865, 'Processing...', fontsize=8,
            color='#88AACC', va='center', family='sans-serif')

    # Classification section
    draw_rounded_rect(ax, 0.65, 0.71, 0.32, 0.10, WHITE, BORDER_GRAY, radius=0.008, lw=0.5)
    ax.text(0.66, 0.795, 'CLASSIFICATION', fontsize=7, fontweight='bold',
            color=MEDIUM_BLUE, va='center', family='sans-serif', zorder=3)

    class_items = [
        ('Category:', 'Authentication', DARK_GRAY),
        ('Priority:', 'High', ACCENT_ORANGE),
        ('Sentiment:', 'Frustrated', ACCENT_RED),
        ('Confidence:', '92%', ACCENT_GREEN),
    ]
    for i, (label, val, color) in enumerate(class_items):
        ypos = 0.775 - i * 0.017
        ax.text(0.66, ypos, label, fontsize=7, fontweight='bold',
                color=MEDIUM_GRAY, va='center', family='sans-serif', zorder=3)
        ax.text(0.745, ypos, val, fontsize=7, fontweight='bold',
                color=color, va='center', family='sans-serif', zorder=3)

    # Action section
    draw_rounded_rect(ax, 0.65, 0.63, 0.32, 0.07, '#F0FFF0', ACCENT_GREEN, radius=0.008, lw=1)
    ax.text(0.66, 0.685, 'RECOMMENDED ACTION', fontsize=7, fontweight='bold',
            color=ACCENT_GREEN, va='center', family='sans-serif', zorder=3)
    ax.text(0.66, 0.66, 'Reply', fontsize=11, fontweight='bold',
            color=DARK_BLUE, va='center', family='sans-serif', zorder=3)
    ax.text(0.72, 0.66, '  \u2014  Standard resolution path via KB-001', fontsize=6.5,
            color=MEDIUM_GRAY, va='center', family='sans-serif', zorder=3)
    ax.text(0.66, 0.64, 'No escalation rule triggered', fontsize=6.5,
            color=MEDIUM_GRAY, va='center', family='sans-serif', zorder=3)

    # KB Articles section
    draw_rounded_rect(ax, 0.65, 0.48, 0.32, 0.14, WHITE, BORDER_GRAY, radius=0.008, lw=0.5)
    ax.text(0.66, 0.605, 'RELEVANT KB ARTICLES', fontsize=7, fontweight='bold',
            color=MEDIUM_BLUE, va='center', family='sans-serif', zorder=3)

    kb_items = [
        ('KB-001', 'SSO Configuration & Troubleshooting', '0.94'),
        ('KB-002', 'MFA Setup and Recovery', '0.81'),
        ('KB-010', 'Role-Based Access Control Guide', '0.45'),
    ]
    for i, (kb_id, title, score) in enumerate(kb_items):
        ypos = 0.58 - i * 0.03
        bar_color = ACCENT_GREEN if float(score) > 0.8 else ('#DAA520' if float(score) > 0.6 else MEDIUM_GRAY)
        # Score bar
        draw_rounded_rect(ax, 0.66, ypos - 0.005, float(score) * 0.12, 0.008, bar_color, radius=0.002, lw=0)
        ax.text(0.66, ypos + 0.01, f'{kb_id}: {title}', fontsize=6.5, fontweight='bold',
                color=DARK_GRAY, va='center', family='sans-serif', zorder=3)
        ax.text(0.94, ypos + 0.01, score, fontsize=7, fontweight='bold',
                color=bar_color, va='center', ha='right', family='sans-serif', zorder=3)

    # Draft Response section
    draw_rounded_rect(ax, 0.65, 0.21, 0.32, 0.26, WHITE, BORDER_GRAY, radius=0.008, lw=0.5)
    ax.text(0.66, 0.455, 'DRAFT RESPONSE', fontsize=7, fontweight='bold',
            color=MEDIUM_BLUE, va='center', family='sans-serif', zorder=3)

    draft_lines = [
        'Dear Acme Corp team,',
        '',
        'Thank you for reporting this SSO issue.',
        'Based on our SSO Configuration Guide',
        '[KB-001], this typically occurs when the',
        'identity provider cache retains the old',
        'password hash after a reset.',
        '',
        'Please try the following steps:',
        '1. Navigate to Admin > SSO Settings',
        '2. Click "Force Token Refresh"',
        '3. Ask the user to log out and back in',
        '',
        'If the issue persists after these steps,',
        'please let us know and we will escalate',
        'to our engineering team.',
    ]
    for i, line in enumerate(draft_lines):
        ax.text(0.66, 0.435 - i * 0.014, line, fontsize=6,
                color=DARK_GRAY, va='center', family='sans-serif', zorder=3)

    # Action buttons
    draw_rounded_rect(ax, 0.65, 0.14, 0.10, 0.035, ACCENT_GREEN, radius=0.005)
    ax.text(0.70, 0.158, 'Accept', fontsize=8, fontweight='bold',
            color=WHITE, va='center', ha='center', family='sans-serif', zorder=3)

    draw_rounded_rect(ax, 0.76, 0.14, 0.10, 0.035, MEDIUM_BLUE, radius=0.005)
    ax.text(0.81, 0.158, 'Edit', fontsize=8, fontweight='bold',
            color=WHITE, va='center', ha='center', family='sans-serif', zorder=3)

    draw_rounded_rect(ax, 0.87, 0.14, 0.10, 0.035, WHITE, BORDER_GRAY, radius=0.005)
    ax.text(0.92, 0.158, 'Override', fontsize=8, fontweight='bold',
            color=MEDIUM_GRAY, va='center', ha='center', family='sans-serif', zorder=3)

    # Feedback section
    draw_rounded_rect(ax, 0.65, 0.08, 0.32, 0.05, '#FAFAFA', BORDER_GRAY, radius=0.008, lw=0.5)
    ax.text(0.70, 0.105, 'Was this helpful?', fontsize=7,
            color=MEDIUM_GRAY, va='center', family='sans-serif', zorder=3)
    ax.text(0.85, 0.105, 'YES  |  NO', fontsize=8, fontweight='bold',
            color=MEDIUM_BLUE, va='center', ha='center', family='sans-serif', zorder=3)

    # Footer
    ax.text(0.50, 0.03, 'AI Support Copilot  |  Pilot Dashboard  |  Gyde AI POD',
            fontsize=8, color=MEDIUM_GRAY, va='center', ha='center', family='sans-serif')

    plt.tight_layout(pad=0.5)
    path = os.path.join(OUTPUT_DIR, "ui_wireframe.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print(f"Saved: {path}")
    return path


def generate_architecture_diagram():
    """Generate system architecture flow diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.patch.set_facecolor(WHITE)

    # Title
    ax.text(0.50, 0.96, 'AI Support Copilot \u2014 System Architecture',
            fontsize=16, fontweight='bold', color=DARK_BLUE,
            va='center', ha='center', family='sans-serif')
    ax.text(0.50, 0.93, 'End-to-end pipeline from ticket input to agent action',
            fontsize=10, color=MEDIUM_GRAY, va='center', ha='center', family='sans-serif')

    # ===== LEFT SIDE: Data Sources =====
    draw_rounded_rect(ax, 0.02, 0.55, 0.16, 0.30, '#FFF8E8', ACCENT_ORANGE, radius=0.01, lw=1.5)
    ax.text(0.10, 0.83, 'DATA SOURCES', fontsize=9, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', family='sans-serif', zorder=3)

    sources = [
        ('Tickets', 'Excel (pilot)\nFreshworks API (prod)'),
        ('KB Articles', '12 articles\nEmbedded & indexed'),
        ('Escalation\nRules', '5 rules\nCondition \u2192 Team'),
    ]
    for i, (name, detail) in enumerate(sources):
        ypos = 0.78 - i * 0.085
        draw_rounded_rect(ax, 0.03, ypos - 0.02, 0.14, 0.065, WHITE, BORDER_GRAY, radius=0.005, lw=0.5)
        ax.text(0.04, ypos + 0.025, name, fontsize=7.5, fontweight='bold',
                color=DARK_BLUE, va='center', family='sans-serif', zorder=3)
        ax.text(0.04, ypos - 0.005, detail, fontsize=6, color=MEDIUM_GRAY,
                va='center', family='sans-serif', zorder=3)

    # ===== CENTER: AI Pipeline =====
    pipeline_x = 0.22
    pipeline_w = 0.52
    draw_rounded_rect(ax, pipeline_x, 0.18, pipeline_w, 0.67, '#F8FAFC', MEDIUM_BLUE, radius=0.01, lw=1.5)
    ax.text(pipeline_x + pipeline_w/2, 0.83, 'AI PIPELINE', fontsize=10, fontweight='bold',
            color=MEDIUM_BLUE, va='center', ha='center', family='sans-serif', zorder=3)

    # Pipeline steps
    steps = [
        {
            'name': '1. CLASSIFY',
            'desc': 'LLM reads ticket text',
            'output': 'Category + Priority + Sentiment',
            'tech': 'Structured output prompting',
            'color': '#E3F2FD',
            'border': '#1976D2',
        },
        {
            'name': '2. RETRIEVE',
            'desc': 'Embed ticket \u2192 search KB index',
            'output': 'Top-K KB articles + scores',
            'tech': 'Hybrid: Vector + BM25',
            'color': '#E8F5E9',
            'border': '#388E3C',
        },
        {
            'name': '3. REASON',
            'desc': 'Ticket + KB + rules \u2192 LLM',
            'output': 'Action: Reply / Ask / Escalate',
            'tech': 'Chain-of-thought reasoning',
            'color': '#FFF3E0',
            'border': '#F57C00',
        },
        {
            'name': '4. DRAFT',
            'desc': 'Generate grounded response',
            'output': 'Response with KB citations',
            'tech': 'RAG with citation tracking',
            'color': '#F3E5F5',
            'border': '#7B1FA2',
        },
        {
            'name': '5. PRESENT',
            'desc': 'Display in copilot sidebar',
            'output': 'Full output + confidence + reasoning',
            'tech': 'Three-panel web app',
            'color': '#E0F2F1',
            'border': '#00796B',
        },
    ]

    step_h = 0.10
    step_gap = 0.015
    start_y = 0.73
    step_x = pipeline_x + 0.02
    step_w = pipeline_w - 0.04

    for i, step in enumerate(steps):
        y = start_y - i * (step_h + step_gap)
        draw_rounded_rect(ax, step_x, y, step_w, step_h, step['color'], step['border'], radius=0.008, lw=1.5)

        # Step name
        ax.text(step_x + 0.01, y + step_h - 0.025, step['name'], fontsize=9, fontweight='bold',
                color=step['border'], va='center', family='sans-serif', zorder=3)

        # Description
        ax.text(step_x + 0.12, y + step_h - 0.025, step['desc'], fontsize=8,
                color=DARK_GRAY, va='center', family='sans-serif', zorder=3)

        # Output
        ax.text(step_x + 0.01, y + 0.04, '\u2192 ', fontsize=8,
                color=step['border'], va='center', family='sans-serif', zorder=3)
        ax.text(step_x + 0.03, y + 0.04, step['output'], fontsize=8, fontweight='bold',
                color=DARK_GRAY, va='center', family='sans-serif', zorder=3)

        # Tech note
        ax.text(step_x + step_w - 0.01, y + 0.04, step['tech'], fontsize=7,
                color=MEDIUM_GRAY, va='center', ha='right', family='sans-serif',
                style='italic', zorder=3)

        # Arrow between steps
        if i < len(steps) - 1:
            arrow_y = y - step_gap / 2
            ax.annotate('', xy=(step_x + step_w/2, arrow_y - 0.005),
                       xytext=(step_x + step_w/2, arrow_y + 0.005),
                       arrowprops=dict(arrowstyle='->', color=MEDIUM_BLUE, lw=2),
                       zorder=3)

    # Arrow from data sources to pipeline
    ax.annotate('', xy=(pipeline_x, 0.70), xytext=(0.18, 0.70),
               arrowprops=dict(arrowstyle='->', color=ACCENT_ORANGE, lw=2), zorder=3)
    ax.annotate('', xy=(pipeline_x, 0.60), xytext=(0.18, 0.60),
               arrowprops=dict(arrowstyle='->', color=ACCENT_ORANGE, lw=2), zorder=3)

    # ===== RIGHT SIDE: Infrastructure =====
    draw_rounded_rect(ax, 0.78, 0.55, 0.20, 0.30, '#F0F8F0', ACCENT_GREEN, radius=0.01, lw=1.5)
    ax.text(0.88, 0.83, 'INFRASTRUCTURE', fontsize=9, fontweight='bold',
            color=ACCENT_GREEN, va='center', ha='center', family='sans-serif', zorder=3)

    infra = [
        ('GCP', 'Cloud platform'),
        ('LLM Gateway', 'Provider-agnostic\nSwappable models'),
        ('Vector Store', 'KB embeddings\nHybrid search index'),
        ('Database', 'Tickets, feedback\nAgent corrections'),
    ]
    for i, (name, detail) in enumerate(infra):
        ypos = 0.78 - i * 0.065
        draw_rounded_rect(ax, 0.79, ypos - 0.015, 0.18, 0.05, WHITE, BORDER_GRAY, radius=0.005, lw=0.5)
        ax.text(0.80, ypos + 0.015, name, fontsize=7.5, fontweight='bold',
                color=DARK_BLUE, va='center', family='sans-serif', zorder=3)
        ax.text(0.80, ypos - 0.005, detail, fontsize=6, color=MEDIUM_GRAY,
                va='center', family='sans-serif', zorder=3)

    # Arrow from pipeline to infra
    ax.annotate('', xy=(0.78, 0.70), xytext=(pipeline_x + pipeline_w, 0.70),
               arrowprops=dict(arrowstyle='<->', color=ACCENT_GREEN, lw=1.5), zorder=3)

    # ===== BOTTOM: Feedback Loop =====
    draw_rounded_rect(ax, 0.22, 0.03, 0.52, 0.12, LIGHT_BLUE, MEDIUM_BLUE, radius=0.01, lw=1.5)
    ax.text(0.48, 0.135, 'FEEDBACK LOOP', fontsize=9, fontweight='bold',
            color=MEDIUM_BLUE, va='center', ha='center', family='sans-serif', zorder=3)

    feedback_flow = 'Agent reviews \u2192 Accepts/Edits \u2192 Rates ("helpful?") \u2192 Corrections saved \u2192 System learns'
    ax.text(0.48, 0.095, feedback_flow, fontsize=8.5,
            color=DARK_GRAY, va='center', ha='center', family='sans-serif', zorder=3)
    ax.text(0.48, 0.06, 'Creates golden evaluations from real usage  |  Drives continuous improvement',
            fontsize=7.5, color=MEDIUM_GRAY, va='center', ha='center',
            family='sans-serif', style='italic', zorder=3)

    # Arrow from pipeline to feedback
    ax.annotate('', xy=(0.48, 0.15), xytext=(0.48, 0.18),
               arrowprops=dict(arrowstyle='->', color=MEDIUM_BLUE, lw=2), zorder=3)

    # ===== BOTTOM LEFT: Guardrails =====
    draw_rounded_rect(ax, 0.02, 0.03, 0.16, 0.12, '#FFF0F0', ACCENT_RED, radius=0.01, lw=1.5)
    ax.text(0.10, 0.135, 'GUARDRAILS', fontsize=9, fontweight='bold',
            color=ACCENT_RED, va='center', ha='center', family='sans-serif', zorder=3)
    guardrail_items = ['Profanity filter', 'Misuse prevention', 'Hallucination check', 'Confidence gating']
    for i, item in enumerate(guardrail_items):
        ax.text(0.04, 0.105 - i * 0.02, f'\u2022 {item}', fontsize=7,
                color=DARK_GRAY, va='center', family='sans-serif', zorder=3)

    # ===== BOTTOM RIGHT: Evaluation =====
    draw_rounded_rect(ax, 0.78, 0.03, 0.20, 0.12, '#FFF8E8', ACCENT_ORANGE, radius=0.01, lw=1.5)
    ax.text(0.88, 0.135, 'EVALUATION', fontsize=9, fontweight='bold',
            color=ACCENT_ORANGE, va='center', ha='center', family='sans-serif', zorder=3)
    eval_items = ['Golden dataset (12 + expanded)', '1000 synthetic questions', 'Automated scoring', 'Target: \u226585% accuracy']
    for i, item in enumerate(eval_items):
        ax.text(0.80, 0.105 - i * 0.02, f'\u2022 {item}', fontsize=7,
                color=DARK_GRAY, va='center', family='sans-serif', zorder=3)

    # ===== LEFT SIDE bottom: Human in the loop =====
    draw_rounded_rect(ax, 0.02, 0.18, 0.16, 0.33, '#E8F0F8', MEDIUM_BLUE, radius=0.01, lw=1.5)
    ax.text(0.10, 0.495, 'HUMAN IN', fontsize=9, fontweight='bold',
            color=MEDIUM_BLUE, va='center', ha='center', family='sans-serif', zorder=3)
    ax.text(0.10, 0.47, 'THE LOOP', fontsize=9, fontweight='bold',
            color=MEDIUM_BLUE, va='center', ha='center', family='sans-serif', zorder=3)

    ax.text(0.10, 0.43, 'Support Agent', fontsize=9, fontweight='bold',
            color=DARK_BLUE, va='center', ha='center', family='sans-serif', zorder=3)

    hitl_items = ['Views copilot output', 'Reviews classification', 'Reads draft response',
                  'Edits if needed', 'Approves & sends', 'Provides feedback']
    for i, item in enumerate(hitl_items):
        ax.text(0.04, 0.39 - i * 0.025, f'{i+1}. {item}', fontsize=7,
                color=DARK_GRAY, va='center', family='sans-serif', zorder=3)

    ax.text(0.10, 0.21, 'Agent ALWAYS decides', fontsize=7, fontweight='bold',
            color=ACCENT_RED, va='center', ha='center', family='sans-serif', zorder=3)

    # Arrow from HITL to pipeline
    ax.annotate('', xy=(pipeline_x, 0.35), xytext=(0.18, 0.35),
               arrowprops=dict(arrowstyle='<->', color=MEDIUM_BLUE, lw=1.5), zorder=3)

    # ===== RIGHT SIDE bottom: Infra continued =====
    draw_rounded_rect(ax, 0.78, 0.18, 0.20, 0.33, '#F8F5FF', '#7B1FA2', radius=0.01, lw=1.5)
    ax.text(0.88, 0.495, 'TECH STACK', fontsize=9, fontweight='bold',
            color='#7B1FA2', va='center', ha='center', family='sans-serif', zorder=3)

    tech_items = [
        ('Frontend', 'React / Next.js'),
        ('Backend', 'Python (FastAPI)'),
        ('LLM', 'Provider-agnostic'),
        ('Embeddings', 'TBD (Architecture)'),
        ('Vector DB', 'TBD (Architecture)'),
        ('Search', 'Hybrid (Vector+BM25)'),
        ('Cloud', 'GCP'),
        ('CI/CD', 'GitHub Actions'),
    ]
    for i, (label, val) in enumerate(tech_items):
        ypos = 0.46 - i * 0.03
        ax.text(0.80, ypos, f'{label}:', fontsize=7, fontweight='bold',
                color='#7B1FA2', va='center', family='sans-serif', zorder=3)
        ax.text(0.88, ypos, val, fontsize=7,
                color=DARK_GRAY, va='center', family='sans-serif', zorder=3)

    plt.tight_layout(pad=0.5)
    path = os.path.join(OUTPUT_DIR, "architecture_diagram.png")
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=WHITE)
    plt.close(fig)
    print(f"Saved: {path}")
    return path


if __name__ == "__main__":
    ui_path = generate_ui_wireframe()
    arch_path = generate_architecture_diagram()
