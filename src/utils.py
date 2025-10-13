def format_price(price: float) -> str:
    """Formats a numeric price into a readable string (e.g., ₹1.20 Cr)."""
    if not isinstance(price, (int, float)):
        return "N/A"
    if price >= 1_00_00_000:
        return f"₹{price / 1_00_00_000:.2f} Cr"
    else:
        return f"₹{price / 1_00_000:.2f} L"