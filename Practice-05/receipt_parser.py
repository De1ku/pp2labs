import re
import json



def main(file_name) -> dict:
    with open(file_name, 'r', encoding='utf-8') as f:
        data = f.read()

    price_re = r'\d{1,3}(?: \d{3})*,\d{2}'
    item_re = re.compile(rf'^\d+\.\n(.*?)\n(\d+,\d{{3}}) x ({price_re})\n({price_re})', re.M)

    items = [
        {
            'product': ' '.join(name.split()),
            'quantity': float(qty.replace(',', '.')),
            'unit_price': float(unit_price.replace(' ', '').replace(',', '.')),
            'price': float(line_total.replace(' ', '').replace(',', '.'))
        }
        for name, qty, unit_price, line_total in item_re.findall(data)
    ]

    all_prices = [float(x.replace(' ', '').replace(',', '.')) for x in re.findall(price_re, data)]
    total_match = re.search(rf'ИТОГО:\s*\n\s*({price_re})', data)
    date_time = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s\d{2}\:\d{2}\:\d{2})', data)
    payment_match = re.search(rf'^(.*?):\s*$\n^({price_re})\s*$\n^ИТОГО:', data, re.M)

    calculated_total = round(sum(i['price'] for i in items), 2)

    return {
        'date_time': date_time.group(1) if date_time else None,
        'payment_method': payment_match.group(1) if payment_match else None, 
        'product_names': [i['product'] for i in items],
        'all_prices': all_prices,
        'items': items,
        'total_amount': float(total_match.group(1).replace(' ', '').replace(',', '.')) if total_match else None,
        'calculated_total': calculated_total
    }


if __name__ == '__main__':
    file_name = 'raw.txt'
    print(json.dumps(main(file_name), indent=2, ensure_ascii=False))