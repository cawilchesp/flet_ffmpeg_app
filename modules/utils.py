def format_duration(total_seconds: float) -> str:
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    parts = []
    if hours:
        parts.append(f"{hours:02d}h")
    if minutes:
        parts.append(f"{minutes:02d}m")
    parts.append(f"{seconds:02d}s")

    return ' '.join(parts)

def format_bandwidth(bps: float) -> str:
    if bps < 1_000:
        return f"{bps:.2f} bps"
    elif bps < 1_000_000:
        kbps = bps / 1_000
        return f"{kbps:.2f} Kbps"
    elif bps < 1_000_000_000:
        mbps = bps / 1_000_000
        return f"{mbps:.2f} Mbps"
    else:
        gbps = bps / 1_000_000_000
        return f"{gbps:.2f} Gbps"
