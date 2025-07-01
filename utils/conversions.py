# PGN (Parameter Group Number) to CAN ID conversion
# Format: 0x18FF0000 | ((PGN & 0xFF) << 8) | SA
# This follows the J1939 protocol format for extended CAN IDs
def pgn_to_can_id(pgn, sa="ISO175_SA"):
    return 0x18FF0000 | ((pgn & 0xFF) << 8) | sa


def parse_j1939_id_to_prio_pgn_sa(hex_id_str):
    """Parse a J1939 CAN ID into priority, PGN, and source address."""
    can_id = int(hex_id_str, 16)

    priority = (can_id >> 26) & 0x7  # 3 bits
    pgn_raw = (can_id >> 8) & 0xFFFF  # 16 bits
    sa = can_id & 0xFF  # 8 bits

    # For PGNs with a PDU1 format (destination-specific), PGN is only upper 14 bits
    dp = (can_id >> 24) & 0x1
    pf = (can_id >> 16) & 0xFF
    ps = (can_id >> 8) & 0xFF

    if pf < 240:
        pgn = pf << 8  # Only upper byte of PS is used
    else:
        pgn = (pf << 8) | ps

    return {
        "CAN ID": hex_id_str,
        "Priority": priority,
        "PGN": f"{pgn:05X}",
        "SA": f"{sa:02X}",
    }


def convert_standard_hex_to_j1939(can_id_hex):
    """Convert a standard 29-bit CAN ID (hex string or int) into J1939 fields."""
    if isinstance(can_id_hex, str):
        can_id = int(can_id_hex, 16)
    else:
        can_id = can_id_hex

    priority = (can_id >> 26) & 0x7
    dp = (can_id >> 24) & 0x1
    pf = (can_id >> 16) & 0xFF
    ps = (can_id >> 8) & 0xFF
    sa = can_id & 0xFF

    # Determine PGN
    if pf < 240:
        # PDU1 format: PGN = pf << 8 (ps is destination address)
        pgn = pf << 8
    else:
        # PDU2 format: PGN = pf << 8 | ps
        pgn = (pf << 8) | ps

    return {
        "CAN ID": f"{can_id:08X}",
        "Priority": priority,
        "PGN": f"{pgn:05X}",
        "PF": pf,
        "PS": ps,
        "SA": f"{sa:02X}",
    }
