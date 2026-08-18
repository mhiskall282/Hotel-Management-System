"""
HMS Architecture & UML Diagram Generator
Generates high-resolution publication-quality PNG diagrams for the HMS project report.
Diagrams:
1. db_erd_architecture.png - Entity Relationship Diagram
2. system_architecture_uml.png - Layered Multi-Tier System & Component Architecture
3. state_machine_flow.png - Booking Lifecycle & Room Operational State Machine
4. operational_sequence_flow.png - UML Operational Sequence Diagram
5. ui_role_dashboard_layout.png - UI Layout & Dashboard Component Architecture
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('docs/diagrams', exist_ok=True)

# Color Palette
NAVY = '#0A2647'
ROYAL = '#144272'
GOLD = '#D97706'
LIGHT_GOLD = '#FEF3C7'
SLATE = '#0F172A'
MUTED = '#64748B'
BG_LIGHT = '#F8FAFC'
CARD_BORDER = '#CBD5E1'
GREEN = '#059669'
AMBER = '#D97706'
RED = '#DC2626'
BLUE = '#2563EB'
PURPLE = '#7C3AED'

def draw_rounded_box(ax, x, y, w, h, title, items=[], bg_color='#FFFFFF', header_color=NAVY, title_color='#FFFFFF', border_color=CARD_BORDER):
    # Main Box
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.04",
                                 facecolor=bg_color, edgecolor=border_color, linewidth=1.5, zorder=2)
    ax.add_patch(box)
    
    # Header Box
    header_h = h * 0.26 if items else h
    header_box = patches.FancyBboxPatch((x, y + h - header_h), w, header_h,
                                        boxstyle="round,pad=0.02,rounding_size=0.04",
                                        facecolor=header_color, edgecolor=border_color, linewidth=1.2, zorder=3)
    ax.add_patch(header_box)
    
    # Header Text
    ax.text(x + w/2, y + h - header_h/2, title, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color=title_color, zorder=4)
    
    # Items
    if items:
        item_y = y + h - header_h - 0.04
        dy = (h - header_h - 0.05) / max(len(items), 1)
        for item in items:
            is_pk = "PK" in item
            is_fk = "FK" in item
            col = RED if is_pk else (BLUE if is_fk else SLATE)
            weight = 'bold' if (is_pk or is_fk) else 'normal'
            ax.text(x + 0.03, item_y, item, ha='left', va='top', fontsize=6.8, fontweight=weight, color=col, zorder=4)
            item_y -= dy

def generate_erd():
    fig, ax = plt.subplots(figsize=(14, 9.5), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9.5)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    
    # Title
    ax.text(7, 9.15, "HOTEL MANAGEMENT SYSTEM (HMS) -- ENTITY RELATIONSHIP DIAGRAM (ERD)",
            ha='center', va='center', fontsize=14, fontweight='bold', color=NAVY)
    ax.text(7, 8.85, "Normalized 3NF Relational Data Architecture with Foreign Keys & Cardinalities",
            ha='center', va='center', fontsize=9.5, color=MUTED)

    # Tables definition: (x, y, w, h, title, items, header_color)
    # Row 1: Users, Roles, Guests, Room Types
    draw_rounded_box(ax, 0.5, 6.0, 2.5, 2.3, "users (Staff)", [
        "+ id [PK] (BIGINT)",
        "+ name (VARCHAR)",
        "+ email [UK] (VARCHAR)",
        "+ password (VARCHAR)",
        "+ is_active (BOOLEAN)"
    ], header_color=NAVY)

    draw_rounded_box(ax, 3.8, 6.0, 2.8, 2.3, "guests (Guest Folio)", [
        "+ id [PK] (BIGINT)",
        "+ name (VARCHAR)",
        "+ phone (VARCHAR)",
        "+ email (VARCHAR)",
        "+ id_number (VARCHAR)",
        "+ nationality (VARCHAR)",
        "+ deleted_at (TIMESTAMP)"
    ], header_color=NAVY)

    draw_rounded_box(ax, 7.4, 6.0, 2.8, 2.3, "room_types (Categories)", [
        "+ id [PK] (BIGINT)",
        "+ name (VARCHAR)",
        "+ base_rate (DECIMAL)",
        "+ capacity (TINYINT)",
        "+ description (TEXT)"
    ], header_color=ROYAL)

    draw_rounded_box(ax, 10.9, 6.0, 2.6, 2.3, "rooms (Inventory)", [
        "+ id [PK] (BIGINT)",
        "+ room_number [UK] (VARCHAR)",
        "+ room_type_id [FK] (BIGINT)",
        "+ status (ENUM)",
        "+ floor (TINYINT)"
    ], header_color=ROYAL)

    # Row 2: Bookings (Central), CheckInOut
    draw_rounded_box(ax, 5.2, 2.8, 3.6, 2.5, "bookings (Reservations)", [
        "+ id [PK] (BIGINT)",
        "+ booking_reference [UK] (VARCHAR)",
        "+ guest_id [FK] (BIGINT)",
        "+ room_id [FK] (BIGINT)",
        "+ check_in_date (DATE)",
        "+ check_out_date (DATE)",
        "+ status (ENUM)",
        "+ created_by [FK] (BIGINT)"
    ], header_color=GOLD)

    draw_rounded_box(ax, 0.5, 2.8, 3.2, 2.2, "check_in_outs (Audits)", [
        "+ id [PK] (BIGINT)",
        "+ booking_id [FK, UK] (BIGINT)",
        "+ actual_check_in_at (TIMESTAMP)",
        "+ actual_check_out_at (TIMESTAMP)",
        "+ checked_in_by [FK] (BIGINT)",
        "+ checked_out_by [FK] (BIGINT)"
    ], header_color=NAVY)

    draw_rounded_box(ax, 10.2, 2.8, 3.3, 2.2, "maintenance_requests", [
        "+ id [PK] (BIGINT)",
        "+ room_id [FK] (BIGINT)",
        "+ issue_title (VARCHAR)",
        "+ priority (ENUM)",
        "+ status (ENUM)",
        "+ reported_by [FK] (BIGINT)"
    ], header_color=RED)

    # Row 3: Invoices, Payments, Additional Services, Audit Logs
    draw_rounded_box(ax, 4.0, 0.3, 3.2, 2.1, "invoices (Billing)", [
        "+ id [PK] (BIGINT)",
        "+ booking_id [FK, UK] (BIGINT)",
        "+ room_charge (DECIMAL)",
        "+ services_charge (DECIMAL)",
        "+ total (DECIMAL)",
        "+ status (ENUM)"
    ], header_color=GREEN)

    draw_rounded_box(ax, 8.0, 0.3, 2.8, 2.1, "payments (Ledger)", [
        "+ id [PK] (BIGINT)",
        "+ invoice_id [FK] (BIGINT)",
        "+ amount (DECIMAL)",
        "+ method (ENUM)",
        "+ paid_at (TIMESTAMP)",
        "+ recorded_by [FK] (BIGINT)"
    ], header_color=GREEN)

    draw_rounded_box(ax, 0.5, 0.3, 3.0, 2.1, "additional_services", [
        "+ id [PK] (BIGINT)",
        "+ booking_id [FK] (BIGINT)",
        "+ invoice_id [FK] (BIGINT)",
        "+ name (VARCHAR)",
        "+ amount (DECIMAL)",
        "+ added_by [FK] (BIGINT)"
    ], header_color=GOLD)

    draw_rounded_box(ax, 11.2, 0.3, 2.3, 2.1, "audit_logs", [
        "+ id [PK] (BIGINT)",
        "+ user_id [FK] (BIGINT)",
        "+ category (VARCHAR)",
        "+ action (VARCHAR)",
        "+ ip_address (VARCHAR)"
    ], header_color=SLATE)

    # Relationship Arrows with Cardinality labels
    def draw_rel(x1, y1, x2, y2, card_start="1", card_end="N", color=MUTED, style='-|>'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.3, shrinkA=3, shrinkB=3), zorder=1)
        ax.text(x1 + (x2-x1)*0.15, y1 + (y2-y1)*0.15 + 0.05, card_start, fontsize=7.5, fontweight='bold', color=NAVY, zorder=5)
        ax.text(x1 + (x2-x1)*0.85, y1 + (y2-y1)*0.85 + 0.05, card_end, fontsize=7.5, fontweight='bold', color=RED, zorder=5)

    # Guests -> Bookings (1:N)
    draw_rel(5.2, 6.0, 6.2, 5.3, "1", "N")
    # Rooms -> Bookings (1:N)
    draw_rel(11.5, 6.0, 8.8, 5.0, "1", "N")
    # RoomTypes -> Rooms (1:N)
    draw_rel(10.2, 7.1, 10.9, 7.1, "1", "N")
    # Users -> Bookings (1:N)
    draw_rel(3.0, 6.5, 5.2, 4.8, "1", "N")
    # Bookings -> CheckInOut (1:1)
    draw_rel(5.2, 3.8, 3.7, 3.8, "1", "1")
    # Bookings -> Invoices (1:1)
    draw_rel(6.5, 2.8, 5.8, 2.4, "1", "1")
    # Invoices -> Payments (1:N)
    draw_rel(7.2, 1.3, 8.0, 1.3, "1", "N")
    # Bookings -> Additional Services (1:N)
    draw_rel(5.2, 3.0, 3.5, 2.0, "1", "N")
    # Rooms -> Maintenance (1:N)
    draw_rel(12.2, 6.0, 12.0, 5.0, "1", "N")

    plt.tight_layout()
    plt.savefig('docs/diagrams/db_erd_architecture.png', bbox_inches='tight')
    plt.close()
    print("Saved docs/diagrams/db_erd_architecture.png")

def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(14, 9.5), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9.5)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    ax.text(7, 9.15, "HOTEL MANAGEMENT SYSTEM (HMS) -- MULTI-TIER SYSTEM ARCHITECTURE",
            ha='center', va='center', fontsize=14, fontweight='bold', color=NAVY)
    ax.text(7, 8.85, "UML Layered Software Design: Presentation, Routing, Controllers, Actions/Services & Persistence",
            ha='center', va='center', fontsize=9.5, color=MUTED)

    # 1. Presentation Tier (Top)
    draw_rounded_box(ax, 0.8, 6.8, 12.4, 1.8, "1. PRESENTATION TIER (Responsive Web UI & Micro-Interactivity)", [
        "&bull; Laravel Blade Templates (Role-Segmented Views: Admin, Manager, Reception, Housekeeping, Accountant, Public Landing)",
        "&bull; Alpine.js Micro-Interactivity (Dynamic Modals, Inactivity Heartbeat Idle Timer, Real-Time Folio Calculation)",
        "&bull; Tailwind CSS v3 (Npontu-Inspired Design Tokens: Deep Navy #0A2647, Warm Gold #F2A93B, Slate Surfaces)"
    ], header_color=NAVY)

    # 2. Security & Routing Tier
    draw_rounded_box(ax, 0.8, 4.8, 12.4, 1.7, "2. ROUTING, SECURITY & ACCESS CONTROL TIER", [
        "&bull; Laravel Web Routes (routes/web.php with CSRF & Encrypted Session Cookies)",
        "&bull; Spatie Laravel-Permission RBAC Middleware (role:admin, role:manager, role:receptionist, role:housekeeping, role:accountant)",
        "&bull; Session Inactivity Guard (30-Minute Timeout Termination via /logout-idle)"
    ], header_color=ROYAL)

    # 3. Application Controllers & Form Requests
    draw_rounded_box(ax, 0.8, 2.7, 5.8, 1.8, "3A. HTTP CONTROLLERS & FORM REQUESTS", [
        "&bull; AuthenticatedSessionController, UserController",
        "&bull; RoomController, RoomTypeController, HousekeepingController",
        "&bull; GuestController, BookingController, CheckInOutController",
        "&bull; InvoiceController, DashboardController, ReportController"
    ], header_color=BLUE)

    # 3B. Domain Actions & Services Tier
    draw_rounded_box(ax, 7.4, 2.7, 5.8, 1.8, "3B. DOMAIN ACTIONS & CALCULATION SERVICES", [
        "&bull; Actions: CreateBookingAction (DB Lock), CheckInAction, CheckOutAction, RecordPaymentAction",
        "&bull; Services: AvailabilityService, BillingService, ReportingService",
        "&bull; Invariants: Anti-Double-Booking Pessimistic Lock, State Derivations"
    ], header_color=GOLD)

    # 4. Persistence & Database Tier (Bottom)
    draw_rounded_box(ax, 0.8, 0.4, 12.4, 1.9, "4. PERSISTENCE & INFRASTRUCTURE TIER", [
        "&bull; Eloquent ORM (12 Models: User, Guest, Room, Booking, CheckInOut, Invoice, Payment, Service, AuditLog)",
        "&bull; MySQL 8.0+ Database (InnoDB Engine, ACID Transactions, Row-Level lockForUpdate(), B-Tree Indexes)",
        "&bull; Export & DevOps Infrastructure: Barryvdh DomPDF, Maatwebsite Excel, Docker Alpine Container, Render Cloud"
    ], header_color=SLATE)

    # Inter-tier Arrows
    def draw_tier_arrow(y_top, y_bottom, label=""):
        ax.annotate('', xy=(7, y_bottom), xytext=(7, y_top),
                    arrowprops=dict(arrowstyle="<->", color=GOLD, lw=2.2, shrinkA=2, shrinkB=2), zorder=5)
        if label:
            ax.text(7.2, (y_top + y_bottom)/2, label, fontsize=8, fontweight='bold', color=NAVY, zorder=6)

    draw_tier_arrow(6.8, 6.5, "HTTP Requests / JSON / HTML")
    draw_tier_arrow(4.8, 4.5, "Authorized Request DTOs")
    draw_tier_arrow(2.7, 2.3, "ACID Transactions & Eloquent Queries")

    plt.tight_layout()
    plt.savefig('docs/diagrams/system_architecture_uml.png', bbox_inches='tight')
    plt.close()
    print("Saved docs/diagrams/system_architecture_uml.png")

def generate_state_machines():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=300)
    fig.patch.set_facecolor('#F8FAFC')
    
    # Left: Booking State Machine
    ax1.set_xlim(0, 7)
    ax1.set_ylim(0, 8)
    ax1.axis('off')
    ax1.text(3.5, 7.6, "A. BOOKING LIFECYCLE STATE MACHINE", ha='center', va='center', fontsize=12, fontweight='bold', color=NAVY)
    
    draw_rounded_box(ax1, 2.2, 6.0, 2.6, 0.9, "pending", ["New form submitted"], header_color=MUTED)
    draw_rounded_box(ax1, 2.2, 4.3, 2.6, 0.9, "confirmed", ["Dates locked; room reserved"], header_color=BLUE)
    draw_rounded_box(ax1, 2.2, 2.6, 2.6, 0.9, "checked_in", ["Room occupied; stay active"], header_color=GOLD)
    draw_rounded_box(ax1, 2.2, 0.9, 2.6, 0.9, "checked_out", ["Completed; invoice settled"], header_color=GREEN)
    draw_rounded_box(ax1, 5.0, 5.1, 1.8, 0.9, "cancelled", ["Dates released"], header_color=RED)

    # Arrows for Booking
    def b_arrow(y1, y2, text):
        ax1.annotate('', xy=(3.5, y2), xytext=(3.5, y1), arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.8))
        ax1.text(3.6, (y1+y2)/2, text, fontsize=7.5, color=SLATE, va='center')

    b_arrow(6.0, 5.2, "Staff / System confirms")
    b_arrow(4.3, 3.5, "Guest arrives (Check-In FR-5.1)")
    b_arrow(2.6, 1.8, "Guest departs (Check-Out FR-5.2)")

    # Cancel arrows
    ax1.annotate('', xy=(5.0, 5.6), xytext=(4.8, 6.4), arrowprops=dict(arrowstyle="->", color=RED, lw=1.4, linestyle='--'))
    ax1.annotate('', xy=(5.0, 5.4), xytext=(4.8, 4.8), arrowprops=dict(arrowstyle="->", color=RED, lw=1.4, linestyle='--'))
    ax1.text(5.1, 6.1, "Cancel prior to check-in", fontsize=6.8, color=RED)

    # Right: Room Status State Machine
    ax2.set_xlim(0, 7)
    ax2.set_ylim(0, 8)
    ax2.axis('off')
    ax2.text(3.5, 7.6, "B. ROOM STATUS OPERATIONAL STATE MACHINE", ha='center', va='center', fontsize=12, fontweight='bold', color=NAVY)

    draw_rounded_box(ax2, 2.2, 6.2, 2.6, 0.9, "available", ["Ready for new guest"], header_color=GREEN)
    draw_rounded_box(ax2, 4.4, 4.6, 2.4, 0.9, "reserved", ["Booking confirmed"], header_color=BLUE)
    draw_rounded_box(ax2, 4.4, 2.8, 2.4, 0.9, "occupied", ["Guest checked in"], header_color=GOLD)
    draw_rounded_box(ax2, 2.2, 1.2, 2.6, 0.9, "dirty", ["Pending sanitization"], header_color=AMBER)
    draw_rounded_box(ax2, 0.2, 3.8, 2.2, 1.2, "maintenance", ["Under repair\n(out of service)"], header_color=RED)

    # Arrows for Room
    ax2.annotate('', xy=(5.4, 5.5), xytext=(4.5, 6.5), arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))
    ax2.text(5.3, 6.2, "Booking created", fontsize=7.2, color=SLATE)

    ax2.annotate('', xy=(5.6, 3.7), xytext=(5.6, 4.6), arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))
    ax2.text(5.7, 4.15, "Check-in", fontsize=7.2, color=SLATE)

    ax2.annotate('', xy=(4.5, 2.1), xytext=(5.4, 2.8), arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))
    ax2.text(5.2, 2.3, "Check-out", fontsize=7.2, color=SLATE)

    # Dirty -> Available (Housekeeper cleans)
    ax2.annotate('', xy=(2.4, 6.2), xytext=(2.4, 2.1), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8, connectionstyle="arc3,rad=-0.3"))
    ax2.text(1.2, 4.2, "Housekeeper\nmarks clean (FR-2.3)", fontsize=7.2, color=GREEN, fontweight='bold')

    # Maintenance transitions
    ax2.annotate('', xy=(1.4, 5.0), xytext=(2.2, 6.4), arrowprops=dict(arrowstyle="->", color=RED, lw=1.2, linestyle=':'))
    ax2.annotate('', xy=(2.2, 6.2), xytext=(1.4, 5.0), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2, linestyle=':'))
    ax2.text(0.3, 5.8, "Issue reported / Resolved", fontsize=6.8, color=RED)

    plt.tight_layout()
    plt.savefig('docs/diagrams/state_machine_flow.png', bbox_inches='tight')
    plt.close()
    print("Saved docs/diagrams/state_machine_flow.png")

def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    ax.text(7, 7.6, "HOTEL MANAGEMENT SYSTEM (HMS) -- OPERATIONAL SEQUENCE DIAGRAM",
            ha='center', va='center', fontsize=14, fontweight='bold', color=NAVY)
    ax.text(7, 7.3, "End-to-End Workflow: Reservation -> Concurrency Lock -> Check-In -> Folio Billing -> Check-Out -> Cleaning",
            ha='center', va='center', fontsize=9.5, color=MUTED)

    # Lifelines: (X, Label, Color)
    actors = [
        (1.5, "Guest / Client", BLUE),
        (4.2, "Front Desk (Receptionist)", ROYAL),
        (7.0, "HMS Backend Engine & Lock", GOLD),
        (9.8, "Accountant (Cashier)", GREEN),
        (12.5, "Housekeeping Staff", AMBER),
    ]

    for x, label, col in actors:
        # Header box
        box = patches.FancyBboxPatch((x-1.1, 6.4), 2.2, 0.6, boxstyle="round,pad=0.02,rounding_size=0.03",
                                     facecolor=col, edgecolor=CARD_BORDER, linewidth=1.2, zorder=3)
        ax.add_patch(box)
        ax.text(x, 6.7, label, ha='center', va='center', fontsize=8, fontweight='bold', color='#FFFFFF', zorder=4)
        # Lifeline dotted line
        ax.plot([x, x], [0.5, 6.4], color=CARD_BORDER, linestyle='--', lw=1.5, zorder=1)

    # Sequence Messages
    steps = [
        (1.5, 4.2, 5.8, "1. Request Reservation (Dates & Room Type)", BLUE),
        (4.2, 7.0, 5.2, "2. CreateBookingAction(lockForUpdate)", GOLD),
        (7.0, 7.0, 4.7, "3. Verify zero overlap & generate ref HMS-XXXXXXXX", GOLD),
        (7.0, 4.2, 4.2, "4. Return Confirmed Booking & Invoice", GREEN),
        (4.2, 1.5, 3.7, "5. Provide Booking Confirmation & Folio Ref", BLUE),
        (4.2, 7.0, 3.1, "6. CheckInAction -> set room=occupied (FR-5.1)", ROYAL),
        (4.2, 7.0, 2.5, "7. Add Service Charge (Room Service GHS 120)", GOLD),
        (4.2, 7.0, 1.9, "8. CheckOutAction -> set room=dirty (FR-5.2)", ROYAL),
        (9.8, 7.0, 1.4, "9. RecordPaymentAction(Cash/Card/MoMo) -> Invoice Paid", GREEN),
        (7.0, 12.5, 0.9, "10. Room marked dirty on Housekeeping Desk", AMBER),
        (12.5, 7.0, 0.5, "11. Housekeeper completes cleaning -> set room=available", GREEN),
    ]

    for x1, x2, y, msg, col in steps:
        if x1 == x2:
            # Self loop
            ax.annotate('', xy=(x1+0.05, y-0.2), xytext=(x1+0.05, y),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.4, connectionstyle="arc3,rad=-0.8"), zorder=3)
            ax.text(x1+0.35, y-0.1, msg, fontsize=7.2, fontweight='bold', color=col, va='center', zorder=4)
        else:
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.5, shrinkA=3, shrinkB=3), zorder=3)
            ax.text((x1+x2)/2, y+0.12, msg, fontsize=7.2, fontweight='bold', color=col, ha='center', va='bottom', zorder=4)

    plt.tight_layout()
    plt.savefig('docs/diagrams/operational_sequence_flow.png', bbox_inches='tight')
    plt.close()
    print("Saved docs/diagrams/operational_sequence_flow.png")

if __name__ == '__main__':
    generate_erd()
    generate_system_architecture()
    generate_state_machines()
    generate_sequence_diagram()
    print("All architecture and UML diagrams generated successfully!")
