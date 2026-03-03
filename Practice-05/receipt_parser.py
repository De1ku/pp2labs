import json
import re
from pathlib import Path

RAW_FILE = Path(__file__).with_name('raw.txt')

PRICE_RE = r'\d{1,3}(?: \d{3})*,\d{2}'
ITEM_RE = re.compile(
    rf'^\d+\.\n(.*?)\n(\d+,\d{{3}}) x ({PRICE_RE})\n({PRICE_RE})',
    re.MULTILINE,
)


def to_float(value: str) -> float:
    return float(value.replace(' ', '').replace(',', '.'))

def parse_receipt(text: str) -> dict:
    items = [
        {
            'product': ' '.join(name.split()),
            'quantity': float(qty.replace(',', '.')),
            'unit_price': to_float(unit_price),
            'price': to_float(line_total),
        }
        for name, qty, unit_price, line_total in ITEM_RE.findall(text)
    ]

    all_prices = [to_float(x) for x in re.findall(PRICE_RE, text)]

    total_match = re.search(rf'ИТОГО:\s*\n\s*({PRICE_RE})', text)
    datetime_match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})', text)
    payment_match = re.search(r'^(.*?):\s*$\n^(' + PRICE_RE + r')\s*$\n^ИТОГО:', text, re.MULTILINE)

    calculated_total = round(sum(item['price'] for item in items), 2)

    return {
        'date_time': datetime_match.group(1) if datetime_match else None,
        'payment_method': payment_match.group(1) if payment_match else None,
        'product_names': [item['product'] for item in items],
        'all_prices': all_prices,
        'items': items,
        'total_amount': to_float(total_match.group(1)) if total_match else calculated_total,
        'calculated_total': calculated_total,
    }

if __name__ == '__main__':
    text = RAW_FILE.read_text(encoding='utf-8')
    print(json.dumps(parse_receipt(text), ensure_ascii=False, indent=2))